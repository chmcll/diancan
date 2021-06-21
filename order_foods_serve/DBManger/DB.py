import MySQLdb
import json
from PIL import Image
import time
class DB():
    def __init__(self):
        global database
        global cursor
        database = MySQLdb.connect("localhost", "root", "root", "order_foods", charset='utf8')
        cursor = database.cursor()
    # 登录
    def login(self, name, password, flag):
        table = None
        List = ""
        sid = ""
        if flag == 0:
            table = 'user'
            sql = "select id from " + table + " where name = '" + name + "' and password='" + password + "'"
            cursor.execute(sql)
            List = cursor.fetchall()
        elif flag == 1:
            table = 'business'
            sql = "select id from " + table + " where name = '" + name + "' and password='" + password + "'"
            cursor.execute(sql)
            List = cursor.fetchall()
            sql = "select id from shop where bid='" + str(List[0][0]) + "'"
            cursor.execute(sql)
            sid = cursor.fetchall()[0][0]
        elif flag == 2:
            table = 'manager'
            sql = "select id from " + table + " where name = '" + name + "' and password='" + password + "'"
            cursor.execute(sql)
            List = cursor.fetchall()
        if len(List)==0:
            return {"status": 201}
        else:
            return {"status": 200, "id": List[0][0],"sid":sid}
    # 注册
    def register(self,name,password,type):
        if type==0:
            sql = "select * from user where name = "+"'"+name+"'"
            cursor.execute(sql)
            if len(cursor.fetchall())>0:
                return json.dumps({"status":201})
            else:
                sql = "insert into user (name,password) value ('"+str(name)+"'"+",'"+str(password)+"')"
                cursor.execute(sql)
                return json.dumps({"status":200})
        else:
            sql = "select * from business where name=" + "'" + str(name) + "'"
            cursor.execute(sql)
            if len(cursor.fetchall()) > 0:
                return json.dumps({"status":201})
            else:
                sql = "insert into business (name,password) value ('" + str(name) + "','" + str(password) +"')"
                cursor.execute(sql)
                sql = "select * from business where name='"+name+"'"
                cursor.execute(sql)
                dict = cursor.fetchall()
                sql = "insert into shop (name,cover,qualification,bid) value('杂货店','/static/cover/222.jpeg',''"+",'"+str(dict[0][0])+"')"
                cursor.execute(sql)
                return json.dumps({"status":200})
    # 查询所有店铺
    def queryshop(self,pagenum):
        sql = "select * from shop where qualification !='"+"'"
        cursor.execute(sql)
        shopnum = len(cursor.fetchall())
        sql = "select * from shop limit "+str(pagenum*12)+",12"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict)>0:
            reList.update({"status":"200"})
        else:
            reList.update({"status":"201"})
        for item in dict:
            jsonData = {"id":item[0],"name":item[1],"cover":item[2],"qualification":item[3],"bid":item[4] }
            data.append(jsonData)
        reList.update({"data":data})
        reList.update({"shopnum":shopnum})
        return reList

    # 查询所有店铺
    def queryshopbyid(self, id):
        sql = "select * from shop where id = '"+id+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "cover": item[2], "qualification": item[3], "bid": item[4]}
            data.append(jsonData)
        reList.update({"data": data})
        return reList
    # 查询某商铺所有菜品
    def queryfoods(self,sid,pagenum):
        sql = "select * from foods"
        cursor.execute(sql)
        foodsnum = len(cursor.fetchall())
        sql = "select * from foods where sid = '"+str(sid)+"'"+"limit "+str(pagenum*4)+",4 "
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id":item[0],"name":item[1],"price":item[2],"food":item[3] }
            data.append(jsonData)
        reList.update({"data":data})
        reList.update({"foodsnum":foodsnum})
        return reList
    # 排序查询菜品
    def sortfoodsbyprice(self,sid,pagenum,flag):
        sql = "select * from foods where sid='"+sid+"'"
        cursor.execute(sql)
        foodsnum = len(cursor.fetchall())
        sql = "select * from foods where sid = '"+str(sid)+"'"+"limit "+str(pagenum*4)+",4 "
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id":item[0],"name":item[1],"price":item[2],"food":item[3] }
            data.append(jsonData)
        if data:
            data.sort(key=lambda x: float(x['price']), reverse=flag)
        reList.update({"data":data})
        reList.update({"foodsnum":foodsnum})
        return reList
    # 查询个人信息
    def queryuserinfo(self,id):
        sql = "select * from user where id = '"+str(id)+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        if len(dict)<=0:
            reList = {"status":201}
        else:
            reList = {"status":200,"data":{"name":dict[0][1],"password":dict[0][2]}}
        return reList
    # 修改个人信息
    def updateuserinfo(self,id,name,password):
        sql = "update user set name = '"+str(name)+"',"+"password='"+str(password)+"'where id='"+str(id)+"'"
        cursor.execute(sql)
        return {"status":200}
    # 加入购物车
    def addcart(self,name,price,num,food,fid,uid,sid):
        sql = "select * from cart where uid = '"+str(uid)+"' and fid='"+str(fid)+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        if len(dict)>0:
            if num==0:
                sql = "delete from cart where uid = '"+str(uid)+"' and fid='"+str(fid)+"'"
            else:
                sql = "update cart set name='"+name+"',price='"+str(price)+"',num='"+str(num)+"',food='"+food+"' where fid='"+str(fid)+"' and uid='"+str(uid)+"'"
        else:
            sql = "insert into cart (name,price,num,food,fid,uid,sid) value('"+name+"','"+str(price)+"','"+str(num)+"','"+food+"','"+str(fid)+"','"+str(uid)+"','"+str(sid)+"')"
        cursor.execute(sql)
        return {"status":200}
    # 从购物车删除
    def deletecart(self,fid,uid):
        sql = "delete from cart where uid = '" + str(uid) + "' and fid='" + str(fid) + "'"
        cursor.execute(sql)
        return {"status": 200}
    # 查询某个用户的购物车
    def querycart(self,uid,pagenum):
        sql = "select * from cart where uid='" + str(uid) + "'"
        cursor.execute(sql)
        cartnum = len(cursor.fetchall())
        sql = "select * from cart where uid = '" + str(uid) + "'" + "limit " + str(pagenum * 4) + ",4"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "price": item[2], "num": item[3], "food": item[4],"fid":item[5],"uid":item[6],"sid":item[7]}
            data.append(jsonData)
        reList.update({"data": data})
        reList.update({"cartnum": cartnum})
        return reList
    # 查询商铺名称
    def queryshopname(self,fid):
        sql = "select sid from foods where id='"+str(fid)+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        sql = "select * from shop where id = '"+str(dict[0][0])+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        reList.update({"status":200})
        reList.update({"data":{"sid":dict[0][0],"name":dict[0][1]}})
        return reList
    # 添加订单
    def addorders(self,name,price,num,shopname,address,remarks,food,fid,uid,sid):
        time1 = str(time.localtime(time.time()).tm_year) + "-" + str(time.localtime(time.time()).tm_mon) + "-" + str(
            time.localtime(time.time()).tm_mday)
        totalprice = float(price)*float(num)
        sql = "insert into orders (name,price,num,shopname,address,remarks,food,fid,uid,sid,totalprice,time) value('"+str(name)+"','"+str(price)+"','"+str(num)+"','"+str(shopname)+"','"+str(address)+"','"+str(remarks)+"','"+str(food)+"','"+str(fid)+"','"+str(uid)+"','"+str(sid)+"','"+str(totalprice)+"','"+str(time1)+"')"
        cursor.execute(sql)
        return {"status": 200}
    # 查询用户的订单
    def queryorders(self,uid,pagenum):
        sql = "select * from orders where uid='" + str(uid) + "'"
        cursor.execute(sql)
        ordersnum = len(cursor.fetchall())
        sql = "select * from orders where uid = '" + str(uid) + "'" + "limit " + str(pagenum * 3) + ",3"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "price": item[2], "num": item[3], "shopname": item[4],
                        "address": item[5], "remarks": item[6], "food": item[7], "fid": item[8],"uid":item[9]}
            data.append(jsonData)
        reList.update({"data": data})
        reList.update({"ordersnum": ordersnum})
        return reList
    # 添加地址
    def addaddrsee(self,name,phonenumber,address,uid):
        sql = "insert into address(name,phonenumber,address,uid) value('"+name+"','"+str(phonenumber)+"','"+address+"','"+str(uid)+"')"
        print(sql)
        cursor.execute(sql)
        return {"status": 200}
    # 删除地址
    def deleteaddrsee(self,id):
        sql = "delete from address where id = '"+str(id)+"'"
        cursor.execute(sql)
        return {"status": 200}
    # 通过id查询某一条地址
    def queryaddressbyid(self,id):
        sql = "select * from address where id='"+str(id)+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        jsonData = {"id": dict[0][0], "name": dict[0][1], "phonenumber": dict[0][2], "address": dict[0][3], "uid": dict[0][4]}
        reList.update({"data":jsonData})
        return reList
    # 修改用户地址
    def updateaddrsee(self,id,name, phonenumber, address):
        sql = "update address set name='"+name+"',phonenumber='"+str(phonenumber)+"',address='"+address+"' where id='"+str(id)+"'"
        cursor.execute(sql)
        return {"status": 200}
    # 查询用户所有地址
    def queryaddrsee(self,uid,pagenum):
        sql = "select * from address where uid='"+str(uid)+"'"
        cursor.execute(sql)
        addressnum = len(cursor.fetchall())
        sql = "select * from address where uid = '"+str(uid)+"'"+"limit "+str(pagenum*3)+",3"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id":item[0],"name":item[1],"phonenumber":item[2],"address":item[3],"uid":item[4] }
            data.append(jsonData)
        reList.update({"data":data})
        reList.update({"addressnum":addressnum})
        return reList
    # 查询用户所有地址（不分页）
    def queryaddrseeall(self,uid):
        sql = "select * from address where uid='"+str(uid)+"'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id":item[0],"name":item[1],"phonenumber":item[2],"address":item[3],"uid":item[4] }
            data.append(jsonData)
        reList.update({"data":data})
        return reList
    # 添加评价
    def addevaluate(self,uid,sid,context,grade,datestr,fid):
        sql = "insert into evaluate (uid,sid,context,grade,time,fid) value ('"+str(uid)+"'"+",'"+str(sid)+"','"+context+"','"+str(grade)+"','"+datestr+"','"+str(fid)+"')"
        cursor.execute(sql)
        return {"status": 200}
    # 查询用户姓名（内部方法，非接口）
    def queryusername(self,uid):
        sql = "select name from user where id ='"+str(uid)+"'"
        cursor.execute(sql)
        return str(cursor.fetchall()[0][0])
    # 查询买家评价信息
    def queryevaluate(self,sid,pagenum):
        db = DB()
        sql = "select * from evaluate where sid='" + str(sid) + "'"
        cursor.execute(sql)
        evaluatenum = len(cursor.fetchall())
        sql = "select * from evaluate where sid = '" + str(sid) + "'" + "limit " + str(pagenum * 5) + ",5"
        cursor.execute(sql)
        dict = cursor.fetchall()
        print(dict)
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": db.queryusername(item[1]), "sid": item[2], "context": item[3], "grade": item[4],
                        "time": item[5]}
            data.append(jsonData)
        reList.update({"data": data})
        reList.update({"evaluatenum": evaluatenum})
        return reList

    # ==========卖家============
    def querybusinessinfo(self,id):
        sql = "select * from business where id = '" + str(id) + "'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        if len(dict) <= 0:
            reList = {"status": 201}
        else:
            reList = {"status": 200, "data": {"name": dict[0][1], "password": dict[0][2]}}
        return reList
    # 修改卖家信息
    def updatebusinessinfo(self,id,name,password):
        sql = "update business set name = '"+str(name)+"',"+"password='"+str(password)+"'where id='"+str(id)+"'"
        cursor.execute(sql)
        return {"status":200}
    # 根据商家id查询名下店铺所有信息
    def queryshopbybid(self,bid):
        sql = "select * from shop where bid = '" + str(bid) + "'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        if len(dict) <= 0:
            reList = {"status": 201}
        else:
            reList = {"status": 200, "data": {"id": dict[0][0], "name": dict[0][1], "cover": dict[0][2], "qualification": dict[0][3], "bid": dict[0][4]}}
        print(reList)
        return reList
    # 上传商铺大图
    def uploadshopcover(self,sid,filepath):
        print(filepath)
        filepath = str(filepath).replace('\\','/').strip('.')
        sql = "update shop set cover = '"+str(filepath)+"'where id = '"+str(sid)+"'"
        cursor.execute(sql)
        return {"status": 200}
    # 修改店铺名称
    def updateshopname(self,id,name):
        sql = "update shop set name='"+str(name)+"' where id='"+str(id)+"'"
        cursor.execute(sql)
        return {"status": 200}
    # 上传营业资质
    def uploadqualification(self,sid,filepath):
        print(filepath)
        filepath = str(filepath).replace('\\', '/').strip('.')
        sql = "update shop set qualification = '" + str(filepath) + "'where id = '" + str(sid) + "'"
        cursor.execute(sql)
        return {"status": 200}
    # 商家添加菜品
    def addfood(self,name,price,food,sid):
        sql = "insert into foods (name,price,food,sid,num) value ('"+name+"','"+price+"','"+food+"','"+sid+"','"+"0"+"')"
        print(sql)
        cursor.execute(sql)
        return {"status": 200}
    # 上传菜品图片
    def uploadfood(self,fid,filepath):
        filepath = str(filepath).replace('\\', '/').strip('.')
        sql = "update foods set food = '" + str(filepath) + "'where id = '" + str(fid) + "'"
        cursor.execute(sql)
        return {"status": 200}
    # 修改菜品
    def updatefood(self,id,name,price):
        sql = "update foods set name='"+name+"',price='"+price+"'where id='"+str(id)+"'"
        cursor.execute(sql)
        return {"status": 200}
    # 删除菜品
    def deletefood(self,fid):
        sql = "delete from foods where id='"+str(fid)+"'"
        cursor.execute(sql)
        return {"status": 200}
    # 通过fid查询菜名
    def queryfoodbyfid(self,fid):
        sql = "select * from foods where id='" + str(fid) + "'"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        jsonData = {"id": dict[0][0], "name": dict[0][1], "price": dict[0][2], "food": dict[0][3],"sid": dict[0][4]}
        reList.update({"data": jsonData})
        return reList

    # 查询用户的订单
    def queryordersbysid(self, sid, pagenum):
        sql = "select * from orders where sid='" + str(sid) + "'"
        cursor.execute(sql)
        ordersnum = len(cursor.fetchall())
        sql = "select * from orders where sid = '" + str(sid) + "'" + "limit " + str(pagenum * 3) + ",3"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "price": item[2], "num": item[3], "shopname": item[4],
                        "address": item[5], "remarks": item[6], "food": item[7], "fid": item[8], "uid": item[9],"sid":item[10]}
            data.append(jsonData)
        reList.update({"data": data})
        reList.update({"ordersnum": ordersnum})
        return reList
    # 销量排序
    def sortfoodsbynum(self,sid,pagenum,flag):
        sql = "SELECT sum(num),fid from orders where sid='"+str(sid)+"'GROUP BY fid "
        cursor.execute(sql)
        dict = cursor.fetchall()
        sql = "select * from foods where sid = '" + str(sid) + "'"
        cursor.execute(sql)
        dict1 = cursor.fetchall()
        foodsnum = len(dict1)
        print(foodsnum)
        for i in range(len(dict)):
            sql = "update foods set num='"+str(dict[i][0])+"' where id = '"+str(dict[i][1])+"'"
            cursor.execute(sql)
        sql = "select * from foods where sid = '" + str(sid) + "'" + "limit " + str(pagenum * 4) + ",4 "
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "price": item[2], "food": item[3],"sid":item[4],"num":item[5]}
            data.append(jsonData)
        if data:
            data.sort(key=lambda x: x['price'], reverse=flag)
        reList.update({"data": data})
        reList.update({"foodsnum": foodsnum})
        print(reList)
        return reList
# 商户订单按照时间排序
    def sortordersbytime(self,sid,pagenum,flag):
        print(sid,pagenum,flag)
        sql = "select * from orders where sid='" + str(sid) + "'"
        cursor.execute(sql)
        ordersnum = len(cursor.fetchall())
        sql = "select * from orders where sid = '" + str(sid) + "'" + "limit " + str(pagenum * 2) + ",2"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "price": item[2], "num": item[3], "shopname": item[4],
                        "address": item[5], "remarks": item[6], "food": item[7], "fid": item[8],"uid":item[9],"sid":item[10],"totalprice":item[11],"time":item[12]}
            data.append(jsonData)
        if data:
            data.sort(key=lambda x: x['time'], reverse=flag)
        reList.update({"data": data})
        reList.update({"ordersnum": ordersnum})
        print(reList)
        return reList
# 商户订单按照订单总价排序
    def sortordersbyprice(self,sid,pagenum,flag):
        print(sid,pagenum,flag)
        sql = "select * from orders where sid='" + str(sid) + "'"
        cursor.execute(sql)
        ordersnum = len(cursor.fetchall())
        sql = "select * from orders where sid = '" + str(sid) + "'" + "limit " + str(pagenum * 2) + ",2"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": item[1], "price": item[2], "num": item[3], "shopname": item[4],
                        "address": item[5], "remarks": item[6], "food": item[7], "fid": item[8],"uid":item[9],"sid":item[10],"totalprice":item[11],"time":item[12]}
            data.append(jsonData)
        if data:
            data.sort(key=lambda x: float(x['totalprice']), reverse=flag)
        reList.update({"data": data})
        reList.update({"ordersnum": ordersnum})
        print(reList)
        return reList
    # 通过id查询评价
    def queryevaluatebyfid(self,fid,pagenum):
        db = DB()
        sql = "select * from evaluate where fid='" + str(fid) + "'"
        cursor.execute(sql)
        evaluatenum = len(cursor.fetchall())
        sql = "select * from evaluate where fid = '" + str(fid) + "'" + "limit " + str(pagenum * 5) + ",5"
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "name": db.queryusername(item[1]), "sid": item[2], "context": item[3],
                        "grade": item[4],
                        "time": item[5],"fid":item[6]}
            data.append(jsonData)
        reList.update({"data": data})
        reList.update({"evaluatenum": evaluatenum})
        return reList
    # 管理员移除商家
    def deleteshop(self,id):
        sql = "delete from shop where id='"+str(id)+"'"
        cursor.execute(sql)
        return {"status":200}
    #
    def sortevaluatebygrade(self,sid,pagenum):
        db = DB()
        sql = "select * from evaluate where sid='"+sid+"'"
        cursor.execute(sql)
        evaluatenum = len(cursor.fetchall())
        sql = "select * from evaluate where sid = '" + str(sid) + "'" + "limit " + str(pagenum * 6) + ",6 "
        cursor.execute(sql)
        dict = cursor.fetchall()
        reList = {}
        data = []
        if len(dict) > 0:
            reList.update({"status": "200"})
        else:
            reList.update({"status": "201"})
        for item in dict:
            jsonData = {"id": item[0], "uid": db.queryusername(item[1]), "sid": item[2], "context": item[3],"grade": item[4],"time": item[5],"fid": item[6]}
            data.append(jsonData)
        if data:
            data.sort(key=lambda x: float(x['grade']), reverse=False)
        reList.update({"data": data})
        reList.update({"evaluatenum": evaluatenum})
        return reList