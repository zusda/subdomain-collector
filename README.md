# subdomain-collector
## 前言

个人用的一个子域名收集。

为了避免重复造轮子，就直接做成了几个子域名收集工具的集合工具。

fofa和google的功能改写自水泽子域名扫描器。


想过弄的通用点，弄过架构那样，弄成命令自定义然后自定义处理函数文件啥的分离开来。但是懒死了，目前这几个工具涵盖的子域名搜集方法很全了，就这样了。
觉得可以就给个star。

## 使用配置：

1.自己的机子去安装esd、ksubdomain、amass以及运行后报错提示缺少的库

2.subdomain_fofa去添加自己的email和key

3.google的代理部分修改成自己的代理（能直连就去掉代理）

## 使用：

```python
python3 subdomain_collector.py -d {domain} -o result.txt
```

执行的命令如下

```python
commands=[
    'esd -d {domain};mv /tmp/esd/.{domain}.esd ./esd_subdomain.txt',
    'ksubdomain e  -d {domain}  | tee ksubdomain.txt',
    'amass enum -v -d {domain} -o amass.txt -passive;mv amass.txt amass_subdomains.txt',
    'python3 EnumGoogle.py -d {domain}',
    'python3 subdomain_fofa.py -d {domain}'
]
```



## 执行效果与流程：

测试环境是kali

每条命令开一个窗口。

然后将每个窗口的结果文件（上面commands产生的文件）进行整理、去重、合并到result文件。







