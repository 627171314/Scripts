#!usr/bin/python
#coding=utf-8
#Author Hu Yong

print '#sources文件夹用于存放需要压缩的图片；\n#output 文件夹用于存放压缩后的图片；'
print '#非付费账号每月有500张限额,重复压缩(图片MD5相同)不消耗额度'
print '#如果提示key失效，或达到限额，可前往:https://tinypng.com/developers 生成新的key,仅需30s搞定'
print '#单次压缩可能不是最小尺寸，如需要可进行多次压缩(默认仅进行一次压缩)，在文件大小与显示质量间取舍'
print '###多次压缩需删除原sources文件夹，将上次压缩生成的output文件夹改名为sources文件夹'

import os
import pip
import imp
import sys
import shutil
#import tinify

def install_and_load(package):
    pip.main(['install', package]);
    
    f, fname, desc = imp.find_module(package)
    return imp.load_module(package, f, fname, desc)

try:
    import tinify
except:
    print '自动安装熊猫压缩所需package'
    tinify = install_and_load('tinify')

inputkey = ''
if len(sys.argv) > 1:
    inputkey = sys.argv[1]

if inputkey.strip() != '':
    tinify.key = inputkey
    print '使用自定义key: ',inputkey
else:
    tinify.key = 'DtAaGr774rGlnfp8o1BsYZJ3wOYPotQr'
    print '使用默认key: ',tinify.key

pwd = os.getcwd()
wkpwd = pwd + '/sources'
if(False == os.path.exists(wkpwd)):
    os.makedirs(wkpwd)
    print 'sources文件夹不存在'

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        #fileList.append(dir.decode('gbk'))
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)  
    return fileList
 
list = GetFileList(wkpwd, [])

print '💪开始处理'
total = len(list)
i = 0
totalDecreaseSize = 0
for e in list:
    i += 1
    des = e.replace('/sources','/output')
    father_path = os.path.dirname(des)
    if(False == os.path.exists(father_path)):
        os.makedirs(father_path)
    if('.DS_Store' == os.path.basename(e)):
        print "⏳正在处理(",i,"/",total,"):跳过系统隐藏文件"
        continue
    fileExtension = os.path.splitext(e)[1]
    if(fileExtension not in ['.png','.PNG','.JPG','.JPEG','.jpg','.jpeg']):
        # 把文件拷贝过去
        print "⏳正在处理(",i,"/",total,"):拷贝非图片文件"
        shutil.copyfile(e,des)
        continue;
    originSize = os.path.getsize(e)
    originSize = originSize/float(1024)
    originSize = round(originSize,3)
    print "⏳正在处理(",i,"/",total,"):", os.path.basename(e)," ——",originSize,"K"
    source = tinify.from_file(e)
    source.to_file(des)
    finalSize = os.path.getsize(des)
    finalSize = finalSize/float(1024)
    finalSize = round(finalSize,3)
    decreaseSize = originSize - finalSize
    totalDecreaseSize += decreaseSize
    print "⏳正在保存(",i,"/",total,"):", os.path.basename(des)," ——",finalSize,"K 减少:",decreaseSize,"K"


print '🎉处理完成, 共减少:',totalDecreaseSize,"K"
print '😘当前账号本月免费使用情况:',tinify.compression_count,"/ 500"


