# 从爬虫到电子书

以简书的个人文集为例

## 简要步骤

确认目录结构 >
分析网页结构 >
稳定访问目标网络 >
下载至本地 >
本地文件打包 >
电子书格式处理
.

## 具体步骤

### 目录结构

最常见的结构:
目录页 >
内容页

目前简书翻页形式为无限滚动, 为简化分析过程, 直接从目录页提取全部内容页链接, 另存为 `*_url.txt`

提取链接方法: 打开目录页 `https://www.jianshu.com/c/${example}`, 按住键盘 `End` 载入所有目录, 右键 Inspect Element, 复制 `.note-list` 的 Inner HTML;
在编辑器中通过正则表达式查找替换, 并补全网址前缀.

### 网页结构

有用的部分有三个:

- 标题
- 内容
- 评论

坚持使用 `re` 一把梭.

评论部分由于 js 异步载入, 因此暂不导入.

### 网络请求

先用自己电脑 Firefox 上取得的 headers 试试.
其他没啥

### 处理文件

#### EPUB: Sigil

`/Text` 导入 html;
`/Images` 导入图片

#### MOBI: KindleGen 

压缩图片, 黑白化  
[后补]

压制 `.mobi`
`kindlegen filename.epub -c2 –verbose -dont_append_source`
