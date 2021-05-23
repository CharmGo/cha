import os
import binascii
import json
import re
import time
import sys


class chaLocal:
    def __init__(self):
        self.__version__ = '1.0.0'
        # 系统类型
        self.osType = os.name
        # 配置文件路径
        self.configPath = None
        # 配置文件状态
        self.configState = False
        # 本地配置文件内容
        self.configContent = ''
        # 服务端配置文件内容
        self.configNetContent = ''
        # 配置文件内容状态
        self.configContentState = False
        # usr状态
        self.usrState = False
        # 指定usr的配置信息
        self.usrContent = ''

        if self.osType == 'posix':
            self.configPath = './chr.config'
        if self.osType == 'windows':
            home = os.environ["HOME"]
            self.configPath = home + '\\document\\Documents\\chr.config'

        # 如果配置文件存在,则读取配置文件内容,如果配置文件内容不为空就使本地配置文件内容状态为True
        if os.path.isfile(self.configPath):
            self.configState = True
        if self.configState:
            with open(self.configPath, 'rb') as f:
                self.configContent = f.read()
        if self.configContent != b'' and self.configContent != '':
            self.configContentState = True

    # 加密函数
    @staticmethod
    def encry(String):
        if type(String) != str:
            try:
                String = str(String)
            except:
                print("String is not str")
                return False
        code = String.encode('utf-8')
        return binascii.b2a_hex(code)

    # 解密函数
    @staticmethod
    def decry(Bytes):
        if type(Bytes) != bytes:
            try:
                Bytes = bytes(Bytes)
            except:
                print("Bytes is not Bytes")
                # return False
        code = binascii.a2b_hex(Bytes)
        return code.decode('utf-8')

    # 处理文件路径
    @staticmethod
    def filterFile(fileName):
        r = re.split('/', fileName)
        return r[-1]
        # print(r)
        # print(r[-1])

    # 检查文件是否存在,返回布尔值
    @staticmethod
    def checkFile(filePath):
        isFile = os.path.isfile(filePath)
        if isFile:
            size = os.path.getsize(filePath)
            if size < 26843545600:
                return True
            else:
                print('文件不可超过25Mb')
                return False
        else:
            print('filePath 必须是一个文件')
            return False

    # 将本地配置文件内容转换成数组形式,如果转换失败则返回False,该函数必须调用
    def ByteConfig2ArrayConfig(self):
        if self.configContentState:
            try:
                self.configContent = chaLocal.decry(self.configContent)
            except:
                print("配置文件出错，请勿修改chr.config文件")
                self.configContent = ''
                self.configContentState = False
                return False
            # print(self.configContent)
            self.configContent = re.split('&', self.configContent)
            return self.configContent.pop()
        # print(self.configContent)
        print("配置文件不存在")

    # 获取所以本地配置文件中已创建的usr
    def getAll(self):
        if self.configContentState:
            print("usr \t\t\t\t time")
            for i in range(len(self.configContent)):
                js = json.loads(self.configContent[i])
                # print(js)
                timeStamp = int(str(js['time']).split('.')[0])
                timeArray = time.localtime(timeStamp)
                creteTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                print(js['usr'], end='')
                print('\t\t\t\t' + creteTime)

    # 检查本地配置文件是否存在usr
    def checkUsr(self, usr):
        if self.configContentState:
            for i in range(len(self.configContent)):
                js = json.loads(self.configContent[i])
                if js['usr'] == usr:
                    self.usrState = True
                    print("本地已存在")
                    return True
            print("本地不存在")
            return False

    # 当检测到usr在本地不存在时,生成本地配置信息,以及服务端配置文件信息
    def generateCode(self, usr):
        # print(self.usrState)
        if not self.usrState:
            prams = {
                'usr': usr,
                'os': self.osType,
                'time': time.time()
            }
            jsonParams = json.dumps(prams)
            self.configContent = chaLocal.encry(jsonParams + '&')
            self.configNetContent = chaLocal.encry(jsonParams)
            # print(self.configContent)
            # print(self.configNetContent)

    # 当本地不存在usr以及服务端返回检测信息服务端不存在usr且将配置信息写入服务端后
    # 使用此函数将配置信息写入配置文件
    def writeConfigFile(self):
        with open(self.configPath, 'ab') as f:
            f.write(self.configContent)

    # 获取本地配置文件中usr的验证信息
    def getUsrInfo(self, usr):
        if self.configContentState:
            # print(self.configContent)
            for i in range(len(self.configContent)):
                js = json.loads(self.configContent[i])
                if js['usr'] == usr:
                    # print(chaLocal.encry(json.dumps(js)))
                    self.usrContent = chaLocal.encry(json.dumps(js))
                    print('本地存在' + usr)
                    # print(chaLocal.encry(json.dumps(js)))
                    self.usrState = True
                    return chaLocal.encry(json.dumps(js))
            print('本地不存在' + usr)

    # 进度条
    @staticmethod
    def prog(filename, size):
        start = time.time()
        getsize = 0
        while size <= getsize:
            getSize = os.path.getsize(filename)
            # print("\r", end="")
            print(getSize+'/'+size)
            # sys.stdout.flush()
            time.sleep(0.05)
        stop = time.time() - start
        print("下载时长:" + str(stop))


if __name__ == '__main__':
    a = chaLocal()
    a.ByteConfig2ArrayConfig()
    # a.getAll()
    # a.checkUsr('charm')
    # a.generateCode('charm')
    # a.getUsrInfo('charm')
    # print(chaLocal.checkFile('./__init__.py'))
    # print(a.filterFile('/usr/abc/asd/__init__.py'))
    a.pro()
