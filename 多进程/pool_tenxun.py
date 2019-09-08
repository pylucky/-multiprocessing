
###多进程爬取 腾讯招聘

import requests,time,re,os,json

def get_page(num):
    data={}
    print("当前进程是{},--进程号是{}".format(num,os.getpid()))
    url="https://careers.tencent.com/tencentcareer/api/post/Query?categoryId=40001001,40001002,40001003,40001004,40001005,40001006&pageIndex={}&pageSize=10".format(str(num))
    headers={
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.659377294.1547435949; pgv_pvi=3635187712; loading=agree',
        'referer': 'https://careers.tencent.com/search.html?query=ot_40001001,ot_40001002,ot_40001003,ot_40001004,ot_40001005,ot_40001006&index=2',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    time.sleep(2)
    response=requests.get(url,headers=headers)
    ##标题
    title=re.findall(r'"RecruitPostName":"(.*?)",',response.text)
    ##地点
    location=re.findall(r'"LocationName":"(.*?)",',response.text)
    ##岗位
    types=[]
    for i in title:
        type=i.split("-")[1]
        types.append(type)

    ##工作内容
    content=re.findall(r'"Responsibility":"(.*?)",',response.text)
    ##发布时间
    pub_time=re.findall(r'"LastUpdateTime":"(.*?)",',response.text)
    ##url
    url=re.findall(r'"PostURL":"(.*?)",',response.text)

    ###save
    ##构建json对象
    # for i in range(len(title)):
    #     data["title"]=title[i]
    #     data["location"]=location[i]
    #     data["content"]=content[i].replace('\r\n',"").replace("\\r","").replace("\\n","").strip()
    #     data["pub_time"]=pub_time[i]
    #     data["types"]=types[i]
    #     data["url"]=url[i]
    #     ##json存贮
    #     with open("tenxun.josn","a+",encoding="utf-8")as f:
    #         f.write(json.dumps(data,ensure_ascii=False)+"\n")

    #存MySQL
    for i in range(len(title)):
        s1=title[i]
        s2=location[i]
        s3=types[i]
        s4=url[i]
        s5=content[i]
        s6=pub_time[i]

        s7=time.localtime()

        from mysqlhelper import  MysqlHelper

        sql="insert into tenxun(title,location,types,url,content,pub_time,crawl_time)value(%s,%s,%s,%s,%s,%s,%s)"
        data=(s1,s2,s3,s4,s5,s6,s7)

        mysql = MysqlHelper()
        mysql.execute_modify_sql(sql,data)
        time.sleep(0.01)
        print("---------插入成功 ------------")

if __name__=="__main__":
    # start=time.time() 300页
    # get_page()
    # end=time.time()
    # print("共耗时{:.0f}秒".format(end-start))

    ###开启多进程
    from multiprocessing import Pool
    start=time.time()
    pool = Pool(8)
    # 创建进程
    # ###让进程 循环多少次，把分页num 放入进程对象
    for num in range(1,300):
        res=pool.apply_async(func=get_page,args=(num,))
    pool.close()
    pool.join()
    ##保存结果
    end=time.time()
    print("共耗时{:.0f}秒".format(end-start))
