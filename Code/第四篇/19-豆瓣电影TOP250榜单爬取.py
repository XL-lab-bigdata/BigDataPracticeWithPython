import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义基础URL
BASE_URL = "https://movie.douban.com/top250"

# 发送请求并解析HTML页面
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 确保请求成功
    return BeautifulSoup(response.text, "html.parser")
# 解析页面中的电影信息
def parse_movies(soup):
    movies = []
    items = soup.select("div.item")  # 定位到每部电影的父元素
    for item in items:
        title = item.select_one("span.title").text  # 获取电影标题
        rating = item.select_one("span.rating_num").text  # 获取评分
        quote = item.select_one("span.inq")  # 获取引言
        quote = quote.text if quote else "暂无引言"  # 判断引言是否存在
        link = item.select_one("a")["href"]  # 获取电影详情页链接
        movies.append({"Title": title, "Rating": rating, "Quote": quote, "Link": link})
    return movies

# 递归爬取所有页面
def scrape_top_250():
    all_movies = []
    for i in range(10):  # 循环10次，爬取10页数据
        url = f"https://movie.douban.com/top250?start={i * 25}&filter="  # 动态生成URL
        print(f"正在抓取: {url}")  # 输出当前抓取的页面URL，便于调试
        soup = fetch_page(url)  # 获取页面并解析
        movies = parse_movies(soup)  # 提取电影数据
        all_movies.extend(movies)  # 累积结果
    return all_movies

# 保存数据到CSV文件
def save_to_csv(movies, filename="douban_top_250.csv"):
    df = pd.DataFrame(movies)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"数据已保存到 {filename}")

# 主程序入口
if __name__ == "__main__":
    print("正在抓取豆瓣电影 Top 250 数据...")
    movies = scrape_top_250()  # 执行爬取
    save_to_csv(movies)  # 保存结果
    print("抓取完成！")
