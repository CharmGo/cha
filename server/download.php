<?php

if ($_POST['state'] == 'checkServerUsr') {
    $usr = $_POST['usr'];
    $configPath = './config/' . $usr . '.config';
    $isdir = is_dir($usr);
    $isFile = is_file($configPath);
    if ($isdir == true && $isFile == true) {
        $cliConfig = $_POST['code'];
        $fopen = fopen($configPath, 'r');
        $con = fread($fopen, filesize($configPath));
        if ($con == $cliConfig) {
            $file = './' . $usr . '/' . $_POST['filename'];
            // echo $file;
            if (is_file($file)) {
                // echo 'ok';
                echo filesize($file);
            } else {
                echo '没有该文件';
            }
        } else {
            echo '身份验证不正确';
        }
    } else {
        echo '服务端不存在该usr,不可上传文件';
    }
}




?>