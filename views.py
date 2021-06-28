from flask_appbuilder import ModelView, has_access 
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Employee,Department, Function, EmployeeHistory, Benefit, MenuItem, MenuCategory, News, NewsCategory , Contact , ContactGroup, Country , Item
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app import appbuilder, db ,data
from flask_appbuilder.baseviews import expose, BaseView
from flask import render_template
from flask_login import current_user

def department_query():
    return db.session.query(Department)

class EmployeeHistoryView(ModelView):
    datamodel = SQLAInterface(EmployeeHistory)
    #base_permissions = ['can_add', 'can_show']
    list_columns = ['department', 'begin_date', 'end_date']

class EmployeeView(ModelView):
    datamodel = SQLAInterface(Employee)
    list_columns = ['full_name', 'department.name', 'employee_number']
    edit_form_extra_fields = {'department':  QuerySelectField('Department', query_factory=department_query, widget=Select2Widget(extra_classes="readonly"))}
    related_views = [EmployeeHistoryView]
    show_template = 'appbuilder/general/model/show_cascade.html'

class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)
    related_views = [EmployeeView]

class DepartmentView(ModelView):
    datamodel = SQLAInterface(Department)
    related_views = [EmployeeView]

class BenefitView(ModelView):
    datamodel = SQLAInterface(Benefit)
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

class MenuItemView(ModelView):
    datamodel = SQLAInterface(MenuItem)
    list_columns = ['id', 'name', 'link', 'menu_category_id']

class MenuCategoryView(ModelView):
    datamodel = SQLAInterface(MenuCategory)
    list_columns = ['id', 'name']

class NewsView(ModelView):
    datamodel = SQLAInterface(News)
    list_columns = ['id', 'title', 'content', 'date', 'newsCat_id']

class NewsCategoryView(ModelView):
    datamodel = SQLAInterface(NewsCategory)
    list_columns = ['id', 'name']

class NewsPageView(BaseView):
    default_view = 'local_news'

    @expose('/local_news/')
    def local_news(self):
        param1 = 'Local News'
        self.update_redirect()
        return self.render_template('news.html', param1 = param1)

    @expose('/global_news/')
    def global_news(self):
        param1 = 'Global News'
        self.update_redirect()
        return self.render_template('news.html', param1=param1)

""" Page View """
#appbuilder.add_view(NewsPageView, 'Local News', category="News")
#appbuilder.add_link("Global News", href="/newspageview/global_news/", category="News")

""" Custom Views """
#appbuilder.add_view(MenuItemView, "MenuItem", icon="fa-folder-open-o", category="Admin")
#appbuilder.add_view(MenuCategoryView, "MenuCategory", icon="fa-folder-open-o", category="Admin")
#appbuilder.add_view(NewsView, "News", icon="fa-folder-open-o", category="Admin")
#appbuilder.add_view(NewsCategoryView, "NewsCategory", icon="fa-folder-open-o", category="Admin")

# ------------------------------------

class CategoryView(BaseView):
    default_view = 'category'
    
    @expose('/')
    def category(self):
        categories= data.getall_item_category()
        self.update_redirect()
        return self.render_template('category/category.html', categories = categories)

appbuilder.add_view(CategoryView, "Category")

class Search(BaseView):
    default_view = 'search'
    @expose('/')
    @has_access
    def search(self):
        self.update_redirect()
        return self.render_template('search/search.html')

appbuilder.add_view(Search,"Search",icon="fa fa-search")

class UserProduct(BaseView):
    default_view = 'userproduct'
    
    @expose('/')
    @has_access
    def userproduct(self):
        role = str(current_user.roles[0])
        if(role =='Admin'):
            itemList = db.session.query(Item).all()
        else : 
            itemList = db.session.query(Item).filter_by(userID = current_user.id).all()
        return self.render_template('product/mylistingitems.html' , itemList=itemList ,role=role)

appbuilder.add_view(UserProduct,"My Listing Items",icon="fas fa-cubes")
# class MyView(BaseView):

#     default_view = 'method1'

#     @expose('/method1/')
#     @has_access
#     def method1(self):
#         # do something with param1
#         # and return to previous page or index
#         return 'Hello'

#     @expose('/method2/<string:param1>')
#     @has_access
#     def method2(self, param1):
#         param1 = 'lam'
#         param1 = 'Goodbye %s' % (param1)
#         return param1
        
#     @expose('/method3/<string:param1>')
#     @has_access
#     def method3(self, param1):
#         item_categorys = data.getall_item_category()   #first: create class in models.py and define what attributes return 
#                                                     #second: create db.session method in data.py
#                                                     #thrid: create view in view.py and define what data passing to the template.
#         # do something with param1
#         # and render template with param
#         param1 = 'Goodbye %s' % (param1)
#         self.update_redirect()
#         return self.render_template('method3.html',
#                               param1 = param1 ,
#                               item_categorys = item_categorys )
                  
# appbuilder.add_view(MyView, "Method1", category='My View')
# appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')
# appbuilder.add_link("Method3", href='/myview/method3/john', category='My View')

# class MyView(BaseView):
 
#     default_view = 'method1'
#     list_columns = ['name','url']

#     @expose('/method1/')
#     def method1(self):
#         # do something with param1
#         # and return to previous page or index
#         return 'Hello'
        
#     @expose('/method2/<string:param1>')
#     def method2(self, param1):
#         # do something with param1
#         # and render it
#         param1 = 'Hello %s' % (param1)
#         return param1
    
#     @expose('/method3/<string:param1>')
#     def method3(self, param1):
#         param2 = 'Goodbye %s' % (param1)
#         self.update_redirect()
#         return self.render_template('method3.html',
#                               param1 = param1)

# appbuilder.add_view_no_menu(MyView())
# appbuilder.add_link("Method3", href='/myview/method3/john', category='My View')


# class ContactModelView(ModelView):
#     datamodel = SQLAInterface(Contact)

#     label_columns = {'contact_group':'Contacts Group'}
#     list_columns = ['name','personal_cellphone','birthday','contact_group']

#     show_fieldsets = [
#         (
#             'Summary',
#             {'fields': ['name', 'address', 'contact_group']}
#         ),
#         (
#             'Personal Info',
#             {'fields': ['birthday', 'personal_phone', 'personal_cellphone'], 'expanded': False}
#         ),
#     ]
    
# class GroupModelView(ModelView):
#     datamodel = SQLAInterface(ContactGroup)
#     related_views = [ContactModelView]
    
# appbuilder.add_view(
#     GroupModelView,
#     "List Groups",
#     icon = "fa-folder-open-o",
#     category = "Contacts",
#     category_icon = "fa-envelope"
# )
# appbuilder.add_view(
#     ContactModelView,
#     "List Contacts",
#     icon = "fa-envelope",
#     category = "Contacts"
# )

# class MyView(ModelView):
#     datamodel = SQLAInterface(MyTable)
#     search_columns = ['name','address']

db.create_all()