import json
import time
import requests
from urlextract import URLExtract
import html2text

# flomo token 和 cookie，通过抓包获取
TOKEN = ''
COOKIE = ''
# md 文件的保存地址
PATH = ''

def my_html_to_markdown(html_str):
    '''
    html_str 字符串转 markdown 字符串
    '''

    extractor = URLExtract()

    # 获取字符串中的所有 URL
    urls = extractor.find_urls(html_str)
    # # 格式化 URL
    for url in urls:

        if(url.find('https://flomoapp') >= 0):
            # flomo 链接
            html_str = html_str.replace(url, '[['+url[url.find('memo_id=')+len('memo_id')+1:len(url)]+']]')
        else:
            # 其他链接
            html_str = html_str.replace(url, '['+url+']('+url+')')

    md_text = html2text.html2text(html_str)

    return md_text


# 获取 flomo 数据
offset = 0
header = {
    'X-XSRF-TOKEN': TOKEN, 'cookie': COOKIE, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://flomoapp.com/mine?', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
while(True):
    req = requests.get(url='https://flomoapp.com/api/memo/?offset=' +
                       str(offset)+'&tz=8:0', headers=header)
    req_json = json.loads(req.text)
    offset += len(req_json['memos'])

    print(offset)

    for item in req_json['memos']:
        html = item['content']

        # 通过 html 获取 md 文本
        md_text = my_html_to_markdown(html)
        # 笔记创建时间
        timeArray = time.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S")
        newtime = time.strftime("%Y%m%d%H%M%S", timeArray)

        # 处理 content 中的标题
        if(item['content'].find('# ') < 0):
            # 如果 MEMO 中原本没有标题

            title = item['slug']
            title += '_'+newtime

        else:
            # 如果 MEMO 中原本有标题：获取标题内容
            start_index = item['content'].find('# ')
            end_index = item['content'].find('</p>', start_index)
            title = item['content'][start_index:end_index]

            title += '_' + item['slug']

            title = title.replace('# ', '', 1)

        md_text = title+'\n\n'+md_text

        # 卡片内的图片
        files = ''
        if(len(item['files'])!=0):
            for img in item['files']:
                files += '![image]'+'('+img['url']+')'
        
        # 图片信息
        md_text +='\n' + files
        # flomo 信息
        md_text +='\n---\n'+'Created in '+'[flomo]'+'(https://flomoapp.com/mine/?memo_id='+item['slug']+') '+item['created_at']
        

        with open(PATH+item['slug']+'.md', 'w', encoding='utf-8') as file:
            file.write(md_text)

    time.sleep(2)

    if(len(req_json['memos']) <= 0):
        break
