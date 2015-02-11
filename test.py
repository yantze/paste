#!/usr/bin/env python
# encoding: utf-8

import markdown

data = """
title: Git
date: 2014-06-08 09:24
tags: [git, lts]
categories: tools
---

##目录

* 简化工作流程
    * [常用提交流程](#normal_commit)

* 初始化
    * [初始化一个空库](#init)
    * [在本地新建了一个库，同步已经存在的库](#pull_exist)

* 分支
    * [创建新的分支](#branch)
    * [常用分支管理](#branch_manage)
    * [合并分支](#merge)
    * [从远程拿下一个新的分支](#branch_newpull)

* 标签
    * [使用tag上线发布](#tag)
    * [带tag的版本提交](#tag_submit)

* 回滚
    * [常用后悔管理](#regret)
    * [操作记录高级命令](#log)


* Misc
    * [把当前仓库生成压缩文档 - zip](#archive)
    * [bug修复，而当前的工作未完成 - stash](#stash)
    * [git添加ssh key实现无密码提交](#ssl_nopwd)
    * [git实现https方式无密码提交](#https_nopwd)
    * [使用git的代理](#proxy)
    * [优化git结构 - gc](#gc)
    * [忽略指定文件](#ignore)
    * [创建命令别名 - alias](#alias)
    * [查找一个文件中一行的作者](#blame)

* 团队协作——标准工作流程
    * 基本流程
    * 常驻分支：master和develop
    * 临时分支： [feature](#feature),release,hotfix
"""
md = markdown.markdown(unicode(data, 'utf8'),
    extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.abbr',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.fenced_code',
        'markdown.extensions.footnotes',
        'markdown.extensions.tables',
        'markdown.extensions.smart_strong',
        'markdown.extensions.codehilite',
        'markdown.extensions.meta',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smarty',
        'markdown.extensions.toc'
    ])

print md


