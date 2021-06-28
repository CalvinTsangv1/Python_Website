from flask_appbuilder.views import IndexView

class FABView(IndexView):
    """
        A simple view that implements the index for the site
    """
    
# def getDatabase():
#     condition_query = []
	
# 	for key, value in condition.items():
# 		if value:
# 			condition_query.append(f"{key}='{value}'")
# 	if condition_query:
# 		condition_query = "WHERE " + ' AND '.join(condition_query)
# 	else:
# 		condition_query = ''
	
# 	postgres_select_query = f"""SELECT * FROM ab_register_user {condition_query} ORDER BY id;"""
# 	print(postgres_select_query)
	
# 	table = []
# 	table.extend(db.engine.execute(postgres_select_query).fetchall())

# 	return table
    index_template = 'index/index.html'
    
    
