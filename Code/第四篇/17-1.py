import requests
# 发送 HTTP GET 请求
response = requests.get('https://homexinlu.com/')
# 输出请求状态码
print('请求状态码:', response.status_code)
# 检查请求状态码，如果状态码不是 200 则抛出异常
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"请求失败: {e}")


# 设置自定义请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
# 发送带有自定义请求头的 GET 请求
response = requests.get("https://homexinlu.com/publ.html", headers=headers)
# 输出请求状态码及异常情况
print('请求状态码：', response)
print('请求状态码是否异常：', response.raise_for_status())
# 确保正确显示网页内容
response.encoding = response.apparent_encoding  # ���ú��ʵı��룬��������
# 展示 HTML 部分内容
print(response.text[1272:1360])