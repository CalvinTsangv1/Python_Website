import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.security.registerviews import RegisterUserDBView
from flask_babel import lazy_gettext
import json

class MyRegisterUserDBView(RegisterUserDBView):
    email_template = 'register_mail.html'
    email_subject = lazy_gettext('Your Account activation')
    activation_template = 'activation.html'
    form_title = lazy_gettext('Fill out the registration form')
    error_message = lazy_gettext('Not possible to register you at the moment, try again later')
    message = lazy_gettext('Registration sent to your email')

class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class Country(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class Department(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Function(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Benefit(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_benefits_employee = Table('benefits_employee', Model.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('benefit_id', Integer, ForeignKey('benefit.id')),
                                Column('employee_id', Integer, ForeignKey('employee.id'))
)

def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

class EmployeeHistory(Model):
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship("Employee")
    begin_date = Column(Date, default=today)
    end_date = Column(Date)

class Employee(Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    address = Column(Text(250), nullable=False)
    fiscal_number = Column(Integer, nullable=False)
    employee_number = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    function_id = Column(Integer, ForeignKey('function.id'), nullable=False)
    function = relationship("Function")
    benefits = relationship('Benefit', secondary=assoc_benefits_employee, backref='employee')
    begin_date = Column(Date, default=datetime.date.today(), nullable=True)
    end_date = Column(Date, default=datetime.date.today(), nullable=True)

    def __repr__(self):
        return self.full_name

class MenuItem(Model):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    link = Column(String(150), nullable=False)
    menu_category_id = Column(Integer, ForeignKey('menu_category.id'), nullable=False)
    menu_category = relationship("MenuCategory")

class MenuCategory(Model):
    __tablename__ = 'menu_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class News(Model):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    date = Column(Date, default=datetime.date.today(), nullable=True)
    newsCat_id = Column(Integer, ForeignKey('news_category.id'), nullable=False)
    newsCat = relationship("NewsCategory")

class NewsCategory(Model):
    __tablename__ = 'news_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    
class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address =  Column(String(564), default='Street')
    birthday = Column(Date)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'))
    contact_group = relationship("ContactGroup")

    def __repr__(self):
        return self.name

########## our models ###############

class Review(Model):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship("User")
    roleID = Column(Integer, ForeignKey('ab_role.id'), nullable=False)
    role = relationship("Role")
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    createdDate = Column(Date, default=datetime.date.today(), nullable=False)
    
    def __repr__(self):
        return self.name

class Region(Model):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    regionName = Column(String(50), unique = False, nullable=False)
    countryID = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship("Country")

    def __repr__(self):
        return self.name

class Address(Model):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    addressLine1 = Column(Text, nullable=False)
    addressLine2 = Column(Text, nullable=True)
    regionID = Column(Integer, ForeignKey('region.id'), nullable=True)
    region = relationship("Region", backref="address")
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return self.name

class AddressBook(Model):   #composite primary and foreign keys
    __tablename__ = 'addressbook'
    userID = Column(Integer, ForeignKey('ab_user.id'), primary_key=True)
    user = relationship("User", backref="addressbook")
    addressID = Column(Integer, ForeignKey('address.id'), primary_key=True)
    address = relationship("Address", backref="addressbook") 

    def __repr__(self):
        return str(self.addressID)

class Category(Model):     #not sure 
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    parentCategoryID = Column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship("Category")
    categoryName = Column(String(50), nullable=False)
    iconURL = Column(String(150), nullable=True)
    
    def __init__(self,id,categoryName,iconURL,parentCategoryID):
        self.id = id
        self.categoryName = categoryName
        self.iconURL = iconURL
        self.parentCategoryID = parentCategoryID
    
    def __repr__(self):
        return (self.id,self.categoryName,self.iconURL,self.parentCategoryID)
        
    def __str__(self):
        return self.categoryName
        
    @property
    def serialize(self):
        return self.categoryName

class Brand(Model):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    brandName = Column(String(50), nullable=False)
    
    def __init__(self,id,brandName):
        self.id = id
        self.brandName = brandName

    def __repr__(self):
        return self.name
        
    @property
    def serialize(self):
        return {'id':self.id,'brandName':self.brandName}

class ItemStatus(Model):
    __tablename__ = 'itemstatus'
    id = Column(Integer, primary_key=True)
    itemStatus = Column(String(8), nullable=False)

    def __init__(self, id, itemStatus):
        self.id = id
        self.itemStatus = itemStatus

    def __repr__(self):
        return self.name
        
    @property
    def serialize(self):
        return self.itemStatus

class Condition(Model):
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True)
    condition = Column(String(4), nullable=False)
    
    def __init__(self, id, condition):
        self.id = id
        self.condition = condition

    def __repr__(self):
        return self.name
        
    @property
    def serialize(self):
        return {'id':self.id,'condition':self.condition}

def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Item(Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship("User", backref="item")
    categoryID = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category")
    itemName = Column(String(100), nullable=False)
    brandID = Column(Integer, ForeignKey('brand.id'), nullable=True)
    brand = relationship("Brand", backref="item")
    price = Column(Integer, nullable=False)
    itemDescription = Column(Text, nullable=True)
    photoURL = Column(String(2000), nullable=True)
    itemStatusID = Column(Integer, ForeignKey('itemstatus.id'), nullable=False)
    itemStatus = relationship("ItemStatus")
    conditionID = Column(Integer, ForeignKey('condition.id'), nullable=False)
    condition = relationship("Condition")
    createdDate = Column(Date, default=datetime.date.today(), nullable=False)
    viewCounter = Column(Integer, default=0, nullable=False)

    def __init__(self, userID, user, categoryID, category, itemName, brandID, brand, price, itemDescription, photoURL, itemStatusID, itemstatus, conditionID, condition, createdDate, viewCounter):
        self.userID = userID
        self.user = user
        self.categoryID = categoryID
        self.category = category
        self.itemName = itemName
        self.brandID = brandID
        self.brand = brand
        self.price = price
        self.itemDescription = itemDescription
        self.photoURL = photoURL
        self.itemStatusID = itemStatusID
        self.itemstatus = itemstatus
        self.conditionID = conditionID
        self.condition = condition
        self.createdDate = createdDate
        self.viewCounter = viewCounter

    def __repr__(self):
        return self.itemName
    
    def __str__(self):
        return self.itemName
        
    @property
    def serialize(self):
        return {'id': self.id,'userID':self.userID,
            'categoryID':self.categoryID,
			'itemName':self.itemName,
			'brandID':self.brandID,
			'brand':self.brand,
			'price':self.price,
			'itemDescription':self.itemDescription,
			'photoURL':self.photoURL,
			'itemStatusID':self.itemStatusID,
			'conditionID':self.conditionID,
			'createdDate':self.createdDate,
			'viewCounter':self.viewCounter}
    
    @property
    def serialize_many2many(self):
        return [ item.serialize for item in self.many2many]

class Message(Model):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship("User", backref="Message")
    itemID = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship("Item", backref="Message")
    createdDate = Column(Date, default=datetime.date.today(), nullable=False)
    message = Column(Text, nullable=False)

    def __repr__(self):
        return self.message

class Like(Model):  #composite primary and foreign keys
    __tablename__ = 'like'
    userID = Column(Integer, ForeignKey('ab_user.id'), primary_key=True)
    user = relationship("User", backref="Like")
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="Like")

    def __repr__(self):
        return self.name

class OfferStatus(Model):
    __tablename__ = 'offerstatus'
    id = Column(Integer, primary_key=True)
    offerStatus = Column(String(8), nullable=False)

    def __repr__(self):
        return self.name

class Offer(Model): #composite primary and foreign keys
    __tablename__ = 'offer'
    buyerID = Column(Integer, ForeignKey('ab_user.id'), primary_key=True)
    user = relationship("User", backref="Offer")
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="Offer")
    offerDate = Column(Date, default=datetime.date.today(), primary_key=True)
    offer = Column(Integer, nullable=False)
    offerStatusID = Column(Integer, ForeignKey('offerstatus.id'), nullable=False)
    offerstatus = relationship("OfferStatus", backref="Offer")

    def __repr__(self):
        return str(self.offer)

class PaymentMethod(Model):
    __tablename__ = 'paymentmethod'
    id = Column(Integer, primary_key=True)
    paymentMethod= Column(String(16), nullable=False)

    def __repr__(self):
        return self.name

class AvailablePaymentMethod(Model):
    __tablename__ = 'availablepaymentmethod'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    paymentMethodID = Column(Integer, ForeignKey('paymentmethod.id'), primary_key=True)
    paymentMethod = relationship("PaymentMethod")
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return self.name

class DeliveryMethod(Model):
    __tablename__ = 'deliverymethod'
    id = Column(Integer, primary_key=True)
    deliveryMethod= Column(String(9), nullable=False)

    def __repr__(self):
        return self.name

class AvailableDeliveryMethod(Model):
    __tablename__ = 'availabledeliverymethod'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    deliveryMethodID = Column(Integer, ForeignKey('deliverymethod.id'), primary_key=True)
    deliveryMethod = relationship("DeliveryMethod")
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return self.name

class CarBody(Model):
    __tablename__ = 'carbody'
    id = Column(Integer, primary_key=True)
    carBody= Column(String(13), nullable=False)

    def __repr__(self):
        return self.name

class CarTransmission(Model): 
    __tablename__ = 'cartransmission'
    id = Column(Integer, primary_key=True)
    carTransmission = Column(String(6), nullable=False)

    def __repr__(self):
        return self.name

class CarInfo(Model): 
    __tablename__ = 'carinfo'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="CarInfo")
    carBodyID = Column(Integer, ForeignKey('carbody.id'))
    carBody = relationship("CarBody", backref="CarInfo")
    carTransmissionID = Column(Integer, ForeignKey('cartransmission.id'))
    carTransmission = relationship("CarTransmission", backref="CarInfo")
    ownerCount = Column(Integer, nullable=False)
    seats = Column(Integer, nullable=False)

    def __repr__(self):
        return self.name

class PropertyType(Model):
    __tablename__ = 'propertytype'
    id = Column(Integer, primary_key=True)
    propertyType = Column(String(20), nullable=False)

    def __repr__(self):
        return self.name

class PropertyLevel(Model):
    __tablename__ = 'propertylevel'
    id = Column(Integer, primary_key=True)
    propertyLevel = Column(String(9), nullable=False)

    def __repr__(self):
        return self.name

class Furnishing(Model):
    __tablename__ = 'furnishing'
    id = Column(Integer, primary_key=True)
    furnishing = Column(String(7), nullable=False)

    def __repr__(self):
        return self.name

class Facilities(Model):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key=True)
    facilities = Column(String(25), nullable=False)

    def __repr__(self):
        return self.name

class AvailableFacilities(Model):
    __tablename__ = 'availablefacilities'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    facilitiesID = Column(Integer, ForeignKey('facilities.id'), primary_key=True)
    facilities = relationship("Facilities")
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return self.name

class Features(Model):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    features = Column(String(18), nullable=False)

    def __repr__(self):
        return self.name

class AvailableFeatures(Model):
    __tablename__ = 'availablefeatures'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    featuresID = Column(Integer, ForeignKey('features.id'), primary_key=True)
    features = relationship("Features")
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return self.name

class PropertyInfo(Model):
    __tablename__ = 'propertyinfo'
    itemID = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item", backref="PropertyInfo")
    propertyTypeID = Column(Integer, ForeignKey('propertytype.id'))
    propertyType = relationship("PropertyType", backref="PropertyInfo")
    propertyLevelID = Column(Integer, ForeignKey('propertylevel.id'))
    propertyLevel= relationship("PropertyLevel", backref="PropertyInfo")
    buildingAge = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)
    beds = Column(Integer, nullable=False)
    baths = Column(Integer, nullable=False)
    furnishinghingID = Column(Integer, ForeignKey('furnishing.id'))
    furnishing = relationship("Furnishing", backref="PropertyInfo")

    def __repr__(self):
        return self.name
        
def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)

class Shuffling(Model):
    __tablename__ = 'cmf_slide_item'
    id = Column(Integer, primary_key=True)
    slide_id = Column(Integer)
    status = Column(Integer)
    list_order = Column(Integer, nullable = True)
    title = Column(String(255), nullable = True)
    image = Column(String(255), nullable = True)
    url = Column(String(255), nullable = True)
    target = Column(String(255), nullable = True)
    description = Column(String(255), nullable = True)
    content = Column(String(255), nullable = True)
    more = Column(String(255), nullable = True)
    is_auth_info  = Column(Integer, nullable = True)
    article_id  = Column(Integer, nullable = True)
    type = Column(Integer, nullable = True)
    
    def __repr__(self):
        return self.id
    
    @property
    def serialize(self):
        return {'id':self.id, 'title':self.title, 'image':self.image, 'url':self.url}

class Post(Model):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    itemID = Column(Integer, ForeignKey('item.id'), nullable=False) #new
    item = relationship("Item") #new
    userID = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship("User")
    postTime = Column(DateTime, default=datetime.datetime.now, nullable=False)
    body = Column(Text, nullable=False)
    
    def __repr__(self):
        return self.id
        
    def __init__(self, id, itemID, userID, postTime, body):
        self.id = id
        self.itemID = itemID
        self.userID = userID
        self.postTime = postTime
        self.body = body
        
    def __str__(self):
        return self.body