# 一个简单的快速保存文字的网站

网站:
http://paste.sinaapp.com

## 功能
- 使用bucket保存内容
- 使用pygment高亮代码
- 使用markdown转换成网页文件
- 优化显示text纯文本文档
- 优化显示markdown内容,使用github的md样式
- 提交后，自动显示二维码

## 感谢
网站灵感和部分代码来自:sprunge.us

## 便捷方式
上传文件内容，然后根据id自动下载文件内容
```
上传程序:
https://github.com/yantze/dotfiles/blob/master/bin/upaste
下载程序:
https://github.com/yantze/dotfiles/blob/master/bin/dpaste
```

例如:
```bash
upaste filename.c  # return xRqH
dpaste xRqH  # return filename.c's content
```
