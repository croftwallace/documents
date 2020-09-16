#!/bin/bash

# bash 脚本赋值等号两边不能留空格
# Linux命令行工具和Shell都是默认以空格、Tab、回车做为值与值之间的分隔符
# 修改Linux命令行工具和Shell的默认分隔符为 换行符
IFS=$'\n'

#获取当前正在执行脚本的绝对路径
base=$(cd `dirname $0`; pwd)

#echo $base

# 找到当前目录下的文件夹
for d in `find . -type d`; do
    echo $d
    cd $base
    cd $d
    for f in `find *.srt -type f`; do
        echo '-->' >> $f
    done
    #如果文件夹不存在，创建文件夹
    if [ ! -d "en" ]; then
        mkdir en
        #mv *.vtt ./en
        mv *.srt ./en
    fi
done
cd $base
rm -r ./en
echo 'move finished'
