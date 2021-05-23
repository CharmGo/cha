import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests_toolbelt.multipart import encoder


class chaNet:
    def __init__(self):
        # 网络请求地址
        self.urlz = ''
        self.url_create = self.urlz+'create.php'
        self.url_search = self.urlz+'search.php'
        self.url_upload = self.urlz+'upload.php'
        self.url_download = self.urlz+'download.php'
        # 网络状态
        self.netState = False
        # 服务端配置状态
        self.serverConfigState = False
        # 服务端创建usr的状态
        self.serverCreatedState = False
        # 下载的文件大小
        self.fileSize = 0
        # 检查网络状态
        try:
            r = requests.post(self.url_create)
            self.netState = r.status_code
        except IOError:
            self.netState = False

    # 检查网络状态,状态为200则检查服务端是否存在usr,如果不存在就返回可以创建,
    # 如果存在就返回不可创建,同时使服务端配置状态为True,
    # 当服务端配置文件状态为False时才能进行下一步
    def checkNetUser(self, usr):
        if not self.netState:
            print("网络错误")
            return False
        elif self.netState != 200:
            "连接服务端状态 " + str(self.netState)
            return False
        else:
            # 网络正常
            prams = {
                'state': 'checkServerUsr',
                'usr': usr
            }
            response = requests.post(self.url_create, prams)
            serverConfigState = response.text
            print(serverConfigState)
            if serverConfigState != '服务端可以创建':
                self.serverConfigState = True
                # print(self.serverConfigState)
                return False

    # 当服务端配置文件状态为False时调用此函数,将usr以及身份信息传递至服务端
    # 如果服务端创建成功则将服务端配置文件状态和服务端创建usr状态设为True
    def createServerUsr(self, usr, code):
        if not self.netState:
            print("网络错误")
            return False
        elif self.netState != 200:
            "连接服务端状态 " + str(self.netState)
            return False
        else:
            # 网络正常
            if not self.serverConfigState:
                prams = {
                    'state': 'createServerUsr',
                    'usr': usr,
                    'configCode': code
                }
                r = requests.post(self.url_create, prams)
                print(r.text)
                if r.text == '创建成功':
                    self.serverConfigState = True
                    self.serverCreatedState = True
                    # print("ok")

    # 搜索所有文件
    def searchNet(self, usr, code):
        if not self.netState:
            print("网络错误")
            return False
        elif self.netState != 200:
            "连接服务端状态 " + str(self.netState)
            return False
        else:
            # 网络正常
            prams = {
                'state': 'searchUsr',
                'usr': usr,
                'usrCode': code
            }
            # print(prams)
            response = requests.post(self.url_search, prams)
            print(response.text)

    # 上传文件前服务端对usr以及文件进行检查
    def checkUsrAndFile(self, usr, filename, code):
        if not self.netState:
            print("网络错误")
            return False
        elif self.netState != 200:
            "连接服务端状态 " + str(self.netState)
            return False
        else:
            # 网络正常
            prams = {
                'state': 'checkServerUsr',
                'usr': usr,
                'filename': filename,
                'code': code
            }
            response = requests.post(self.url_upload, prams)
            serverConfigState = response.text
            print(serverConfigState)
            if serverConfigState == '服务端可以上传':
                self.serverConfigState = True
                # print(self.serverConfigState)
                return True

    # 文件上传
    def uploadFile(self, usr, filename):
        m = MultipartEncoder(
            fields={
                'usr': usr,
                'uploadFile': (filename, open(filename, 'rb'), 'chaPython/client')}
        )
        try:
            print('正在上传~~')
            r = requests.post(self.url_upload, data=m, headers={'Content-Type': m.content_type})
        except:
            print('文件不宜过大')
        print(r.text)

    def checkDownload(self, usr, filename, code):
        if not self.netState:
            print("网络错误")
            return False
        elif self.netState != 200:
            "连接服务端状态 " + str(self.netState)
            return False
        else:
            # 网络正常
            prams = {
                'state': 'checkServerUsr',
                'usr': usr,
                'filename': filename,
                'code': code
            }
            response = requests.post(self.url_download, prams)
            serverConfigState = response.text
            # print(serverConfigState)
            try:
                if type(int(serverConfigState)) == int:
                    self.serverConfigState = True
                    self.fileSize = int(serverConfigState)
                    # print(self.serverConfigState)
                    return True
            except ValueError:
                print(serverConfigState)
                return False

    @staticmethod
    def download(usr, filename, downPath='./'):
        url = 'https://www.ujfdolu.cn/chr/' + usr + '/' + filename
        try:
            r = requests.post(url, stream=True)
            state = r.status_code
        except IOError:
            print('网络错误')
            return False
        if state == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
            print('下载成功')
        else:
            print('连接服务器状态:' + str(state))
            return False


if __name__ == '__main__':
    a = chaNet()
    # a.checkNetUser('charm')
    # a.createServerUsr('???', 'hello')
    # a.searchNet('charms', 'hello')
    # a.checkUsr('charm')
    # a.uploadFile('charm','test.deb')
    a.download('charm', 'test.deb')
