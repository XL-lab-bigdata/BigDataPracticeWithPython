from lxml import etree
from pyquery import PyQuery as pq
import requests

# 发送请求并获取网页内容
url = "https://news.sina.com.cn/"
response = requests.get(url)
# 设置编码方式
response.encoding = response.apparent_encoding
html_content = response.text

# 使用 lxml 解析HTML文档
parser = etree.HTMLParser()
tree = etree.fromstring(html_content, parser)
# 使用 XPath 提取所有新闻标题和链接
titles = tree.xpath('//a/text()')
links = tree.xpath('//a/@href')
# 使用 pyquery 操作 DOM 树，提取特定内容

doc = pq(html_content)
headlines = doc('div.cheadTopbar a')
# 打印 lxml 提取的内容

print("使用 lxml 提取的内容:")
for title, link in zip(titles[:5], links[:5]):
    print(f"标题: {title}, 链接: {link}")
# 打印 pyquery 提取的内容

print("\n使用 pyquery 提取的内容:")
for headline in headlines.items():
    print(f"标题: {headline.text()}, 链接: {headline.attr('href')}")
