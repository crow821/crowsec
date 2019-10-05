<?php

require_once "../../common/common.php";
if (!isset($_SESSION['user'])) {
    header("Location:../login.php");
}
$filter = array(".jpg", '.png', '.gif');

if ($_FILES['file']['error']) {
    die();
}
if ($_FILES['file']) {
    $arr = $_FILES['file'];
    $file_ext = trim(strtolower(strrchr($arr['name'], ".")));

    if (file_exists(TPMELATE."/upload/".$arr['name'])){
        echo "<script>alert('该文件已经存在')</script>";
    } else{
        $filename = iconv("UTF-8","gb2312",TPMELATE."/upload/".$arr['name']);
        move_uploaded_file($arr["tmp_name"],$filename);
        echo $filename;die();
    }
}
require_once TPMELATE."/upload_file_1.html";
