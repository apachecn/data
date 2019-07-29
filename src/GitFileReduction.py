#!/usr/bin/python
# coding: utf-8
import os
import subprocess

# 查询大文件
shell = """
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"
"""
exitcode, output = subprocess.getstatusoutput(shell)
print("exitcode: ", exitcode)
print("output: ", type(output), output)

for i in output.split("\n"):
    filename = i.split(" ")[1]
    print(filename)
    # 删除大文件记录
    shell = """
    git filter-branch -f --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch %s' --tag-name-filter cat -- --all
    """ % filename
    print(shell)
    exitcode, output = subprocess.getstatusoutput(shell)
    print(">>> ", exitcode)

# 提交代码
shell = "git push origin --force --all"
print(shell)
exitcode, output = subprocess.getstatusoutput(shell)
print(">>> ", exitcode)
