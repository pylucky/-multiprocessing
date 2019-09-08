import threading
import requests
import time,re,json
from queue import  Queue

class MyThread(threading.Thread):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.659377294.1547435949; pgv_pvi=3635187712; loading=agree',
        'referer': 'https://careers.tencent.com/search.html?query=ot_40001001,ot_40001002,ot_40001003,ot_40001004,ot_40001005,ot_40001006&index=2',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    def __init__(self,task_q,lock):
        ###任务队列
        self.task_q=task_q
        ##锁
        self.lock=lock
        # 找到MyThread的父类然后调用init方法
        super(MyThread, self).__init__()

    def run(self):
        ###队列不为空，获取任务
        while not self.task_q.empty():
            url=self.task_q.get()
            print(url,"----------- q.get 一个url --------------")

            time.sleep(2)
            response = requests.get(url, headers=self.headers)
            ##标题
            title = re.findall(r'"RecruitPostName":"(.*?)",', response.text)
            ##地点
            location = re.findall(r'"LocationName":"(.*?)",', response.text)
            ##岗位
            types = []
            for i in title:
                type = i.split("-")[1]
                types.append(type)

            ##工作内容
            content = re.findall(r'"Responsibility":"(.*?)",', response.text)
            ##发布时间
            pub_time = re.findall(r'"LastUpdateTime":"(.*?)",', response.text)
            ##url
            url = re.findall(r'"PostURL":"(.*?)",', response.text)

            ##save
            ##构建json对象
            # data = {}
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
            ##存MySQL
            """
            多线程存SQL要加锁
            """
            for i in range(len(title)):
                s1 = title[i]
                s2 = location[i]
                s3 = types[i]
                s4 = url[i]
                s5 = content[i]
                s6 = pub_time[i]
                s7=time.localtime()
                from mysqlhelper import MysqlHelper
                sql = "insert into tenxun_thread(title,location,types,url,content,pub_time,crawl_time)value(%s,%s,%s,%s,%s,%s,%s)"
                data = (s1, s2, s3, s4, s5, s6,s7)

                mysql = MysqlHelper()
                ## 锁 ()
                with self.lock:
                    mysql.execute_modify_sql(sql, data)
                    time.sleep(0.01)
                    print("---------插入成功 ------------")


if __name__ == '__main__':
    start=time.time()
    ##lock
    lock=threading.Lock()

    ##初始化任务队列,把任务放入队列里面
    task_q = Queue()
    ##分页数量
    for i in range(1,300):
        base_url = "https://careers.tencent.com/tencentcareer/api/post/Query?categoryId=40001001,40001002,40001003,40001004,40001005,40001006&pageIndex={}&pageSize=10".format(
            str(i))
        task_q.put(base_url)
    ##放线程的list对象
    t_list=[]
    for i in range(1, 20):
        t=MyThread(task_q, lock)
        t.start()
        t_list.append(t)
    ##循环线程对象，join()
    for thread in t_list:
        thread.join()

    end=time.time()
    print("耗时{:.0f}秒".format(end-start))