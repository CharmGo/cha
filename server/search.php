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

// 获取usr目录下所以文件

if ($_POST['state'] == 'searchUsr') {
    $usr = $_POST['usr'];
    $usrInfo = $_POST['usrCode'];

    $configPath = './config/' . $usr . '.config';
    $isdir = is_dir($usr);
    $isFile = is_file($configPath);
}

// echo $configPath.PHP_EOL;
if ($isdir == true && $isFile == true) {
    $con = getUsrInfo($usr);
    if ($con == $usrInfo) {
        // echo "ok";
        $list = scandir($usr);
        $count = count($list) - 2;
        if ($count == 0) {
            echo $usr . "没有文件";
        } else {
            echo $usr . "共有" . $count . "个文件" . PHP_EOL;
            echo "filename" . "\t\t\t\t\t" . "size" . PHP_EOL;
            echo "" . PHP_EOL;
            for ($i = 2; $i < $count + 2; $i++) {
                $filename = './' . $usr . '/' . $list[$i];
                echo $list[$i] . "            " . filesize($filename) . PHP_EOL;
            }
        }
    } else {
        echo "身份验证错误,请勿修改配置文件";
    }
} else {
    echo "服务端配置文件不存在";
}
