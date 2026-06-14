import requests
import json
import re
from pyquery import PyQuery as pq
import pandas as pd
from tqdm import tqdm

# 获取新浪主页的各个模块，返回所有模块的名称和链接
def get_all_category_url():
    # 网址
    sina_url = 'https://www.sina.com.cn/'
    # requests.get获取网页源代码
    html = requests.get(sina_url)
    # # 设置编码
    # html.encoding = html.apparent_encoding
    # 尝试设置编码为utf-8，避免乱码
    html.encoding = 'utf-8'
    # PyQuery库解析源代码
    doc = pq(html.text)
    # 根据源代码标签特点来对应解析
    # 获取所需要的网页节点
    lis = doc('.main-nav').find('li')
    url_dict = {}
    for item in lis.items():
        # 获取所需要的网页节点中的网址
        result = item('a').attr('href')
        if len(result) > 0 and result[0:4] == 'http':
            url_dict[item.text()] = result
    # 返回所有模块的名称和链接
    return url_dict

# 获取某个模块内的内容，依据源代码的特点进行解析
def get_category_content(cate_name, all_category_url):
    df = pd.DataFrame()
    # 得到指定模块的url
    url = all_category_url[cate_name]
    # 获取该模块内容的源代码
    html = requests.get(url)
    # 设置编码
    html.encoding = html.apparent_encoding
    # PyQuery库解析源代码
    doc = pq(html.text)
    # 根据源代码解析提取包含所需要内容的网页节点
    # 获取class属性为blk_04的节点中名称为a的子孙节点
    lis = doc('.blk_04').find('a')
    title_list = []
    url_list = []
    time_list = []
    content_list = []
    # 遍历各个节点，解析所需要的属性值（标题，网址，发布时间，发布内容）
    for i in tqdm(range(len(lis))):
        item = list(lis.items())[i]
        try:
            print('这是第%i条,共爬取%i条'%(i,len(lis)))
            url_1 = item.attr('href')
            print(url_1)
            html_1 = requests.get(url_1)
            html_1.encoding = html_1.apparent_encoding
            html = html_1.text

            # title的标签有两种形式
            try:
                title = re.findall('<h1 class="main-title">(.*?)</h1>',html)[0]#item.text()
                print(1)
            except:
                title = re.findall('<title>(.*?)</title>',html)[0]
                print(2)
            time = re.findall('<span class="date">(.*?)</span>',html)[0]
            doc_1 = pq(html)
            content_list_0 = doc_1('#article').find('p')
            content_list_1 = [item.text() for item in content_list_0.items()]
            content = ''.join(content_list_1).replace('\n','')
            title_list.append(title)
            url_list.append(url_1)
            time_list.append(time)
            content_list.append(content)

        # 反爬措施：页面没有找到 5秒钟之后将会带您进入新浪首页!
        except:
            print('失败！页面未找到')
            continue
    df['标题'] = title_list
    df['网址'] = url_list
    df['发布时间'] = time_list
    df['内容'] = content_list
    # 将该模块所有信息储存到csv文件中
    df.to_csv(cate_name+'.csv', encoding = 'gb18030',index = None)
    print(cate_name+' content has been saved in '+cate_name+'.csv successfully!')

def main():
    all_category_url = get_all_category_url()
    print(all_category_url.keys())
    print('*'*100)
    print('请自由选择模块进行内容爬取，此次以"新闻"模块为例:')
    cate_name = '新闻'#以"新闻"模块为例
    get_category_content(cate_name, all_category_url)
    df = pd.read_csv(cate_name+'.csv',encoding = 'gb18030')
    print(df)

main()