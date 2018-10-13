#coding=utf-8
import os
import sys
import re
import time
reload(sys)
sys.setdefaultencoding('utf-8')

# 指定的正则，或字符串
specify_str = ''
# 指定的目录
specify_dir =  ''

# 所有包含字符串的文件
results = []

# 检查参数是否合法
def check_params():
    global  folders, specify_dir, specify_str
    if len(sys.argv) < 3:
        print '参数不足：python ' + sys.argv[0] + ' your_floder ' + ' specify_str '
        return False

    specify_str = sys.argv[1] 
    if specify_str.strip()=='':
        print '参数为空：需指定要查找的字符串或正则'
        return False

    # 指定的目录
    specify_dir =  sys.argv[2]
    if specify_dir.strip()=='':
        print '参数为空：必须指定查找路径'
        return False

    if  False == os.path.exists(specify_dir): 
        print '参数错误：路径错误'
        return False

    folders = [specify_dir]
    return True

# 遍历所有文件函数
def check_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    # print '--------'
    # print list
    for dir in list:
           path = os.path.join(rootdir,dir)
           if os.path.isfile(path):
              # 处理文件，判断是否是.h或.m文件，如果是，是否包含指定的字符串
              check_file_and_grep_string(path)
           if os.path.isdir(path):
              # print '+++:' + path
              _files.extend(check_all_files(path))
    return _files
    
# 提取字符串函数
def check_file_and_grep_string(int_put_file):
    # 验证文件拓展名是否符合要求
    global results
    fileExtension = os.path.splitext(int_put_file)[1]
    if(fileExtension in ['.h','.m','.mm']):
        regex = re.compile(specify_str)
        # 开始处理文件
        _file = open(int_put_file)
        # 逐行处理
        sub_re_str = '"(.*)"'
        for each in _file:
            strs = regex.findall(str(each))
            if len(strs) > 0:
                for astring in strs:
                    print astring
                    temp_rex = re.compile(sub_re_str)
                    # print temp_rex.findall(astring)
                    content = temp_rex.findall(astring)[0]
                    results.append('"'+ content + '" = "' + content +'";')
    else:
        pass


# 将提取结果写入文件函数
def write_string_to_file():
    global results
    cur_path = os.getcwd()
    out_put_file = cur_path + '/all_string.txt'
    # 去处重复字符串
    # 列表去重:通过set方法进行处理
    results = list(set(results))
    print "共找到:%s个字符串 "% len(results)
    ##写出数据到本地
    # 设置输出文件路径
    sep = '\n'
    out = open(out_put_file, "a")
    for each in results:
        print each
        out.write(each + sep)
    ##关闭连接
    out.close()


# 工作函数
def worker ():
    is_param_ok = check_params();
    if is_param_ok:
        check_all_files(specify_dir)
        if len(results) > 0:
            write_string_to_file()
            print '✅处理完成，共处理%s'%len(results) + '个字符串'
        else:
            print '⚠️ 未找到符合要求的字符串'

time1=time.time()
worker()
time2 = time.time()
print u'总共耗时：' + str(time2 - time1) + 's'
