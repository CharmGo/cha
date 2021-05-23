<?php

// 获取usr的配置信息
function getUsrInfo($usr)
{
    $configPath = './config/' . $usr . '.config';
    $f = fopen($configPath, 'r');
    $content = fread($f, filesize($configPath));
    fclose($f);
    return $content;
}

// 获取usr目录下所有文件
function getUsrDirFile($usr, $file)
{
    if (is_dir($usr)) {
        $files = scandir($usr);
        $rel = array_search($file, $files);
        if ($rel) {
            echo '文件已存在';
            return false;
        } else {
            return true;
        }
    }
}
// getUsrDirFile('charm','linuxqq_2.0.0-b2-1089_amd64.deb');
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
                echo '文件已存在,不可再次上传';
            } else {
                echo '服务端可以上传';
            }
        } else {
            echo '身份验证不正确';
        }
    } else {
        echo '服务端不存在该usr,不可上传文件';
    }
}

if ($_FILES['uploadFile']['type'] == 'chaPython/client') {
    $usr = $_POST['usr'];
    $filepath = './' . $usr . '/' . $_FILES['uploadFile']['name'];
    if (is_dir($usr) && !is_file($filepath)) {
        echo '正在上传~~'.PHP_EOL;
        move_uploaded_file($_FILES['uploadFile']['tmp_name'], $filepath);
        echo "上传成功";
    }else{
        echo 'usr目录不存在或该文件已上传';
    }
}
