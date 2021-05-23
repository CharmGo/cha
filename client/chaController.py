# 控制器
import chaLocal as local
import chaNet as net
import fire


# 获取本地所以usr
def getUsrAll():
    l = local.chaLocal()
    l.ByteConfig2ArrayConfig()
    l.getAll()


# 搜索usr在服务端的文件,搜索条件,本地配置文件中usr的身份信息与服务端一致
def searchUsrFile(usr):
    l = local.chaLocal()
    l.ByteConfig2ArrayConfig()
    l.getUsrInfo(usr)
    if l.usrContent != '':
        # print(l.usrContent)
        n = net.chaNet()
        n.searchNet(usr, l.usrContent)


# 创建usr
def createUsr(usr):
    l = local.chaLocal()
    l.ByteConfig2ArrayConfig()
    l.checkUsr(usr)
    l.generateCode(usr)
    # print(l.configContent)
    # print(l.configNetContent)
    if not l.usrState:
        n = net.chaNet()
        n.checkNetUser(usr)
        # print(n.serverConfigState)
        if not n.serverConfigState:
            n.createServerUsr(usr, l.configNetContent)
            # print(n.serverConfigState)
            # print(n.serverCreatedState)
            if n.serverConfigState == True & n.serverCreatedState == True:
                l.writeConfigFile()


# 上传文件:检查上传的文件是否符合条件,再检查本地usr是否存在,
# 存在即将usr验证信息上传至服务端验证,如果服务端存在且usr验证信息一致
# 则返回验证结果
def uploadFile(usr, FilePath):
    l = local.chaLocal()
    if l.checkFile(FilePath):
        l.ByteConfig2ArrayConfig()
        l.getUsrInfo(usr)
        # print(l.usrContent)
        # print(l.usrState)
        if l.usrState:
            n = net.chaNet()
            fileName = l.filterFile(FilePath)
            n.checkUsrAndFile(usr, fileName, l.usrContent)
            if n.serverConfigState:
                # print(n.serverConfigState)
                n.uploadFile(usr, fileName)


# 下载文件
# 确认验证信息->返回下载链接->下载
def downFile(usr, fileName):
    l = local.chaLocal()
    l.ByteConfig2ArrayConfig()
    l.getUsrInfo(usr)
    # print(l.usrContent)
    # print(l.usrState)
    if l.usrState:
        n = net.chaNet()
        FileName = l.filterFile(fileName)
        n.checkDownload(usr, FileName, l.usrContent)
        if n.serverConfigState:
            print("将下载" + str(n.fileSize / 1232896) + ' M')
            n.download(usr, FileName)


if __name__ == '__main__':
    # getUsrAll()
    # createUsr('charm')
    # searchUsrFile('charm')
    # uploadFile('charm','./__init__.py')
    fire.Fire({
        'all': getUsrAll,
        'create': createUsr,
        'search': searchUsrFile,
        'up': uploadFile,
        'down': downFile
    })
    # uploadFile('xdy', 'test.py')
    # downFile('charm', 'test.deb')
