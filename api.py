from .aws_api import amazonApi;
from sqlalchemy import event , desc , asc
from flask import jsonify, send_file
from .models import Item , Category, Brand, ItemStatus, Condition, Shuffling
from flask_appbuilder.security.sqla.models import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re

class androidApi:
    
    def __init__(self, db):
        self.db = db
        self.aws = amazonApi();
        
    def getPopularProducts(self):
        code=0
        msg="Failed"
        result = []
        for i in self.db.session.query(Item).order_by(desc(Item.viewCounter)).all():
            list = i.serialize
            category = self.db.session.query(Category).filter_by(id=list.get('categoryID')).first()
            if category !=None:
                list['category'] = category.serialize
                del list['categoryID']
            brand = self.db.session.query(Brand).filter_by(id=list.get('brandID')).first()
            if brand != None:
                list['brand'] = brand.serialize
                del list['brandID']
            itemStatus = self.db.session.query(ItemStatus).filter_by(id=list.get('itemStatusID')).first()
            if itemStatus != None:
                list['itemStatus'] = itemStatus.serialize
                del list['itemStatusID']
            condition = self.db.session.query(Condition).filter_by(id=list.get('conditionID')).first()
            if condition != None:
                list['conditionID'] = condition.serialize
                del list['conditionID']
            user = self.db.session.query(User).filter_by(id=list.get('userID')).first()
            if user != None:
                for key in user.serialize:
                    list[key] = user.serialize[key]
            result.append(list)
        return jsonify(code=1,msg="Success",data=result)
        
    def getRecentProducts(self):
        code=0
        msg="Failed"
        result = []
        for i in self.db.session.query(Item).order_by(desc(Item.createdDate)).all():
            list = i.serialize
            category = self.db.session.query(Category).filter_by(id=list.get('categoryID')).first()
            if category !=None:
                list['category'] = category.serialize
                del list['categoryID']
            brand = self.db.session.query(Brand).filter_by(id=list.get('brandID')).first()
            if brand != None:
                list['brand'] = brand.serialize
                del list['brandID']
            itemStatus = self.db.session.query(ItemStatus).filter_by(id=list.get('itemStatusID')).first()
            if itemStatus != None:
                list['itemStatus'] = itemStatus.serialize
                del list['itemStatusID']
            condition = self.db.session.query(Condition).filter_by(id=list.get('conditionID')).first()
            if condition != None:
                list['conditionID'] = condition.serialize
                del list['conditionID']
            result.append(list)
        return jsonify(code=1,msg="Success",data=result)
        
    def getProductDetails(self, itemId):
        code=0
        msg="Failed"
        data = ""
        itemDetails = self.db.session.query(Item).filter_by(id=itemId).first().serialize
        if itemDetails != None and len(itemDetails) != 0:
            category = self.db.session.query(Category).filter_by(id=itemDetails.get('categoryID')).first()
            if category !=None:
                itemDetails['category'] = category.serialize
                del itemDetails['categoryID']
            brand = self.db.session.query(Brand).filter_by(id=itemDetails.get('brandID')).first()
            if brand != None:
                itemDetails['brand'] = brand.serialize
                del itemDetails['brandID']
            itemStatus = self.db.session.query(ItemStatus).filter_by(id=itemDetails.get('itemStatusID')).first()
            if itemStatus != None:
                itemDetails['itemStatus'] = itemStatus.serialize
                del itemDetails['itemStatusID']
            condition = self.db.session.query(Condition).filter_by(id=itemDetails.get('conditionID')).first()
            if condition != None:
                itemDetails['conditionID'] = condition.serialize
                del itemDetails['conditionID']
            code = 1
            msg = "Success"
            data = itemDetails
        return jsonify(code=code,msg=msg,data=data)
        
    def getConfig(self):
        data = {}
        data['heartbeat'] = 60
        data['is_force_upgrade'] = 0
        data['is_ios_base'] = 0
        data['is_binding_mobile'] = 0

        return jsonify(code=1,msg="Success",data=data)
        
    def doLogin(self, loginType, account, password):
        loginType = 2  #default email login
        
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        result = {'code':0, 'msg':''}
        if loginType == 1:
            if account.isnumeric() == False or len(account) != 8:
                result['code'] = 0
                result['msg'] = 'Mobile phone number format is incorrect!'
                return jsonify(result)
        elif loginType == 2:
            if re.search(regex, account) == False:
                result['code'] = 0
                result['msg'] = 'Email format is incorrect!'
                return jsonify(result)
                
        accountInfo = self.db.session.query(User).filter_by(username=account).first()
        if accountInfo.serialize == None or accountInfo.serialize == {} or accountInfo.serialize == []:
            result['msg'] = "Account don't exist, please register account"
            result['data'] = accountInfo.serialize
            return jsonify(result)
        
        if check_password_hash(accountInfo.serialize['password'], '123'):
            result['msg'] = "Input wrong password, please retry again!"
            result['data'] = ""
            return jsonify(result)
            
        result['code'] = 1
        result['msg'] = 'successfully login'
        result['data'] = accountInfo.serialize
        return jsonify(result)
        
    def getAdvertise(self, shuffling_id):
        result = {'code':0,'msg':'','data':''}
        data = []
        imageList = self.db.session.query(Shuffling).filter_by(slide_id=1, status=1).order_by(desc(Shuffling.list_order)).all()
        for image in imageList:
            data.append(image.serialize)
            
        if len(data) >= 1:
            result['code'] = 1
            result['data'] = data
        else:
            result['msg'] = "No image"
            
        return jsonify(result)
        
    def registerUser(self,userName, nickName, password, mobile, email):
        result = {'code':0,'msg':'','data':''}
        data = []
        if self.aws.createUserIdentity(userName, nickName, email, mobile):
            response = self.aws.updateUserIdentity(userName, nickName, password, email, mobile)
            result['msg'] = 'register successfully'
            result['data'] = response['ResponseMetadata']['HTTPStatusCode']
            return result
        return result
        
    def doSMSCode(self,loginType, account, code):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        result = {'code':0, 'msg':''}
        ### SMS Type
        #if loginType == "1":
        #    if account.isnumeric() == False or len(account) != 8:
        #        result['code'] = 0
        #        result['msg'] = 'Mobile phone number format is incorrect!'
        #        return jsonify(result)
        #    result['msg'] = self.aws.sendSMSCode('+852'+account, code)
        #    
        ### Email Type
        #elif loginType == "2":
        #    if re.search(regex, account) == False:
        #        result['code'] = 0
        #        result['msg'] = 'Email format is incorrect!'
        #        return jsonify(result)
        #    result['msg'] = self.aws.sendEmailCode(account, code, "Hong Kong")
        result['msg'] = "Message sent it!"
        result['code'] = 1
        return jsonify(result)
        
    def getPrivateChat(self,userId, productId):
        userInfo = self.db.session.query(User).filter_by(id=userId).first().serialize
        productInfo = self.db.session.query(Item).filter_by(id=productId).first().serialize
        return jsonify(code=1,product_id=productInfo['id'], user_id=productInfo['userID'], photo=productInfo['photoURL'], item_name=productInfo['itemName'],user_info=userInfo)

    def getUser(self, userId):
        return jsonify(self.db.session.query(User).filter_by(id=userId).first().serialize)

    #def getproductImage()
#########   API   ##########
# Display Object
# 1.Banner, 2.Daily Product, 3.Product Detail, 4.Profile 5.userLogin 6.AWS send SMS
##############
#1. GET BANNER 
###############
#@app.route("/getBannerImage?imageName=<image_name>", methods=['GET'])
#def getBannerImage(image_name):
#    filename = "static/img/" + image_name
#    return send_file(filename, mimetype=image_name.split(".")[1])
##############
##2. Daily Product
##############
#@app.route("/getDailyProduct", methods=['GET'])
#def getDailyProduct():
#    return jsonify(json_list = db.session.query(Item.itemName, Item.price, Item.itemDescription).all())
##############
##3. Product Detail
##############
#@app.route("/getProductDetail?itemId=<itemId>", methods=['GET'])
#def getProductDetailById(itemId):
#    return jsonify(db.session.query(Item.id, Item.id, Item.categoryID, Item.itemName, Item.price, Item.itemDescription, Item.itemStatusID, Item.viewCounter).filter(Item.id == itemId).first())
#
#@app.route("/getProductDetail?itemName=<itemName>", methods=['GET'])
#def getProductDetailByName(itemName):
#    return jsonify(db.session.query(Item.id, Item.id, Item.categoryID, Item.itemName, Item.price, Item.itemDescription, Item.itemStatusID, Item.viewCounter).filter(Item.itemName == itemName).first())
##############
##4. Profile
##############
#@app.route("/getUser?username=<username>", methods=['GET'])
#def getUser(username):
#    return jsonify(db.session.query(User.id, User.email, User.password, User.username, User.first_name, User.last_name, User.mobile, User.gender, User.joinDate).filter(User.username == username).first())
#
#@app.route("/getUserInfo?id=<id>", methods=['GET'])
#def getUserInfo(id):
#    return jsonify(db.session.query(User.id, User.email, User.password, User.username, User.first_name, User.last_name, User.mobile, User.gender, User.joinDate).filter(User.id == id).first())
#############
##5. userLogin
#############
#@app.route("/doLogin?loginType=<loginType>&account=<account>&password=<password>", methods=['GET'])
#def doLogin(loginType, account, password):
#    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
#    result = {'code':0, 'msg':''}
#    if loginType == 1:
#        if account.isnumeric() == False or len(account) != 8:
#            result['code'] = 0
#            result['msg'] = 'Mobile phone number format is incorrect!'
#            return jsonify(result)
#    elif loginType == 2:
#        if re.search(regex, account) == False:
#            result['code'] = 0
#            result['msg'] = 'Email format is incorrect!'
#            return jsonify(result)
#    return jsonify(db.session.query(User.id, User.email, User.password, User.username, User.first_name, User.last_name, User.mobile, User.gender, User.joinDate).filter(User.username == account).first())
#############
##6. aws send SMS
#############
#@app.route("/doSMSCode?loginType=<loginType>&account=<account>&code=<code>", methods=['POST'])
#def doSMSCode(loginType, account, code):
#    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
#    result = {'code':0, 'msg':''}
#    ### SMS Type
#    if loginType == 1:
#        if account.isnumeric() == False or len(account) != 8:
#            result['code'] = 0
#            result['msg'] = 'Mobile phone number format is incorrect!'
#            return jsonify(result)
#        result['msg'] = aws.sendSMSCode(account, code)
#    ### Email Type
#    elif loginType == 2:
#        if re.search(regex, account) == False:
#            result['code'] = 0
#            result['msg'] = 'Email format is incorrect!'
#            return jsonify(result)
#        result['msg'] = aws.sendEmailCode(account, code, "Hong Kong")
#    result['code'] = 1
#    return jsonify(result)
##data.fill_gender()
##data.fill_data()
#db.create_all()