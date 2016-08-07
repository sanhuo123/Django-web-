#coding=utf-8
import requests
import re
import threading
import time
class link(object):
    def __init__(self):
        self.url=[]
        pass
    def city(self):
        r=requests.get('http://www.grfy.net/index.htm')
        allcity=re.findall('''<li><a href=\"(.*?)">''',r.text)
        self.allcityurl=allcity
        pass
    def citylink(self):
        self.city()
        for i in self.allcityurl:
            url=i+'/sale'
            threading.Thread(target=self.getpage,args=(url,)).start()
        pass
    def getpage(self,url):
        def add(str1):
            url2=re.findall('(http://.*?/sale)',url)
            return ''.join(url2)+'/'+str1
        r=requests.get(url).text
        lists=re.findall('''<div class="list01"><a href="(.*?)" target="_blank">''',r)
        self.url=self.url+map(add,lists)
        func = lambda x,y:x if y in x else x + [y]
        reduce(func, [[], ] + self.url) #去重
        list2=re.findall("<li><a href=\"(.*?)\">[^\d]+</a></li></ul></ul>",r)
        if len(str(list2))>=3:
            r2=re.findall('(http://.*?/sale)',url)
            list2=''.join(r2)+'/'+list2[-1]
            self.getpage(list2)
        else:
            return

        return
class data(object):
    def __init__(self):
        pass
    def getdata(self,url):
        try:
            print '线程开始',threading.active_count()
            page=requests.get(url).text
            name=re.findall('<div id=\"centent\">\s*?<h1>(.*?)</h1>',page)
            num=re.findall('<div class=\"l_fy\">\s*?<p>.*?(\d+)',page)
            times=re.findall(u'发布时间：(.*?)</p>',page)
            money=re.findall(u'<dd><strong>(.*?)</strong>|万元(.*?)</dd>',page)
            many=re.findall(u'<dt>户型面积：</dt>\s+<dd>(.*?)</dd>',page)
            xiaoquming=re.findall(u'<dt>小区名称：</dt>\s+<dd>(.*?)</dd>',page)
            xiaoquadd=re.findall(u'<dt>小区地址：</dt>\s+<dd>(.*?)</dd>',page)
            house=re.findall(u'<dt>房屋概况：</dt>\s+<dd>(.*?)</dd>',page)
            loucen=re.findall(u'<dt>所处楼层：</dt>\s+<dd>(.*?)</dd>',page)
            person=re.findall(u'<dt>联 系 人：</dt>\s+<dd>(.*?)</dd>',page)
            phone=re.findall('''<dd class="redtelphone"><img src="(.*?)"></dd>|<dd class="redtelphone">(.*?)</dd>''',page)
            household=re.findall(u'<h2>房屋概况</h2>\s*?<div class="des">\s*?<strong>([\s\S]+)<div class="cr_bottom_right">',page)
            k=''.join(household)
            k2=re.findall('''(<span.*?">)''', k)
            k3=re.findall('''(<p.*?">)''', k)
            k4=re.findall('''(<div.*?</div>)''', k)
            k5=re.findall('''(<font.*?">)''', k)
            k7=re.findall('''(<b.*?/>)''', k)
            k8=re.findall('''(<ul.*?">)''', k)
            k9=re.findall('''(style=.*?">)''', k)
            k6=re.findall('''data-original="(.*?)"''', page)
            for i in k2:
                k = k.replace(i,'')
            for i in k3:
                k = k.replace(i,'')
            for i in k5:
                k = k.replace(i,'')
            for i in k4:
                k = k.replace(i,'')
            for i in k7:
                k = k.replace(i,'')
            for i in k8:
                k = k.replace(i,'')
            for i in k9:
                k = k.replace(i,'')
            for i in ('</strong>', '<br />','<p>','<br/>','</p>','</span>','</font>','&nbsp;','&nbsp', '</b>','<b>','<strong>','</ul>','<h2 ','<b ','<span>',):
                k = k.replace(i,'')
    #'''import sqlite3             #保存图片到sqllite3
    #    import StringIO
    #    s = StringIO.StringIO()
    #    db = sqlite3.connect('test.db')
    #    cur = db.cursor()

     #   cur.execute("CREATE TABLE if not exists t (b BLOB);")
    #    for imgUrl in k6:
    #        response = requests.get(imgUrl, stream=True)
     #       image = response.content
    #        s.write(image)
     #       with open(s, 'rb') as f:
    #            cur.execute("insert into t values(?)", (sqlite3.Binary(f.read()), ))
     #           db.commit()

     #       cur.execute('select b from t limit 1')
    #        b = cur.fetchone()[0]

    #        with open(s, 'wb') as f:
    #            f.write(b)
    #    db.close()
     #           '''

            if money[1] and phone[0]:
                resulta='名称:'+ ''.join(name)+'  编号：'+''.join(num)+'\r\n发布时间：'+''.join(times)+'\r\n售价：'+ \
                ''.join(money[0])+'万元'+''.join(money[1])+'\r\n户型面积：'+''.join(many)+'\r\n小区名称：'+''.join(xiaoquming)+ \
                '\r\n小区地址：'+''.join(xiaoquadd).replace('-',' ')+'\r\n房屋概况：'+''.join(house)+'\r\n所处楼层：'+''.join(loucen)+ \
                '\r\n联 系 人：'+''.join(person)+'\r\n联系电话:'+''.join(phone[0])+'\r\n概况：'+k+'\r\n房景图:'+' '.join(k6)+'\r\n\r\n'
                print resulta
                filetowrite.write(resulta)
        except:
            if phone[0]:
                resultb='名称:'+ ''.join(name)+'  编号：'+''.join(num)+'\r\n发布时间：'+''.join(times)+'\r\n售价：'+ \
                ''.join(money[0])+'\r\n户型面积：'+''.join(many)+'\r\n小区名称：'+''.join(xiaoquming)+ \
                '\r\n小区地址：'+''.join(xiaoquadd).replace('-',' ')+'\r\n房屋概况：'+''.join(house)+'\r\n所处楼层：'+''.join(loucen)+ \
                '\r\n联 系 人：'+''.join(person)+'\r\n联系电话:'+''.join(phone[0])+'\r\n概况：'+k+'\r\n房景图:'+' '.join(k6)+'\r\n\r\n'
                print resultb
                filetowrite.write(resultb)
        finally:
            print '线程结束',threading.active_count()
            raise(SystemExit)

def main():
    duowan=link()
    #threading.Thread(target=duowan.citylink,args=()).start()        #全国
    threading.Thread(target=duowan.getpage,args=('http://cd.grfy.net/sale',)).start()  #成都
    lpl=data()
    i=0
    time.sleep(3)
    t1=time.time()
    while 1:
        try:
            if len(duowan.url[i])>=3 and len(duowan.url) >= 3 and threading.active_count()<=50:
                threading.Thread(target=lpl.getdata, args=(duowan.url[i], )).start()
                i=i+1
                print threading.active_count(),'----------------------------',len(duowan.url),'-----',i,time.time()-t1
        except:
            if threading.active_count()<2:
                time.sleep(2)
                break
            continue
if __name__ == '__main__':
    filetowrite=open('a.txt', 'wb')
  #  f=open('a.txt','w')
  #  import sys
   # old=sys.stdout #将当前系统输出储存到一个临时变量中
   # sys.stdout=f  #输出重定向到文件
    main()
    filetowrite.close()
   # sys.stdout=old #还原原系统输出
   # f.close()
    print '进程结束！'
