<?php
// 检查服务端是否存在usr,检查条件:usr,
// 判断依据:config下是否存在$usr.config以及是否存在$usr目录
// 若都不存在则可以创建,否则不能创建
if ($_POST['state'] == 'checkServerUsr') {
    $usr = $_POST['usr'];
    $configPath = './config/' . $usr . '.config';
    $isdir = is_dir($usr);
    $isFile = is_file($configPath);
    if ($isdir == false && $isFile == false) {
        echo '服务端可以创建';
    } else {
        echo '服务端已存在,不可创建';
    }
}

if ($_POST['state'] == 'createServerUsr') {
    $usr = $_POST['usr'];
    $configCode = $_POST['configCode'];

    $ismkdir = mkdir($usr);
    if ($ismkdir) {
        $configPath = './config/' . $usr . '.config';
        // echo $configPath . PHP_EOL;
        try {
            $f = fopen($configPath, 'w');
            fwrite($f, $configCode);
            echo "创建成功";
        } catch (Exception $e) {
            $ferror = fopen('./error.log', 'a');
            fwrite($ferror, $e->getMessage());
            fclose($ferror);
            echo "创建配置文件失败";
        }
        fclose($f);
    } else {
        echo "创建项目失败";
    }
}

