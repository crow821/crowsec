/**
 * shellcode_launcher.exe: allows loading & executing arbitrary binary files.
 * Copyright (C) 2010 Jerrold "Jay" Smith (public@clinicallyinane.com)
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <Windows.h>

#define EXTRA_SPACE     0x10000
#define MAX_REG_NAME_SIZE 4

#define REG_EAX         0
#define REG_EBX         1
#define REG_ECX         2
#define REG_EDX         3
#define REG_EDI         4
#define REG_ESI         5

#define REG_MAX         6       

#define MAX_OPEN_FILES  10

char* regNames[] = {
    "eax",
    "ebx",
    "ecx",
    "edx",
    "edi",
    "esi"
};

#define NUM_REGISTERS   6

typedef void(*void_func_ptr)(void);

unsigned char callNext[] = {
    0xe8, 0x00, 0x00, 0x00, 0x00,       //call  $+5
};

#if 0
unsigned char callPopEdi[] = {
    0xe8, 0x00, 0x00, 0x00, 0x00,       //call  $+5
    0x5f                                //pop   edi
};
#endif

unsigned char popRegInstr[] = {
    0x58,                           //eax
    0x5b,                           //ebx
    0x59,                           //ecx
    0x5a,                           //edx
    0x5f,                           //edi
    0x5e                            //esi
};

#if 0
unsigned char addEdiImmediate[] = {
    0x81, 0xc7                          // add edi, <32-bit immediate>
};
#endif

unsigned char addRegImmediate[][2] = {
    { 0x81, 0xc0 }, //add eax, 0x11223344: 81c0  44332211
    { 0x81, 0xc3 }, //add ebx, 0x11223344: 81c3  44332211
    { 0x81, 0xc1 }, //add ecx, 0x11223344: 81c1  44332211
    { 0x81, 0xc2 }, //add edx, 0x11223344: 81c2  44332211
    { 0x81, 0xc6 }, //add esi, 0x11223344: 81c6  44332211
    { 0x81, 0xc7 }, //add edi, 0x11223344: 81c7  44332211
};

unsigned char jmp32bitOffset[] = {
    0xe9                                // jmp <32-bit immediate_offset>
};

unsigned char breakpoint[] = {
    0xcc                                // int3
};

struct FileInfo {
    int     index;
    char*   names[MAX_OPEN_FILES];
    HANDLE  handles[MAX_OPEN_FILES];
};

struct ConfigurationData {
    int             doBp;
    DWORD           startOff;
	DWORD			baseAddress;
	char*           shellcodeFilename;
	DWORD           shellcodeSize;
    int             setRegStart[NUM_REGISTERS];
    int             setRegEnd[NUM_REGISTERS];
    struct FileInfo readFiles;
    struct FileInfo writeFiles;
    struct FileInfo readWriteFiles;
    struct FileInfo loadedLibraries;
};

void usage(void) {
    printf("Usage: shellcode_launcher.exe\n");
	printf("shellcode_launcher.exe -i <shellcode_filename> -o <offset> -ba <base_address> [-bp] [-r <in_filename>]\n   [-w <in_filename>] [-L <lib_name] [-<reg>][+<reg>]\n");
    printf("  <shellcode_filename> is the binary containing the shellcode to execute\n");
    printf("  <offset> is the (decimal) offset into the shellcode to start executing\n");
	printf("  <base_address> is your preferred base address to insert the shellcode (i.e. 0xFD0000\n");
    printf("  <in_filename> is an additional file to open, either readonly (-r) \n");
    printf("     or writeable (-w), such as for a malicious PDF the shellcode\n");
    printf("     requires an open handle for\n");
    printf("  -<reg>: load register <reg> with a pointer to the start of the shellcode\n");
    printf("  +<reg>: load register <reg> with a pointer to the end of the shellcode\n");
    printf("  -bp: add a breakpoint prior to jumping into the shellcode\n");
	printf("  -L <lib_name>: Load library <libname> during initialization\n");
}

// Returns TRUE (1) if string s1 is equal to string s2
int isStrEqual(const char *s1, const char*s2) {
    return (0 == strncmp(s1, s2, strlen(s2)));
}

// Validates that there is an additional argument by examining argc & the 
// current argv index. If it is missing, prints a message using the given
// argFlag to format the message, prints usage, and exits.
void checkExtraArgument(int argc, int currI, char* argFlag) {
    if((currI+1) >= argc) {
        printf("Missing argument to %s", argFlag);
        usage();
        exit(1);
    }
}

// For the given source string, checks if it starts with the desired
// '+' or '-' character given in plusMinus. If so, normalizes the case
// and then compares the remainder of the string against all of hte
// Returns -1 if this fails, else returns the REG_X index value for the
// found register.
int isRegisterCommand(const char *source, char plusMinus) {
    char localSource[MAX_REG_NAME_SIZE];
    unsigned int i;
    if(!source) {
        return -1;
    }
    if(source[0] != plusMinus) {
        return -1;
    }
    size_t len = strlen(source);
    if(len > MAX_REG_NAME_SIZE) {
        return -1;
    }
    memset(localSource, 0, sizeof(localSource));
    for(i=0; i<len; i+=1) {
        localSource[i] = (char)tolower(source[i+1]);
    }
    for(i=0; i<REG_MAX; i++) {
        //if(isStrEqual(localSource, regNames[i])) {
        if(!strcmp(localSource, regNames[i])) {
            //found a match, return the current reg index
            return i;
        }
    }
    //if got here, no matches
    return -1;
}

// Returns -1 on error, else 0 on success
int doLoadLibraries(struct ConfigurationData* config) {
    int i;
    for(i=0; i<config->loadedLibraries.index; i++) {

        printf("Trying to LoadLibrary: %s\n", config->loadedLibraries.names[i]);
        HMODULE libHandle = LoadLibrary(config->loadedLibraries.names[i]);
        if(libHandle == NULL) {
            printf("Error loading library %s: 0x%08\n", config->loadedLibraries.names[i], GetLastError());
            return -1;
        }
        config->loadedLibraries.handles[i] = libHandle;
    }
    return 0;
}

int doCreateFiles(struct ConfigurationData* config) {
    int i;
    //open read-only files
    for(i=0; i<config->readFiles.index; i++) {
        HANDLE inFile = INVALID_HANDLE_VALUE;
        printf("Opening readable file: %s\n", config->readFiles.names[i]);
        inFile = CreateFile(config->readFiles.names[i], GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
        if (inFile == INVALID_HANDLE_VALUE) {
            printf("Couldn't open file %s: %08x\n", config->readFiles.names[i], GetLastError());
            return 1;
        }
        config->readFiles.handles[i] = inFile;
    }

    for(i=0; i<config->writeFiles.index; i++) {
        printf("Opening writeable file: %s\n", config->writeFiles.names[i]);
        HANDLE inFile = CreateFile(config->writeFiles.names[i], GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
        if (inFile == INVALID_HANDLE_VALUE) {
            printf("Couldn't open file %s: %08x\n", config->readFiles.names[i], GetLastError());
            return 1;
        }
        config->writeFiles.handles[i] = inFile;
    }

    for(i=0; i < config->readFiles.index; i++) {
        printf("Opening read-writeable file: %s\n", config->readWriteFiles.names[i]);
        HANDLE inFile = CreateFile(config->readWriteFiles.names[i], GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
        if (inFile == INVALID_HANDLE_VALUE) {
            printf("Couldn't open file %s: %08x\n", config->readFiles.names[i], GetLastError());
            return 1;
        }
        config->readWriteFiles.handles[i] = inFile;
    }

    return 1;
}

//return -1 on error, else #of bytes written
int doSetupShellcodeJump(unsigned char* buffer, DWORD dataOffset, DWORD shellcodeOffset, DWORD startOff) {
    int amtWritten = (sizeof(jmp32bitOffset) + sizeof(DWORD));
    DWORD jumpOffset = (EXTRA_SPACE+startOff)-dataOffset;
    //subtract the size of the jump instruction
    jumpOffset -= amtWritten;

    memcpy(buffer + dataOffset, jmp32bitOffset, sizeof(jmp32bitOffset));
    DWORD* jumpTarget = (DWORD*)(buffer+dataOffset+sizeof(jmp32bitOffset));

    //store the jump offset
    //printf("Writing 0x%08x:0x%08x\n", jumpTarget, jumpOffset);
    *jumpTarget = jumpOffset;

    return amtWritten;
}

//allocates the fills the buffer with dat
//returns -1 on failure, else 0 on success
//allocated outBuffer 
int createShellcodeBuffer(struct ConfigurationData* config, unsigned char** outBuffer) {
    if(!outBuffer) {
        printf("ERROR: no output buffer specified\n");
        return -1;
    }
	HANDLE inFile = CreateFile(config->shellcodeFilename, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (inFile == INVALID_HANDLE_VALUE) {
		printf("Couldn't open shellcode-containing file %s: %08x\n", config->shellcodeFilename, GetLastError());
		return -1;
	}
	config->shellcodeSize = GetFileSize(inFile, NULL);
	if(config->shellcodeSize == INVALID_FILE_SIZE) {
		printf("Couldn't get file size\n");
		return -1;
	}
	if(config->startOff > config->shellcodeSize) {
		printf("Execution offset larger than file size!\n");
		return -1;
	}
	if(config->baseAddress) {
        config->baseAddress -= EXTRA_SPACE; 
	}

    //extra space for extra pieces
	unsigned char* buffer = (unsigned char*)VirtualAlloc((PVOID) config->baseAddress, config->shellcodeSize + EXTRA_SPACE, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

	if(buffer == NULL) {
		printf("Couldn't allocate %d bytes\n", config->shellcodeSize);
		return -1;
	}
	DWORD bytesRead = 0;
	if(!ReadFile(inFile, (buffer+EXTRA_SPACE), config->shellcodeSize, &bytesRead, NULL)) {
		printf("Couldn't read file bytes\n");
		return -1;
	}
    //keep an open handle to shellcode file in case the shellcode looks for the open handle
    //CloseHandle(inFile);

	if(bytesRead != config->shellcodeSize) {
		printf("Only read %d of %d bytes!\n", bytesRead, config->shellcodeSize);
		return -1;
	}
    *outBuffer = buffer;

    return 0;
}

//set the specified register to a value just prior to the shellcode
int doSetRegStart(unsigned char*buffer, DWORD currOffset, DWORD shellcodeOffset, int regIndex) {
    printf("Setting reg start: %08x %08x %d\n", currOffset, shellcodeOffset, regIndex);
    int totalCopied = 0;
    //copy call $
    memcpy(buffer+currOffset, callNext, sizeof(callNext));
    totalCopied += sizeof(callNext);
    //copy pop register
    printf("Setting pop %d at 0x%08x\n", regIndex, currOffset+totalCopied);
    buffer[currOffset+totalCopied] = popRegInstr[regIndex];
    totalCopied += sizeof(popRegInstr[0]);

    //calculate immed value to add to reg to point to start of shellcode
    DWORD immed = shellcodeOffset - (currOffset + sizeof(callNext));
    //copy the add reg 32-bit immed instr
    memcpy(buffer+currOffset+totalCopied, addRegImmediate[regIndex], sizeof(addRegImmediate[0]));
    totalCopied += sizeof(addRegImmediate[0]);
    DWORD* immedTarget = (DWORD*)(buffer + currOffset + totalCopied);
    *immedTarget = immed;
    totalCopied += sizeof(DWORD);

    return totalCopied;
}


//set the specified register to a value at the end of the shellcode
int doSetRegEnd(unsigned char*buffer, DWORD currOffset, DWORD shellcodeOffset, int regIndex, int shellcodeSize) {
    printf("Setting reg end: %08x %08x %d\n", currOffset, shellcodeOffset, regIndex);
    int totalCopied = 0;
    //copy call $
    memcpy(buffer+currOffset, callNext, sizeof(callNext));
    totalCopied += sizeof(callNext);
    //copy pop register
    buffer[currOffset+totalCopied] = popRegInstr[regIndex];
    totalCopied += sizeof(popRegInstr[0]);

    //calculate immed value to add to reg to point to start of shellcode
    DWORD immed = shellcodeSize + shellcodeOffset - (currOffset + sizeof(callNext));
    //copy the add reg 32-bit immed instr
    memcpy(buffer+currOffset+totalCopied, addRegImmediate[regIndex], sizeof(addRegImmediate[0]));
    totalCopied += sizeof(addRegImmediate[0]);
    DWORD* immedTarget = (DWORD*)(buffer + currOffset+totalCopied);
    *immedTarget = immed;
    totalCopied += sizeof(DWORD);

    return totalCopied;
}

//set the specified register to a value at the end of the shellcode
int doSetBp(unsigned char*buffer, DWORD currOffset) {
    printf("Creating breakpoint at: 0x%08x\n", (unsigned int)(buffer + currOffset));
    memcpy(buffer + currOffset, breakpoint, sizeof(breakpoint));

    return sizeof(breakpoint);
}

//returns -1 on failure, else 0 on success
int fillPreambleBuffer(struct ConfigurationData* config, unsigned char* buffer, DWORD shellcodeOffset) {
    //okay, start filling in the preamble bytes
    DWORD dataOffset = 0;
    DWORD amtWritten = 0;
    int i = 0;

    if(!config || !buffer) {
        printf("ERROR: bad args to fillPreambleBuffer\n");
    }
    
    //for each entry n the setRegStart & setRegEnd arrays, add
    for(i=0; i<REG_MAX; i++) {
        if(config->setRegStart[i]) {
            amtWritten = doSetRegStart(buffer, dataOffset, shellcodeOffset, i);
            if(amtWritten<0) {
                printf("Error during doSetRegStart\n");
                return -1;
            }
            dataOffset += amtWritten;
        }

        if(config->setRegEnd[i]) {
            amtWritten = doSetRegEnd(buffer, dataOffset, shellcodeOffset, i, config->shellcodeSize);
            if(amtWritten<0) {
                printf("Error during doSetRegEnd\n");
                return -1;
            }
            dataOffset += amtWritten;
        }
    }

    //add breakpoint if requested
    if(config->doBp) {
        amtWritten = doSetBp(buffer, dataOffset);
        if(amtWritten < 0) {
            printf("Error during doSetBp\n");
            return -1;
        }
        dataOffset += amtWritten;
    }


    //setup jump to shellcode location
    return doSetupShellcodeJump(buffer, dataOffset, shellcodeOffset, config->startOff);
}

// Fills in the provided ConfigurationData config struct from the provided command line parameters.
// Returns -1 on error, else success
int parseCommandLineArgs(int argc, char** argv, struct ConfigurationData* config) {

    int i = 1;
    int regIndex;

    while(i < argc) {
        if (isStrEqual(argv[i], "-i")) {
            checkExtraArgument(argc, i, "-i");
            config->shellcodeFilename = argv[i+1];
            i += 2;
        } else if (isStrEqual(argv[i], "-o")) {
            char *endOfString = NULL;
            config->startOff = strtoul(argv[i+1], &endOfString, 0);
            printf("Using starting offset: 0x%08x (%d)\n", config->startOff, config->startOff);
            i += 2;
		} else if (isStrEqual(argv[i], "-ba")) {
            char *endOfString = NULL;
            config->baseAddress = strtoul(argv[i+1], &endOfString, 0);
            printf("Using base address: 0x%08x (%d)\n", config->baseAddress, config->baseAddress);
            i += 2;
        } else if (isStrEqual(argv[i], "-bp")) {
            config->doBp = 1;
            i += 1;
        } else if (isStrEqual(argv[i], "-x")) {
            //orange: i forget why i wanted -x
            i += 1;
        } else if (isStrEqual(argv[i], "-L")) {
            checkExtraArgument(argc, i, "-L");
            int index = config->loadedLibraries.index;
            if(index < MAX_OPEN_FILES) {
                config->loadedLibraries.names[index] = argv[i+1];
            }
            config->loadedLibraries.index += 1;

            i += 2;
        } else if(isStrEqual(argv[i], "-r")) {
            checkExtraArgument(argc, i, "-r");
            if(config->readFiles.index < MAX_OPEN_FILES) {
                config->readFiles.names[config->readFiles.index] = argv[i+1];
                config->readFiles.index += 1;
            } else {
                printf("ERROR: Too many -r files specified. Limit is %d\n", MAX_OPEN_FILES);
                return -1;
            }
            i += 2;
        } else if(isStrEqual(argv[i], "-w")) {
            checkExtraArgument(argc, i, "-w");
            if(config->writeFiles.index < MAX_OPEN_FILES) {
                config->writeFiles.names[config->writeFiles.index] = argv[i+1];
                config->writeFiles.index += 1;
            } else {
                printf("ERROR: Too many -w files specified. Limit is %d\n", MAX_OPEN_FILES);
                return -1;
            }
 
            i += 2;
        } else if(isStrEqual(argv[i], "-rw")) {
            checkExtraArgument(argc, i, "-rw");

            if(config->readWriteFiles.index < MAX_OPEN_FILES) {
                config->readWriteFiles.names[config->readWriteFiles.index] = argv[i+1];
                config->readWriteFiles.index += 1;
            } else {
                printf("ERROR: Too many -rw files specified. Limit is %d\n", MAX_OPEN_FILES);
                return -1;
            }
            i += 2;
 

        } else if( (regIndex = isRegisterCommand(argv[i], '-')) >= 0) {
            //make sure there isn't confliching +/- for same register
            if(config->setRegEnd[regIndex]) {
                printf("ERROR: conflicting +/- requests for register %s\n", regNames[regIndex]);
                usage();
                return -1;
            }
            //set the flag for the given regiser
            printf("Setting %d -%s\n", regIndex, regNames[regIndex]);
            config->setRegStart[regIndex] = 1;
            i += 1;
        } else if( (regIndex = isRegisterCommand(argv[i], '+')) >= 0) {
            //make sure there isn't confliching +/- for same register
            if(config->setRegStart[regIndex]) {
                printf("ERROR: conflicting +/- requests for register %s\n", regNames[regIndex]);
                usage();
                return -1;
            }
            //set the flag for the given regiser
            printf("Setting %d +%s\n", regIndex, regNames[regIndex]);
            config->setRegEnd[regIndex] = 1;
            i += 1;
        } else {
            printf("WARNING: unknown flag: %s. Skipping\n", argv[i]);
            i += 1;
        }
    }
    return 0;
}

int main(int argc, char* argv[]) {
	printf("Starting up\n");
    struct ConfigurationData config;
	if(argc < 3) {
		usage();
	    return 1;	
	}
    memset(&config, 0, sizeof(struct ConfigurationData));
    if(parseCommandLineArgs(argc, argv, &config) < 0) {
        return 1;
    }
    
    //load required libraries
    if(doLoadLibraries(&config) < 0) {
        printf("Load Libraries failed. Exiting\n");
        return 1;
    }
    if(doCreateFiles(&config) < 0) {
        printf("Creat auxiliary files failed. Exiting\n");
        return 1;
    }

    unsigned char* buffer = NULL;
    if(createShellcodeBuffer(&config, &buffer) < 0) {
        printf("Creating shellcode buffer failed. Exiting\n");
        return 1;
    }

    if(fillPreambleBuffer(&config, buffer, EXTRA_SPACE) < 0) {
        printf("Filling preamble buffer failed. Exiting\n");
        return 1;
    }


    //now call the buffer - does not return
	void_func_ptr callLoc = (void_func_ptr)(buffer);
	printf("Calling file now. Loaded binary at: 0x%08x\n", (unsigned int)(buffer+EXTRA_SPACE));
	callLoc();
	

	return 0;
}

