#!/bin/bash

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
    #如果文件夹不存在，创建文件夹
    if [ ! -d "en" ]; then
        mkdir en
        mv *.vtt ./en
    fi
done
