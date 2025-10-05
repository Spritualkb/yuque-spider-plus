# 新版本的具备有gui
https://github.com/Spritualkb/yuque-spider-gui

# yuque-spider-plus

该项目基于https://github.com/burpheart/yuque-crawl项目进行修改

语雀文档抓取工具（爬虫） 可以保存任意用户整个语雀知识库为Markdown格式 (包含完整目录结构和索引) 

![](./assets/yuque-demo.png)

使用：
安装 python3

https://www.python.org/downloads/

执行安装运行模块

```shell
pip install requests tqdm urllib3
```

执行抓取：

`python3 main.py 语雀文档地址`

demo：
`python3 main.py https://www.yuque.com/burpheart/phpaudit`



## 2024/07/03

### 增加需要密码需要设置cookie功能爬取

把浏览器全部cookie值复制到指定设置

命令行 

示例 1：提供 URL 和 Cookie

```shell
python main.py "https://www.yuque.com/burpheart/phpaudit" --cookie "verified_books=****"
```


示例 2：提供 URL、Cookie 和输出路径

```python
python main.py "https://www.yuque.com/burpheart/phpaudit" --cookie "verified_books=****" --output "download"
```


示例 3：仅提供 URL

```shell
python main.py "https://www.yuque.com/burpheart/phpaudit"
```

示例 4：提供 URL 和输出路径

```shell
python main.py "https://www.yuque.com/burpheart/phpaudit" --output "download"
```


示例 5：使用默认参数（显示帮助信息）

```shell
python main.py
```



## 2024/07/04

### 网络图片本地观看

修复出现部分图片无法本地加载的情况，把网络图片下载下来并把markdown对应的图片路径替换为相对路径的./assets路径下

## 2024/09/27

### 实现批量url笔记爬取

从input.txt读取对应链接和cookie
链接和cookie以逗号分隔



### 执行命令

python main.py --input input.txt --output D:\Notebook







