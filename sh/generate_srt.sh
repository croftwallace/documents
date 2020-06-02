#!/bin/bash

# Linux命令行工具和Shell都是默认以空格、Tab、回车做为值与值之间的分隔符
# 修改Linux命令行工具和Shell的默认分隔符为 换行符
IFS=$'\n'

#获取当前正在执行脚本的绝对路径
base=$(cd `dirname $0`; pwd)

#echo $base

# 找到当前目录下的文件夹
for f in `find *.mp4 -type f`; do
    echo $f
    #autosub -S zh-CN -D zh-CN -i $f
    autosub -S en -D en -i $f
done

echo 'generate srt finished'
