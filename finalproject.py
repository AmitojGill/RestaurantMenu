from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

'''
#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
'''

#Show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant)
	return render_template('restaurants.html', restaurants = restaurants)
	

#Add a new restaurant
@app.route('/restaurant/new')
def newRestaurant():
	return render_template('newRestaurant.html')

#Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return render_template('editRestaurant.html', restaurant = restaurant)

#Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return render_template('deleteRestaurant.html', restaurant = restaurant)

#Show menu for a given restaurant
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return render_template('menu.html',items = items, restaurant=restaurant)

#Add a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],
			description=request.form['description'],
			price=request.form['price'],
			restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html',restaurant_id = restaurant_id,restaurant=restaurant)

'''
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
'''

#Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	return render_template('editmenuitem.html',restaurant=restaurant, item=item)

#Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id):
	return render_template('deletemenuitem.html',restaurant=restaurant, item=item)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)