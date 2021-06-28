import datetime
import random
import logging
from .models import Gender, Country , Item , Category
from app import db


log = logging.getLogger(__name__)


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


def fill_data():
    countries = ['Portugal', 'Germany', 'Spain', 'France', 'USA', 'China', 'Russia', 'Japan']
    for country in countries:
        c = Country(name=country)
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            log.error("Update ViewMenu error: {0}".format(str(e)))
            db.session.rollback()

#Item_Catagory method:
def getall_item_category():
    return db.session.query(Category).order_by(Category.categoryName).filter_by(parentCategoryID="").all()
    
# def get_item_category_name(param):
#     return db.session.query(Category).filter_by(id=param).first()

# def get_item_detail():
#     return db.session.query(Item).filter_by().first().id