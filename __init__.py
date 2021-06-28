import logging, re
from flask import Flask , render_template , request, send_file , jsonify, redirect ,url_for , flash
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy.engine import Engine
from sqlalchemy import event , desc , asc , DateTime
from .indexview import FABView
from .models import *
from .api import androidApi
import datetime
from flask_appbuilder.security.sqla.models import User
from flask_qrcode import QRcode 
from werkzeug.utils import secure_filename
from .helpers import *
from config import S3_BUCKET , S3_LOCATION
import werkzeug, json
from datetime import datetime
from flask_login import current_user
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer ,ListTrainer


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
valueList = {"rr"}
app = Flask(__name__)
app.config.from_object('config')
app.config['JSON_AS_ASCII'] = False
db = SQLA(app)
valueList = {"rr","bb"}
appbuilder = AppBuilder(app, db.session, base_template='mybase.html', indexview=FABView)
app.url_map.strict_slashes = False
api = androidApi(db)

###.  QRCode.   ###
QRcode(app)
###################
###.  ChatBot.   UNCOMMAND BELOW 3 LINE TO ENABLE THE FUNCTION OF CHATBOT!!!!   ###
# bot = ChatBot("ChatBot")
# trainer = ChatterBotCorpusTrainer(bot)  
# # trainer.train("chatterbot.corpus.english")

# PS :
#     install for chatbot
#     pip install update click
#.    python -m pip install en-core-web-sm

#     CHATBOT Error :[E941] Can't find model 'en'
    
#     Solution:
#     1. Open the venv\lib\Python37\lib\site-packages\chatterbot\tagging.py file
#     2. Go to Line 13
#     3. Replace self.nlp = spacy.load(self.language.ISO_639_1.lower()) with
#     if self.language.ISO_639_1.lower() == 'en':
#         self.nlp = spacy.load('en_core_web_sm')
#     else:
#         self.nlp = spacy.load(self.language.ISO_639_1.lower())

# Credit to :
# https://dev.to/sahilrajput/build-your-first-chatbot-in-5-minutes--15e3
###################

"""
Only include this for SQLLite constraints
"""
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

from app import views, data

#MAIN PAGE
# processor is for main page to load latest product.
# processor is loaded before loading template.
#1.Call Model to get data
#2.use Contetxt_processor pass value to MainPage, must use dict(key=value) e.g. dict(result=database_data)
@app.context_processor
def process():
    return dict(itemlists = db.session.query(Item).order_by(desc(Item.viewCounter)).limit(10),
                itemlists2 = db.session.query(Item).order_by(desc(Item.createdDate)).limit(10))

@app.context_processor                             
def category_list():
    return dict(category_list = db.session.query(Category).order_by(asc(Category.categoryName)).filter_by(parentCategoryID="").all())

#SEARCH PAGE
@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == "POST":
        keywords=request.form['search']
        results =db.session.query(Item).filter(Item.itemName.like('%'+keywords+'%')).all()
        #search Model by result key
        return render_template("/search/search_result.html", base_template='mybase.html', appbuilder=appbuilder, results=results,keywords=keywords)
    else:
        return render_template("/search/search.html", base_template='mybase.html', appbuilder=appbuilder)


#Product Details
@app.route("/product_detail/itemId=<itemId>")
def getProductDetails(itemId):
    #database
    item = db.session.query(Item).filter_by(id=itemId).first()
    category = db.session.query(Category).filter_by(id=item.categoryID).first()
    if category.parentCategoryID!="":
        parentCategory = db.session.query(Category).filter_by(id=category.parentCategoryID).first()
    else:
        parentCategory="" 
    viewCounter(item.id)
    url = request.url
    comments = getCommentContent(itemId)
    # strftime("%d/%m/%Y %H:%M:%S")
    return render_template("product/product.html", base_template='mybase.html',appbuilder=appbuilder,
                            item=item, category=category, parentCategory=parentCategory, url=url, comments=comments)

#Comment content
def getCommentContent(itemId):
    comments=db.session.query(Post).filter_by(itemID=itemId).order_by(asc(Post.postTime)).all()
    return comments
    
#Comment form
@app.route('/product_detail/itemId=<itemId>/comment_form', methods=['GET', 'POST'])
def createComment(itemId):
        itemId= itemId
        body=request.args.get('comment')
        userID=current_user.id
        postTime =datetime.now()
        newComment=Post( '',itemId, userID,postTime , body)
        db.session.add(newComment)
        db.session.commit()
        return redirect(url_for("getProductDetails",itemId=itemId))

# Product List
@app.route('/product_list/categoryId=<int:categoryId>')



@app.route('/product_list/productId=<int:productId>')  #<------------------for what?
def getProductListByCategoryId(categoryId=None, productId=None):
    product_list = find_ProductList(categoryId)[0]
    lists = find_ProductList(categoryId)[1]
    lists2 = []
    for list in lists:
        lists2.append(db.session.query(Category).filter_by(id=list).first().categoryName)
    lists = dict(zip(lists, lists2))
    return render_template("product/product_list.html", base_template='mybase.html', appbuilder=appbuilder, product_list=product_list, lists=lists)

def find_ProductList(catId):
    cat = db.session.query(Category).filter_by(id=catId).first()
    lists=[cat.id]
    if cat.parentCategoryID is not None:
        catList = []
        subCatList = db.session.query(Category).filter_by(parentCategoryID=cat.id).all()
        for cats in subCatList:
             lists.append(cats.id)
        for list in lists:
            catList.extend(db.session.query(Item).filter_by(categoryID=list).all())
    else:
        catList = db.session.query(Item).filter_by(categoryID=catId).all()
    return catList ,lists

# Most Recent Page
@app.route('/product_list/recent')
def getProductListByTime():
    product_list = db.session.query(Item).order_by(desc(Item.createdDate)).all()
    title = "Most Recent Items"
    return render_template("product/product_list.html", base_template='mybase.html', appbuilder=appbuilder, product_list=product_list, title=title)

# Most Popular Page
@app.route('/product_list/popular')
def getProductListByView():
    product_list = db.session.query(Item).order_by(desc(Item.viewCounter)).all()
    title = "Most Popular Items"
    return render_template("product/product_list.html", base_template='mybase.html', appbuilder=appbuilder, product_list=product_list, title=title)

#Redirect to User-Register Page
@app.route('/register')
def userRegister():
      return redirect("register/form")

#UserProduct CRUD Page

###edit product ###
@app.route('/edit/itemId=<int:itemId>')
def productEdit(itemId):
    item = db.session.query(Item).filter_by(id=itemId).first()
    categories = db.session.query(Category).all()
    return render_template("product/product_edit.html", base_template='mybase.html', appbuilder=appbuilder, item=item , categories=categories)

@app.route('/updateItem',methods=['Get','Post'])
def productUpdate():
    # item = request.form[]
    # return redirect(url_for('productEdit',itemId=4))
    return render_template("test.html", base_template='mybase.html', appbuilder=appbuilder)


###delete product ###
@app.route('/delete/itemId=<int:itemId>', methods=['GET'])
def deleteProduct(itemId):
    #return jsonify(itemId)
    db.session.query(Item).filter_by(id=itemId).delete()
    #db.session.commit()
    return redirect("/userproduct")
    
###create product ###
@app.route('/create')
def createForm():
    return render_template("product/product_create.html", base_template='mybase.html', appbuilder=appbuilder)



@app.route('/create' , methods=['GET','Post'])
def createItem():
   
    return redirect("/userproduct")

# def insertItemForm(form):
#     print(form)

#Function for View Counter
def viewCounter(itemId):
    item = db.session.query(Item).filter_by(id=itemId).first()
    item.viewCounter += 1
    db.session.commit()

#########   S3 upload function #########   

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # function to check file extension
# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/uploadpage')
# def uploadPage():
#     return render_template("S3upload.html", base_template='mybase.html', appbuilder=appbuilder)


# def upload_file_to_s3(file, bucket_name, acl="public-read"):

#     """
#     Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
#     """

#     try:

#         s3.upload_fileobj(
#             file,
#             bucket_name,
#             file.filename,
#             ExtraArgs={
#                 "ACL": acl,
#                 "ContentType": file.content_type
#             }
#         )

#     except Exception as e:
#         print("Something Happened: ", e)
#         return e

#     return "{}{}".format(S3_LOCATION, file.filename)

# @app.route("/upload", methods=["POST"])
# def upload_file():

# 	# A
#     if "user_file" not in request.files:
#         return "No user_file key in request.files"

# 	# B
#     file    = request.files["user_file"]

#     """
#         These attributes are also available

#         file.filename               # The actual name of the file
#         file.content_type
#         file.content_length
#         file.mimetype

#     """

# 	# C.
#     if file.filename == "":
#         return "Please select a file"

# 	# D.
#     if file and allowed_file(file.filename):
#         file.filename = secure_filename(file.filename)
#         output   	  = upload_file_to_s3(file, S3_BUCKET)
#         return str(output)

#     else:
#         return redirect("/")

#########   #S3 upload function #########   


######## API Testing field (temp) #########
@app.route("/api/recommend_product", methods=['GET'])
def getPopularProducts():
    return api.getPopularProducts()
    
@app.route('/api/product_list/recent', methods=['GET'])
def getRecentProducts():
    return api.getRecentProducts()
    
@app.route('/api/get_product_details', methods=['GET'])
def getProduct():
    itemId = request.args.get("itemId")
    return api.getProductDetails(itemId)
    
@app.route("/api/do_login", methods=['GET'])
def loginAccount():
    loginType = request.args.get('loginType')
    account = request.args.get('account')
    password = request.args.get('code')
    return api.doLogin(loginType, account, password)
    
    
@app.route('/api/upload_proudct', methods=['GET'])  
def uploadImageFile():
    code = 0
    msg = "Failed"
    imageFile = request.files['image']
    fileName = werkzeug.utils.secure_filename(imageFile.filename)
    imageFile.save(fileName)
    return jsonify(code=1,msg="Image uploaded successfully")
    
@app.route("/api/config", methods=['GET'])
def getConfig():
    return api.getConfig()

@app.route("/api/recommended_api/shuffling", methods=['POST'])
def adveristment():
    shuffling = request.args.get('shuffling')
    return api.getAdvertise(shuffling)
    
@app.route("/api/doSMSCode", methods=['GET'])
def sendSMS():
    loginType = request.args.get("loginType")
    account = request.args.get("account")
    code = request.args.get("code")
    return api.doSMSCode(loginType, account, code)
    
@app.route("/api/registerUser", methods=['GET'])
def registerUser():
    userName = request.args.get("userName")
    nickName = request.args.get("nickName")
    password = request.args.get("password")
    email = request.args.get("email")
    mobile = request.args.get("mobile")
    return jsonify(api.registerUser(userName, nickName, password, mobile, email))
    
@app.route("/api/privateChat", methods=['GET'])
def privateChat():
    userId = request.args.get("to_user_id")
    productId = request.args.get("uid")
    return api.getPrivateChat(userId, productId)
    
@app.route("/api/personal_api/get_user_page_info", methods=['GET'])
def getUserInfo():
    userId = request.args.get("id")
    return api.getUser(userId)
    
#############

##### chatbot  #########
@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')    
    return str(bot.get_response(userText)) 

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot/chatbot_page.html",base_template='mybase.html', appbuilder=appbuilder)
############################