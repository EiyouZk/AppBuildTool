# -*- coding: utf-8 -*-
import optparse
import os
import sys
import getpass
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import date, time, datetime, timedelta
import sys
import codecs
reload(sys)
sys.setdefaultencoding( "utf-8" )


#配置文件路径
commendPath = '/Users/' + getpass.getuser() + '/'    
commendFinderName = 'Project'    
commendFullPath = commendPath + commendFinderName    
configFileName = 'paBuildPyConfigFile.json'             
commendFilePath = commendPath + configFileName
codePath = None     
#工程名
#targetName = None

#scheme
#targetName = None
schemeName = None

#临时文件夹名称 
tempFinder = None
#远程地址 包括git地址或者svn地址
remotePath = None
#checkout后的本地路径

#主路径
mainPath = None  # www 文件夹
#证书名
#certificateName = None
certificateName = None
#账户信息
svnUser = None
svnPassword= None

#Cordova工程参数
proFinderName = None
packageName = None
projectName = None

#描述文件
profileName = None
profileUuid = None

#判断是否是workspace
isWorkSpace = False

#版本
tag = 'master'

#钥匙链相关
keychainPath='~/Library/Keychains/login.keychain'

commonplugin = ['cordova-plugin-brightness','cordova-plugin-camera','cordova-plugin-gli-clipboard','cordova-plugin-compat','cordova-plugin-file','cordova-plugin-file-transfer','cordova-plugin-inappbrowser','cordova-plugin-network-information','cordova-plugin-statusbar','cordova-plugin-whitelist','https://github.com/EiyouZk/cordova-plugin-update-app.git','https://github.com/EiyouZk/cordova-plugin-pictures.git','https://github.com/EiyouZk/cordova-plugin-glifile.git'，'cordova-plugin-media']
    # ,'https://github.com/EiyouZk/cordova-plugin-wechatsdk.git','https://github.com/EiyouZk/cordova-plugin-alipay.git'

#输出路径，输出文件名
ipaPath = None

#存放archive文件路径
archiveFile = None


#显示已有的参数
def showParameter():
    print 'remotePath                 :%s'%remotePath
    print 'certificateName            :%s'%certificateName
    print 'svnUser                    :%s'%svnUser
    print 'proFinderName              :%s'%proFinderName
    print 'packageName                :%s'%packageName
    print 'projectName                :%s'%projectName
    print 'profileName                :%s'%profileName
    print 'profileUuid                :%s'%profileUuid
    print 'svnPassword                :%s'%svnPassword
    print 'schemeName                 :%s'%schemeName
    print 'projectName                :%s'%projectName
    
#设置参数
def setParameter():
    global tempFinder
    global mainPath
    global remotePath
    global certificateName
    global svnUser
    global proFinderName
    global packageName
    global projectName
    global profileName
    global svnPassword
    global codePath
    global projectName
    global schemeName
    global profileUuid
    # 工程名 新建不可缺
    if isNone(projectName):
        projectName = raw_input('input projectName:')    
    if isNone(remotePath):
        remotePath = raw_input('input remotePath:')   
    if isNone(certificateName):
        certificateName = raw_input('input certificateName:')    
    if isNone(svnUser):
        svnUser = raw_input('input svnUser:')
    global svnPassword
    if isNone(svnPassword):  
        svnPassword = raw_input('input svnPassword:')
    if isNone(proFinderName):
        proFinderName = raw_input('input proFinderName(cordova工程文件夹名):')
    if isNone(packageName):
        packageName = raw_input('input packageName(包名):')
    if isNone(projectName):
        projectName = raw_input('input projectName(工程名):')
    if isNone(schemeName):
        schemeName = raw_input('input schemeName:')
    if isNone(profileName):
    	profileName = raw_input('input profileName(签名描述文件名):')
    if isNone(profileUuid):
    	profileUuid = raw_input('input profileUuid(描述文件uuid):')

    #保存到本地
    writeJsonFile()

def setBuildParam():
    global mainPath
    global projectName
    global schemeName
    global profileUuid
    global profileName
    if isNone(mainPath):
    	mainPath = raw_input('input projectPath(输入ios工程所在路径):')
    if isNone(projectName):
    	projectName = raw_input('input projectPath(输入ios项目文件名):')
    if isNone(schemeName):
    	schemeName = raw_input('input projectPath(输入ios项目scheme名):')
    if isNone(profileName):
    	profileName = raw_input('input profileName(签名描述文件名):')
    if isNone(profileUuid):
    	profileUuid = raw_input('input profileUuid(描述文件uuid):')
    
#判断字符串是否为空
def isNone(para):
    if para == None or len(para) == 0:
        return True
    else:
        return False
    
#是否需要设置参数
def isNeedSetParameter():
    if isNone(remotePath) or isNone(projectName) or isNone(proFinderName) or isNone(packageName) or isNone(projectName) or isNone(schemeName):
        return True

    else :
        return False
        

#参数设置
def setOptparse():
    createConfigfile()
    p = optparse.OptionParser()
    #参数配置指令
    p.add_option("--config","-c",action="store_true", default=None,help = "config User's data")
    options,arguments = p.parse_args()
    #配置信息
    if options.config == True and len(arguments) == 0 :
        configMethod()

   
#配置信息 
def configMethod():
    os.system('clear')
    readJsonFile()
    print '您的参数如下:'
    print '************************************'
    showParameter()
    print '************************************'
    setParameter()
    # sys.exit()
    
#设置配置文件路径
def createConfigfile():
    if os.path.isfile(commendFilePath):
    	if raw_input('自动打包配置文件已经存在，是否继续使用配置文件的打包参数(y/n)：') == 'n':
	    	os.remove(commendFilePath)
	    	os.system('touch %s'%(commendFilePath))
	        initJsonFile()        
    else:
    	os.system('touch %s'%(commendFilePath))
        initJsonFile()

    return
    
#初始化json配置文件
def initJsonFile():
    fout = open(commendFilePath,'w')
    js = {}
    js['remotePath']        = None
    js['certificateName']   = None
    js['svnUser']           = None
    js['svnPassword']           = None
    js['proFinderName']     = None
    js['packageName']       = None
    js['projectName']       = None
    js['profileName']       = None
    js['profileUuid']       = None
    js['tempFinder']        = None
    js['mainPath']          = None
    js['svnPassword']       = None
    js['codePath']          = None
    js['schemeName']        = None
    js['projectName']       = None
    outStr = json.dumps(js,ensure_ascii = False)
    fout.write(outStr.strip().encode('utf-8') + '\n')
    fout.close()
    
#读取json文件
def readJsonFile():
    fin = open(commendFilePath,'r')
    for eachLine in fin:
        line = eachLine.strip().decode('utf-8')
        line = line.strip(',')
        js = None
        try:
            js = json.loads(line)
            global tempFinder
            global mainPath
            global remotePath
            global certificateName
            global svnUser
            global svnPassword
            global proFinderName
            global packageName
            global projectName
            global profileName
            global profileUuid
            global svnPassword
            global schemeName
            global codePath
            if isNone(remotePath):
                remotePath = js['remotePath']
            if isNone(certificateName):
                certificateName = js['certificateName']
            if isNone(svnUser):
                svnUser = js['svnUser']
            if isNone(proFinderName):
                proFinderName = js['proFinderName']
            if isNone(packageName):
                packageName = js['packageName']
            if isNone(projectName):
                projectName = js['projectName']
            if isNone(profileName):
            	profileName = js['profileName']
            if isNone(profileUuid):
            	profileUuid = js['profileUuid']
            # tempFinder = js['tempFinder']
            if isNone(schemeName):
                schemeName = js['schemeName']
            if isNone(mainPath):
              mainPath = js['mainPath']
            if isNone(svnPassword):
                svnPassword = js['svnPassword']
            if isNone(codePath):
                codePath = js['codePath']
            if isNone(projectName):
                projectName = js['projectName']
        except Exception,e:
            print Exception
            print e
            continue
    fin.close()
    
#写json文件
def writeJsonFile():
    showParameter()
    try:
        fout = open(commendFilePath,'w')
        js = {}
        js['remotePath'] = remotePath
        js['certificateName'] = certificateName
        js['svnUser'] = svnUser
        js['proFinderName'] = proFinderName
        js['packageName'] = packageName
        js['projectName'] = projectName
        js['profileName'] = profileName
        js['tempFinder'] = tempFinder
        js['mainPath'] = mainPath
        js['svnPassword'] = svnPassword
        js['codePath'] = codePath
        js['schemeName'] = schemeName
        js['projectName'] = projectName
        js['profileUuid'] = profileUuid
        outStr = json.dumps(js,ensure_ascii = False)
        fout.write(outStr.strip().encode('utf-8') + '\n')
        fout.close()
    except Exception,e:
        print Exception
        print e
        
#删除文件夹
def rmoveFinder(path):
    os.system('rm -r -f %s'%path)
    return
    
#创建文件夹
def createFileFinder(path):
    os.system('mkdir %s'%path)
    return
    
#对文件夹授权
def allowFinder(path):
    os.system('sudo chmod -R 777 %s'%path)
    return
    
#查找文件
def scan_files(directory,postfix):
    print directory
    files_list=[]
    for root, sub_dirs, files in os.walk(directory):
        for special_file in sub_dirs:
            if special_file.endswith(postfix):
                files_list.append(os.path.join(root,special_file))    
    return files_list
  
#判断文件夹是否存在
def isFinderExists():
    return os.path.exists(mainPath)

#clone工程
def gitClone():
    global codePath
    print codePath
    if 'svn' in remotePath:
        os.system ('svn checkout %s --username=%s --password=%s %s'%(remotePath,svnUser,svnPassword,codePath))
    else:
        os.system ('git clone %s %s --depth 1'%(remotePath,codePath))
    return
    
#显示所有版本
def gitShowTags():
    os.system('clear')
    readJsonFile()
    print '所有的版本'
    print mainPath
    print '************************************'
    os.system ('cd %s;git tag'%mainPath)
    print '************************************'
    sys.exit()

#pull工程
def gitPull():
    os.system('cd %s;git reset --hard;git pull'%mainPath)
    return
   
#设置版本 
def setGitVersion(version):
    if len(version)>0:
        os.system('cd %s;git reset --hard;git checkout %s'%(mainPath,version))
    return
    
#回到主版本
def setGitVersionMaster():
    setGitVersion('master')
    return
 
#clean工程   
def cleanPro():
    os.system('cd %s;xcodebuild clean -configuration "Release" -alltargets'%(mainPath))
    return

#清理pbxproj文件
def clearPbxproj():
    global all_the_text
    path = '%s/%s.xcodeproj/project.pbxproj'%(mainPath,targetName)

    file_object = open(path)
    try:
        all_the_text=file_object.readlines()
        for text in all_the_text:
            if 'PROVISIONING_PROFILE' in text:
                all_the_text.remove(text)
    finally:
        file_object.close()
       
    file_object = open(path,'w')
    try:
        for text in all_the_text:
            file_object.write(text)
    finally:
        file_object.close()
    return

def allowKeychain():
    # User interaction is not allowed
    # os.system("security unlock-keychain -p '%s' %s"%(svnPassword,keychainPath))
    os.system("security unlock-keychain -p '%s' %s" %(svnPassword,keychainPath)) 
    return

#编译获取.app文件和dsym
def buildApp():
    print "p389",mainPath,projectName,schemeName,certificateName,profileUuid
    # os.system("cd %s;xcodebuild archive -project  ./%s.xcodeproj -scheme %s -configuration Release -archivePath archive/%s.xcarchive CODE_SIGN_IDENTITY='%s' PROVISIONING_PROFILE='%s' "%(mainPath,projectName,schemeName,projectName,certificateName,profileUuid))
    os.system("cd %s;xcodebuild archive -project  ./%s.xcodeproj -scheme %s -configuration Release -archivePath archive/%s.xcarchive"%(mainPath,projectName,schemeName,projectName))
 
    if raw_input('输出archive文件完成，是否继续？(输入‘n’退出)：') == 'n':
    	sys.exit()
    
    return
    
#创建ipa
def cerateIPA():
    print "p400",mainPath,projectName
    if os.path.exists('%s/%s.ipa'%(mainPath,projectName)):
 		if raw_input('工程ipa文件存在，是否删除并继续？(输入‘n’退出)：') == 'n':
 			sys.exit()
 		else:
 			os.remove('%s/%s.ipa'%(mainPath,projectName))

    # os.system ('cd %s;xcodebuild -exportArchive -archivePath archive/%s.xcarchive -exportPath %s -exportFormat ipa －exportProvisioningProfile %s '%(mainPath,projectName,projectName,profileName))
    os.system ('cd %s;xcodebuild -exportArchive -archivePath archive/%s.xcarchive -exportPath %s -exportFormat ipa'%(mainPath,projectName,projectName))

    printMsg('导出ipa完成')
    return
    
#上传
def uploadToFir():
    httpAddress = None
    if os.path.exists('%s/%s.ipa'%(mainPath,targetName)):
        ret = os.popen("fir p '%s/%s.ipa' -T '%s'"%(mainPath,targetName,svnUser))
        for info in ret.readlines():
            if 'Published succeed' in info:
                httpAddress = info
                print httpAddress
                break
    else:
        print '没有找到ipa文件'
    return httpAddress
        
#发邮件给测试不带附件
def sendEmail(text):
    if not os.path.exists('%s/%s.ipa'%(mainPath,targetName)):
        print '没有找到ipa文件'
        return
    msg = MIMEText('地址:%s'%text,'plain','utf-8')
    msg['to'] = packageName
    msg['from'] = proFinderName
    msg['subject'] = '新的测试包已经上传'
    try:
        server = smtplib.SMTP()
        server.connect(profileName)
        server.login(proFinderName,projectName)
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        print '发送成功'
    except Exception, e:  
        print str(e)
    return
    
#定时任务
def runTask(func, day=0, hour=0, min=0, second=0):
  # Init time
  now = datetime.now()
  strnow = now.strftime('%Y-%m-%d %H:%M:%S')
  print 'now:',strnow
  # First next run time
  period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
  next_time = now + period
  strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
  print 'next run:',strnext_time
  while True:
      # Get system current time
      iter_now = datetime.now()
      iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
      if str(iter_now_time) == str(strnext_time):
          # Get every start work time
          print 'start work: %s' % iter_now_time
          # Call task func
          func()
          print 'task done.'
          # Get next iteration time
          iter_time = iter_now + period
          strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
          print 'next_iter: %s' % strnext_time
          # Continue next iteration
          continue

    
def setVersion():
    global tag
    setGitVersion(tag)
    return

#判断是否是workspace
def checkWorkSpace():
    global isWorkSpace
    if os.path.exists('%s/%s.xcworkspace'%(mainPath,targetName)):
        isWorkSpace = True
    else:
        isWorkSpace = False
    return

def createProject():
    global commendFullPath
    global proFinderName
    global mainPath
    global codePath    
    print '\033[1;33;40m'
    print '*' * 50
    print '准备创建cordova工程...'
    print '*' * 50
    os.system ('cd %s;sudo cordova create %s %s %s'%(commendFullPath, proFinderName,packageName,projectName))
    commendFullPath = commendFullPath + '/' + proFinderName
    codePath = commendFullPath+'/www'
    print commendFullPath
    allowFinder(commendFullPath)
    printMsg('准备获取最新代码...')
    if raw_input('是否继续(y/n)：') == 'n':
        sys.exit()

    if os.path.exists(codePath):
        rmoveFinder(codePath)
    createFileFinder(codePath)
    gitClone()

    mainPath = commendFullPath + '/platforms/ios' 

    printMsg('准备添加基本插件...')
    if raw_input('是否继续(y/n)：') == 'n':
        sys.exit()

    for pluginname in commonplugin:
        try:
            addPlugin(pluginname)
        except Exception as err:
            printMsg('插件％s加载失败'%(pluginname))
        finally:
            printMsg('继续添加插件')

    pluginname = raw_input('是否需要添加cordova，如果时输入插件名，否者键入Enter即可(y/n)：')
    while pluginname != '' or  pluginname == 'n':
        addPlugin(pluginname)
        pluginname = raw_input('是否继续添加cordova 插件，如果是输入插件名，否者键入Enter即可(y/n)：') 


    printMsg('准备创建cordova ios项目工程')
    if raw_input('是否继续(y/n)：') == 'n':
        pass   
    else:
    	os.system ('cd %s;sudo cordova platform add ios --save'%(commendFullPath))
        printMsg('cordova androd平台所需配置如下：')
        os.system ('cd %s;ordova requirements android '%(commendFullPath))


    printMsg('准备创建cordova android项目工程')
    if raw_input('是否继续(y/n)：') == 'n':
        pass    
    else:
    	os.system ('cd %s;sudo cordova platform add android --save'%(commendFullPath))
        printMsg('cordova ios平台所需配置如下：')
        os.system ('cd %s;ordova requirements ios '%(commendFullPath))

    
    allowFinder(commendFullPath)
    
    # 参数设置
    setParameter()
    printMsg('cordova ios 工程创建完成请配置相关信息。')

    return

def printMsg(msg):
    print '\033[1;33;40m'
    print '*' * 50
    print msg
    print '*' * 50

def addPlugin(pluginname):
	global mainPath

	if isNone(mainPath):
		tmpPath = raw_input("请输入cordova工程路径：")
        if '/' == tmpPathm[-1]:
            mainPath = tmpPath+'/platforms/ios'
        elif:
            mainPath = tmpPath+'platforms//ios'

	cordovaProPath = mainPath.replace("/platforms/ios","")
	print commendFullPath
	os.system ('cd %s;sudo cordova plugin add %s --save;sudo cordova prepare'%(cordovaProPath,pluginname))
	allowFinder(cordovaProPath)
	return

# def updateCode():
# 	global codePath
# 	global mainPath
# 	if isNone(mainPath):
# 		mainPath = raw_input("请输入ios工程远程路径：")
# 	codePath = mainPath.replace("/platforms/ios","") + '/www'
    
#     if 'svn' in remotePath:
#     	os.system ('cd %s;svn update'%(codePath))

def updateCode():
	global mainPath
	if isNone(mainPath):
		mainPath = raw_input('请输入ios工程路径')
	codePath = mainPath.replace('/platform/ios','')+'/www'

	if 'svn' in remotePath:
		os.system('cd %s;svn update;cd ..;sudo cordova prepare'%(codePath))


def prepro():
	os.system ('cd %s;open ./%s.xcodeproj;sleep 10;killall Xcode;' %(mainPath,projectName))
    

#主函数
def main():
    # 设置参数
    setOptparse()

    readJsonFile()

    print '\033[1;33;40m'
    print '*' * 50
    print '选择打包类型，0：表示传入svn地址，获取代码，创建cordova工程，输出ipa包；1:表示传入ios 工程地址，包含.xcodeproj文件; 2:表示给项目添加插件,并且打包输出ipa; 3:更新代码，并且打包输出Ipa。'
    print '*' * 50
    types = raw_input('输入操作类型:') 
    if types == '0':
        # 判断是非需要设置参数
        if isNeedSetParameter():
            print '检查所需参数，您需要设置参数,您的参数如下(使用 --config 或者 -c):'
            showParameter()
            sys.exit()
        
        # 创建cordova工程
        createProject()
        if raw_input('准备打包，请查看xcode配置是否完善？(y/n)：') == 'n':
            sys.exit()
    elif types == '1':
        setBuildParam()
    elif types == '2':
    	try:
    		pluginname = raw_input('输入插件名：')
    		setBuildParam()
    		while pluginname != '':
    			addPlugin(pluginname)
    			pluginname = raw_input('是否继续添加cordova 插件，如果是输入插件名，否者键入Enter即可')
    	except:
    		printMsg('添加插件失败，即将退出操作')
    		sys.exit()
    elif types == '3':
    	setBuildParam()
    	updateCode()    	

    # # # 判断是否是workspace
    # # # checkWorkSpace()
    # # # #设置git版本 暂不使用
    # # # # setVersion() 
    # # # #设置文件夹权限
    # allowFinder()
    # # # # allowKeychain()
    # # # #clear pbxproj文件
    # # # # clearPbxproj()

    # 对工程的预处理
    prepro()
    # clean工程
    cleanPro()
    # # # #编译
    buildApp()
    # # # #生成ipa文件
    cerateIPA()
    # # 上传到fir.im
    # # httpAddress = uploadToFir()
    # # 发邮件给测试
    # # if not isNone(httpAddress):
    #    # sendEmail(httpAddress)

    return

main()
