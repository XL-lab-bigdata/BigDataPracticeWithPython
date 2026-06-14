from bs4 import BeautifulSoup
import requests

# 1. 发送请求获取新浪新闻网页HTML
url = "https://news.sina.com.cn/"
response = requests.get(url)

# 2. 尝试使用response.apparent_encoding作为编码方式
response.encoding = response.apparent_encoding

# 3. 检查是否正确解析为UTF-8，如果不是则手动设置为UTF-8
if response.encoding.lower() != 'utf-8':
    response.encoding = 'utf-8'

html_content = response.text

# 4. 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 5. 提取页面标题及其他指定标签内容
page_title = soup.title.string
print("页面标题:", page_title)

# 提取<title>标签的文本内容
title = soup.title.text if soup.title else "未找到 <title> 标签内容"
print("Title:", title)

# 提取<h1>标签的文本内容
h1 = soup.h1.text if soup.h1 else "未找到 <h1> 标签内容"
print("H1:", h1)

# 提取<p>标签的文本内容
p = soup.p.text if soup.p else "未找到 <p> 标签内容"
print("P:", p)

# 提取第一个<a>标签的href属性值
a = soup.a['href'] if soup.a else "未找到 <a> 标签内容"
print("Link:", a)

# 6. 提取第3到第5个链接
all_links = soup.find_all('a')
for index, link in enumerate(all_links[2:5], start=3):  # 从第3个到第5个链接
    href = link.get('href')
    text = link.get_text().strip()
    print(f"链接 {index}: {text}, URL: {href}")

# 7. 使用CSS选择器提取内容 例如，提取 <div class="cheadTopbar"> 下的所有 <a> 标签的文本和链接
content_with_css = soup.select('div.cheadTopbar a')
if content_with_css:
    for content in content_with_css:
        print("通过CSS选择器获取的内容:", content.get_text().strip(), "URL:", content.get('href'))
else:
    print("未找到符合CSS选择器的内容")
