import requests
import re
from jinja2 import Template

# 获取热搜数据


def get_hot_search():

    response = requests.get('https://s.weibo.com/top/summary', headers={
        "Cookie":
        "SUB=_2AkMWJrkXf8NxqwJRmP8SxWjnaY12zwnEieKgekjMJRMxHRl-yj9jqmtbtRB6PaaX-IGp-AjmO6k5cS-OH2X9CayaTzVD",
    })

    hot_search = re.findall(
        r'<a href="(\/weibo\?q=[^"]+)".*?>(.+)<\/a>', response.text)
    hot_search_result = []
    for search_item in hot_search:
        hot_search_result.append({
            'url': search_item[0],
            'title': search_item[1]
        })

    return hot_search_result

# 生成 HTML 文件


def generate_html(hot_search):
    template = Template('''
    <head>
    <title>微博热搜 - 热门话题排行榜</title>
    <meta name="description" content="查看微博上的热门话题排行榜。">
    <meta name="keywords" content="微博,热搜,热门话题,排行榜">
    <style>
    body {
        font-family: Arial, sans-serif;
        font-size: 16px;
        background-image: url('./static/background.jpg');
        background-size: cover;
        background-position: center;
    }
    h1 {
        text-align: center;
        margin-top: 40px;
        color: white;
        text-shadow: 2px 2px 4px #000000;
        font-size: 36px;
        font-weight: bold;
    }
    ul {
        list-style-type: none;
        padding: 0;
        margin: 40px auto;
        width: 80%;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }
    li {
        width: 30%;
        margin-bottom: 20px;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.8);
        text-align: center;
        border-radius: 10px;
        box-shadow: 2px 2px 4px #000000;
        color: black;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.5s;
    }
    li:hover {
        transform: scale(1.1);
        box-shadow: 4px 4px 8px #000000;
        cursor: pointer;
    }
    </style>
    </head>
    <body>
        <h1>微博热搜</h1>
        <div>
        <ul>
        {% for item in hot_search %}
            <li><a href='https://s.weibo.com/{{ item.url }}'>{{ item.title }}</a></li>
        {% endfor %}
        </ul>
        </div>
    </body>
    </html>
    ''')
    html = template.render(hot_search=hot_search)
    with open('hot_search.html', 'w', encoding='utf-8') as f:
        f.write(html)


# 运行程序
hot_search = get_hot_search()
generate_html(hot_search)
