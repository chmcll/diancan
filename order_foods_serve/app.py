import time
import os
from flask import Flask,request
from flask_cors import *
import json
from DBManger.DB import DB

db = DB()
app = Flask(__name__,template_folder='app.py',static_folder='static')
CORS(app, supports_credentials=True)
@app.route('/login',methods=['post'])
def login():
    name = json.loads(request.get_data())['name']
    password = json.loads(request.get_data())['password']
    type = json.loads(request.get_data())['type']
    response = db.login(name,password,type)
    return response
# 注册接口
@app.route('/register',methods=['post'])
def register():
    name = json.loads(request.get_data())['name']
    password = json.loads(request.get_data())['password']
    type = json.loads(request.get_data())['type']
    response = db.register(name,password,type)
    return str(response)
# 查询商家接口
@app.route('/queryshop',methods=['post'])
def queryshop():
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryshop(int(pagenum)-1)
    return response
@app.route('/queryshopbyid',methods=['post'])
def queryshopbyid():
    id = json.loads(request.get_data())['id']
    response = db.queryshopbyid(id)
    return response
# 查询菜品接口
@app.route('/queryfoods',methods=['post'])
def queryfoods():
    sid = json.loads(request.get_data())['sid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryfoods(sid,pagenum-1)
    return response
# 价格排序
@app.route('/sortfoodsbyprice',methods=['post'])
def sortfoodsbyprice():
    sid = json.loads(request.get_data())['sid']
    pagenum = json.loads(request.get_data())['pagenum']
    flag = json.loads(request.get_data())['flag']
    response = db.sortfoodsbyprice(sid,pagenum-1,flag)
    return response
# 查询用户信息接口
@app.route('/queryuserinfo',methods=['post'])
def queryuserinfo():
    id = json.loads(request.get_data())['id']
    response = db.queryuserinfo(id)
    return response
# 修改用户信息接口
@app.route('/updateuserinfo',methods=['post'])
def updateuserinfo():
    id = json.loads(request.get_data())['id']
    name = json.loads(request.get_data())['name']
    password = json.loads(request.get_data())['password']
    response = db.updateuserinfo(id,name,password)
    return response
# 加入购物车接口
@app.route('/addcart',methods=['post'])
def addcart():
    print(json.loads(request.get_data()))
    name = json.loads(request.get_data())['name']
    price = json.loads(request.get_data())['price']
    num = json.loads(request.get_data())['num']
    food = json.loads(request.get_data())['food']
    fid = json.loads(request.get_data())['fid']
    uid = json.loads(request.get_data())['uid']
    sid = json.loads(request.get_data())['sid']
    response = db.addcart(name,price,num,food,fid,uid,sid)
    return response

# 删除购物测内容
@app.route('/deletecart',methods=['post'])
def deletecart():
    fid = json.loads(request.get_data())['fid']
    uid = json.loads(request.get_data())['uid']
    response = db.deletecart(fid,uid)
    return response
# 查询购物车接口
@app.route('/querycart',methods=['post'])
def querycart():
    uid = json.loads(request.get_data())['uid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.querycart(uid,pagenum-1)
    return response
@app.route('/queryshopname',methods=['post'])
def queryshopname():
    fid = json.loads(request.get_data())['fid']
    response = db.queryshopname(fid)
    return response
# 加入订单接口
@app.route('/addorders',methods=['post'])
def addorders():
    print(json.loads(request.get_data()))
    name = json.loads(request.get_data())['name']
    price = json.loads(request.get_data())['price']
    num = json.loads(request.get_data())['num']
    shopname = json.loads(request.get_data())['shopname']
    address = json.loads(request.get_data())['address']
    remarks = json.loads(request.get_data())['remarks']
    food = json.loads(request.get_data())['food']
    fid = json.loads(request.get_data())['fid']
    uid = json.loads(request.get_data())['uid']
    sid = json.loads(request.get_data())['sid']
    response = db.addorders(name,price,num,shopname,address,remarks,food,fid,uid,sid)
    return response

@app.route('/queryorders',methods=['post'])
def queryorders():
    uid = json.loads(request.get_data())['uid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryorders(uid,pagenum-1)
    return response
# 增加地址接口
@app.route('/addaddress',methods=['post'])
def addaddrsee():
    name = json.loads(request.get_data())['name']
    phonenumber = json.loads(request.get_data())['phonenumber']
    address = json.loads(request.get_data())['address']
    uid = json.loads(request.get_data())['uid']
    response = db.addaddrsee(name,phonenumber,address,uid)
    return response
# 删除地址接口
@app.route('/deleteaddress',methods=['post'])
def deleteaddrsee():
    id = json.loads(request.get_data())['id']
    response = db.deleteaddrsee(id)
    return response
# 更新地址接口
@app.route('/updateaddress',methods=['post'])
def updateaddrsee():
    id = json.loads(request.get_data())['id']
    name = json.loads(request.get_data())['name']
    phonenumber = json.loads(request.get_data())['phonenumber']
    address = json.loads(request.get_data())['address']
    response = db.updateaddrsee(id,name, phonenumber, address)
    return response
# 查询地址接口
@app.route('/queryaddress',methods=['post'])
def queryaddrsee():
    uid = json.loads(request.get_data())['uid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryaddrsee(uid,pagenum-1)
    return response
# 通过id查地址
@app.route('/queryaddressbyid',methods=['post'])
def queryaddressbyid():
    id = json.loads(request.get_data())['id']
    response = db.queryaddressbyid(id)
    return response
# 查询用户所有地址
@app.route('/queryaddressall',methods=['post'])
def queryaddressall():
    uid = json.loads(request.get_data())['uid']
    response = db.queryaddrseeall(uid)
    return response
# 添加评价
@app.route('/addevaluate',methods=['post'])
def addevaluate():
    uid = json.loads(request.get_data())['uid']
    sid = json.loads(request.get_data())['sid']
    context = json.loads(request.get_data())['context']
    grade = json.loads(request.get_data())['grade']
    fid = json.loads(request.get_data())['fid']
    datestr = str(time.localtime(time.time()).tm_year)+"-"+str(time.localtime(time.time()).tm_mon)+"-"+str(time.localtime(time.time()).tm_mday)
    response = db.addevaluate(uid,sid,context,grade,datestr,fid)
    return response
# 某商家评价查询接口
@app.route('/queryevaluate',methods=['post'])
def queryevaluate():
    sid = json.loads(request.get_data())['sid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryevaluate(sid,pagenum-1)
    return response

# 查询卖家信息接口
@app.route('/querybusinessinfo',methods=['post'])
def querybusinessinfo():
    id = json.loads(request.get_data())['id']
    response = db.querybusinessinfo(id)
    return response
# 修改商家信息接口
@app.route('/updatebusinessinfo',methods=['post'])
def updatebusinessinfo():
    id = json.loads(request.get_data())['id']
    name = json.loads(request.get_data())['name']
    password = json.loads(request.get_data())['password']
    response = db.updatebusinessinfo(id,name,password)
    return response
# 根据卖家id查询商铺的所有信息
@app.route('/queryshopbybid',methods=['post'])
def queryshopbybid():
    bid = json.loads(request.get_data())['bid']
    response = db.queryshopbybid(bid)
    return response
# 商铺大图上传接口
@app.route('/uploadcover/<sid>',methods=['post','get'])
def uploadcover(sid):
    fileObj = request.files.get("file")
    filename = str(str(time.time())+fileObj.filename)
    filepath = os.path.join(r'.\static\cover',filename)
    fileObj.save(filepath)
    response = db.uploadshopcover(sid,filepath)
    return response
# 修改商铺名接口
@app.route('/updateshopname',methods=['post'])
def updateshopname():
    id = json.loads(request.get_data())['id']
    name = json.loads(request.get_data())['name']
    response = db.updateshopname(id,name)
    return response
# 商铺营业资质上传接口
@app.route('/uploadqualification/<sid>',methods=['post','get'])
def uploadqualification(sid):
    fileObj = request.files.get("file")
    filename = str(str(time.time()) + fileObj.filename)
    filepath = os.path.join(r'.\static\qualification', filename)
    fileObj.save(filepath)
    response = db.uploadqualification(sid, filepath)
    return response
# 添加菜品接口
@app.route('/addfood',methods=['post'])
def addfood():
    name = json.loads(request.get_data())['name']
    price = json.loads(request.get_data())['price']
    sid = json.loads(request.get_data())['sid']
    food="/static/food/333.jpeg"
    response = db.addfood(name,price,food,sid)
    return response
# 菜品图片上传接口
@app.route('/uploadfood/<fid>',methods=['post','get'])
def uploadfood(fid):
    fileObj = request.files.get("file")
    filename = str(str(time.time()) + fileObj.filename)
    filepath = os.path.join(r'.\static\food', filename)
    fileObj.save(filepath)
    response = db.uploadfood(fid, filepath)
    return response
# 修改菜品信息接口
@app.route('/updatefood',methods=['post'])
def updatefood():
    name = json.loads(request.get_data())['name']
    price = json.loads(request.get_data())['price']
    id = json.loads(request.get_data())['id']
    response = db.updatefood(id,name,price)
    return response
# 根据fid查询菜品接口
@app.route('/queryfoodbyfid',methods=['post'])
def queryfoodbyfid():
    fid = json.loads(request.get_data())['fid']
    response = db.queryfoodbyfid(fid)
    return response
# 菜品删除接口
@app.route('/deletefood',methods=['post'])
def deletefood():
    fid = json.loads(request.get_data())['fid']
    response = db.deletefood(fid)
    return response
# 店铺订单查询接口
@app.route('/queryordersbysid',methods=['post'])
def queryordersbysid():
    sid = json.loads(request.get_data())['sid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryordersbysid(sid,pagenum-1)
    return response
# 菜品按销量排序接口
@app.route('/sortfoodsbynum',methods=['post'])
def sortfoodsbynum():
    sid = json.loads(request.get_data())['sid']
    flag = json.loads(request.get_data())['flag']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.sortfoodsbynum(sid,pagenum-1,flag)
    return response
# 订单按时间排序接口
@app.route('/sortordersbytime',methods=['post'])
def sortordersbytime():
    sid = json.loads(request.get_data())['sid']
    flag = json.loads(request.get_data())['flag']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.sortordersbytime(sid,pagenum-1,flag)
    return response
# 订单按价格排序接口
@app.route('/sortordersbyprice',methods=['post'])
def sortordersbyprice():
    sid = json.loads(request.get_data())['sid']
    flag = json.loads(request.get_data())['flag']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.sortordersbyprice(sid,pagenum-1,flag)
    return response
# 某菜品的评价查询接口
@app.route('/queryevaluatebyfid',methods=['post'])
def queryevaluatebyfid():
    fid = json.loads(request.get_data())['fid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.queryevaluatebyfid(fid,pagenum-1)
    return response
# 管理员移除商家接口
@app.route('/deleteshop',methods=['post'])
def deleteshop():
    id = json.loads(request.get_data())['id']
    response = db.deleteshop(id)
    return response
# 管理员按评分排序评价接口
@app.route('/sortevaluatebygrade',methods=['post'])
def sortevaluatebygrade():
    sid = json.loads(request.get_data())['sid']
    pagenum = json.loads(request.get_data())['pagenum']
    response = db.sortevaluatebygrade(sid,pagenum-1)
    return response
if __name__ == '__main__':
    app.run()
