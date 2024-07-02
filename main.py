import sys
import requests
import json
import re
import os
import urllib.parse
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm  # 导入tqdm

def save_page(book_id, sulg, path, cookies=None):
    try:
        headers = {'Cookie': cookies} if cookies else {}
        docsdata = requests.get(
            f'https://www.yuque.com/api/docs/{sulg}?book_id={book_id}&merge_dynamic_data=false&mode=markdown',
            headers=headers, timeout=10
        )
        if docsdata.status_code != 200:
            print("文档下载失败 页面可能被删除 ", book_id, sulg, docsdata.content)
            return
        docsjson = json.loads(docsdata.content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(docsjson['data']['sourcecode'])
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

def get_book(url="https://www.yuque.com/burpheart/phpaudit", cookies=None):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    headers = {'Cookie': cookies} if cookies else {}
    try:
        docsdata = session.get(url, headers=headers, timeout=10)
        data = re.findall(r"decodeURIComponent\(\"(.+)\"\)\);", docsdata.content.decode('utf-8'))
        docsjson = json.loads(urllib.parse.unquote(data[0]))
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return

    list = {}
    temp = {}
    md = ""
    table = str.maketrans('\/:*?"<>|\n\r', "___________")
    if not os.path.exists(f"download/{docsjson['book']['id']}"):
        os.makedirs(f"download/{docsjson['book']['id']}")

    for doc in tqdm(docsjson['book']['toc'], desc="Downloading Documents", unit="doc"):  # 加入tqdm进度条
        if doc['type'] == 'TITLE' or doc['child_uuid'] != '':
            list[doc['uuid']] = {'0': doc['title'], '1': doc['parent_uuid']}
            uuid = doc['uuid']
            temp[doc['uuid']] = ''
            while True:
                if list[uuid]['1'] != '':
                    if temp[doc['uuid']] == '':
                        temp[doc['uuid']] = doc['title'].translate(table)
                    else:
                        temp[doc['uuid']] = list[uuid]['0'].translate(table) + '/' + temp[doc['uuid']]
                    uuid = list[uuid]['1']
                else:
                    temp[doc['uuid']] = list[uuid]['0'].translate(table) + '/' + temp[doc['uuid']]
                    break
            if not os.path.exists(f"download/{docsjson['book']['id']}/{temp[doc['uuid']]}"):
                os.makedirs(f"download/{docsjson['book']['id']}/{temp[doc['uuid']]}")
            if temp[doc['uuid']].endswith("/"):
                md += "## " + temp[doc['uuid']][:-1] + "\n"
            else:
                md += "  " * (temp[doc['uuid']].count("/") - 1) + "* " + temp[doc['uuid']][temp[doc['uuid']].rfind("/") + 1:] + "\n"
        if doc['url'] != '':
            if doc['parent_uuid'] != "":
                if temp[doc['parent_uuid']].endswith("/"):
                    md += " " * temp[doc['parent_uuid']].count("/") + "* [" + doc['title'] + "](" + urllib.parse.quote(
                        temp[doc['parent_uuid']] + "/" + doc['title'].translate(table) + '.md') + ")" + "\n"
                else:
                    md += "  " * temp[doc['parent_uuid']].count("/") + "* [" + doc['title'] + "](" + urllib.parse.quote(
                        temp[doc['parent_uuid']] + "/" + doc['title'].translate(table) + '.md') + ")" + "\n"
                save_page(str(docsjson['book']['id']), doc['url'],
                          f"download/{docsjson['book']['id']}/{temp[doc['parent_uuid']]}/{doc['title'].translate(table)}.md", cookies)
            else:
                md += " " + "* [" + doc['title'] + "](" + urllib.parse.quote(
                    doc['title'].translate(table) + '.md') + ")" + "\n"
                save_page(str(docsjson['book']['id']), doc['url'],
                          f"download/{docsjson['book']['id']}/{doc['title'].translate(table)}.md", cookies)
            time.sleep(random.randint(1, 4))  # 每次请求后等待1到4秒的随机时间

    with open(f"download/{docsjson['book']['id']}/SUMMARY.md", 'w', encoding='utf-8') as f:
        f.write(md)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        get_book(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        get_book(sys.argv[1])
    else:
        get_book()
