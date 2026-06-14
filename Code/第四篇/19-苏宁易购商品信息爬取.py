# -*- coding: UTF-8 -*-
import requests
import codecs
import json
from bs4 import BeautifulSoup
import urllib3
import xlwt
from tqdm import tqdm

def column(col_num):
        if col_num == 0:
            col_num = 1
        else:
            col_num = 0
        return col_num

# 创建工作表，设定文字颜色等格式
work_book = xlwt.Workbook(encoding='utf-8')
sheet = work_book.add_sheet('sheet0', cell_overwrite_ok=True)
r_style = "font:colour_index red;"
red_style = xlwt.easyxf(r_style)
b_style = "font:colour_index blue;"
blue_style = xlwt.easyxf(b_style)

# 取消警告
requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings()
session = requests.session()

# 访问苏宁易购网站关键词的搜索界面 获取所有商品的店铺和商品ID得到列表每个元素为一个元组（店铺-商品，商品名称）
searchUrl = 'https://search.suning.com/emall/searchV1Product.do?keyword={keyword}&pg=01&paging={page}'
idList = []

# 获取苏宁易购“电视机”搜索结果第一页的所有商品信息
for page_num in range(1, 2):
    print("第%s页商品列表获取" %(page_num))
    config = {
     'keyword': '电视机',
     'page': page_num
    }
    # 获取源代码 requests.get
    r = session.get(searchUrl.format(**config), verify=False)
    # 设定编码
    r.encoding = 'UTF-8'
    # 解析源代码 BeautifulSoup
    searchHtml = BeautifulSoup(r.text, 'lxml')# 解析源代码
    productHtml_list = searchHtml.find_all('li', attrs={'doctype': '1'})
    print('该页共%i个商品'%len(productHtml_list))

    # 遍历所需网页节点进行信息抽取
    for productHtml in productHtml_list:
        # 获取评论数
        comment_num = 0
        if productHtml.find('div', attrs={'class': 'info-evaluate'}) is not None:
                comment_num = productHtml.find('div', attrs={'class': 'info-evaluate'}).find('i').get_text()
        # 获取商品id, 商品标题，评论数,存入idList中
        tub = (productHtml['id'], productHtml.find('a')['title'], comment_num)
        idList.append(tub)
print("开始爬取商品属性信息")

row_num = 0  # xls行数
currentCol = 1  # 列号标记
good_num = 0  # 商品个数记录
page_xls = 1

# 遍历获取到的list对象,每个商品都去获取它的商品信息
for tub in tqdm(idList[:10]):
    print("row_num：%s   page_xls：%s" % (row_num, page_xls))
    if row_num/15000 >= 1:
        sheet = work_book.add_sheet('sheet'+str(page_xls), cell_overwrite_ok=True)
        row_num = 0
        currentCol = 1  # 列号标记
        page_xls += 1
    good_num += 1

    # 分割shopID 和商品ID
    listTub = tub[0].split('-')
    shopId = listTub[0]
    proId = listTub[1]
    print("shopId：%s   proId：%s" % (shopId, proId))
    currentCol = column(currentCol)
    sheet.write(row_num, currentCol, shopId, red_style)
    currentCol = column(currentCol)
    sheet.write(row_num, currentCol, proId, red_style)
    sheet.write(row_num, 2, good_num, red_style)
    sheet.write(row_num, 4, tub[1], red_style)
    parameter = {
        'productId': proId.zfill(18),
        'shopId': shopId,
    }
    sheet.write(row_num, 7, tub[2], red_style)
    # 访问每个商品的详情界面
    baseUrl = 'http://product.suning.com/{shopId}/{productId}.html'.format(**parameter)
    sheet.write(row_num, 3, baseUrl, red_style)
    row_num += 1


    session = requests.session()
    with codecs.open('jsonGoodData.txt', 'a+', encoding='utf-8') as f:
        while True:
            try:
                print(baseUrl)
                r = session.get(baseUrl)
                r.encoding = 'UTF-8'
                proHtml = BeautifulSoup(r.text, 'lxml')
                tables = proHtml.findAll('table')
                # print(tables)
                # 找到包装参数和其他参数的相关table 提取参数
                tab = proHtml.find(id='bzqd_tag')
                tab2 = proHtml.find(id='itemParameter')
                if tab is not None:
                    for tr in tab.findAll('tr'):
                        num = 0
                        for td in tr.findAll('td'):
                            if td.getText() != '':
                                currentCol = column(currentCol)
                                sheet.write(row_num, currentCol, td.getText())
                                if num % 2 != 0:
                                    row_num += 1
                                num += 1
                                f.write(td.getText() + '\n')
                if tab2 is not None:
                    for tr in tab2.findAll('tr'):
                        for th in tr.findAll('th'):
                            if th.getText() != '':
                                currentCol = column(currentCol)
                                sheet.write(row_num, currentCol, th.getText(), blue_style)
                                row_num += 1
                                f.write(th.getText() + '\n')
                                currentCol = 1
                        num = 0
                        for td in tr.findAll('td'):
                            if td.getText() != '':
                                currentCol = column(currentCol)
                                sheet.write(row_num, currentCol, td.getText())
                                if num % 2 != 0:
                                    row_num += 1
                                num += 1
                                f.write(td.getText() + '\n')
            except Exception as e:
                print(e)
                continue
            break
    print("row_num：%s   page_xls：%s" % (row_num, page_xls))
work_book.save('苏宁易购商品信息表(演示demo).xls')



