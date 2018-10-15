#coding=utf-8
import os
import sys
import re
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def distinct_strings():
    cur_path = os.getcwd()
    in_put_path = cur_path + '/confict_string.txt'
    out_put_path = cur_path + '/distinct_string.txt'

    # 如果文件不存在不作处理
    if  False == os.path.exists(in_put_path): 
    	print 'confict_string.txt 文件不存在'
    	return

    in_put_file = open(in_put_path)
    # 读取原文件内容
    soruce_strings = []
    for each in in_put_file:
    	soruce_strings.append(str(each))

    # 读取完成，关闭文件
    in_put_file.close()

    # 利用Set去重
    print '去重前个数%s' % len(soruce_strings)
    distinct_strings = list(set(soruce_strings))
    print '去重后个数%s' % len(distinct_strings)

    # 打印那些被去除掉的重复字符串
    abadan_strings = list(set(soruce_strings).difference(set(distinct_strings)))
    print '-----被去除的重复string----'
    print abadan_strings
    print '-----被去除的重复string----'

    # 写入文件
    out_put_file = open(out_put_path, 'w+')
    for each in distinct_strings:
        out_put_file.write(each)
    ##关闭连接
    out_put_file.close()


# 执行脚本
print '💪开始处理文件...'
distinct_strings()
print '✅文件处理完成...'



	