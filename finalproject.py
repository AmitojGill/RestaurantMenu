from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

#Add restaurants JSON Endpoint
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurant=[restaurant.serialize for restaurant in restaurants])

#Add restaurant/restaurant_id/menu/JSON
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItem=[item.serialize for item in menu])

#Add restaurant/restaurant_id/menu/menu_id/JSON
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=[item.serialize])

#Show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant)
	return render_template('restaurants.html', restaurants = restaurants)
	
#Add a new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New Restaurant Created")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

#Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method ==  'POST':
		updatedRestaurant = Restaurant(name = request.form['namme'], id=restaurant_id)
		session.add(updatedRestaurant)
		session.commit()
		flash('Restaurant Successfully Edited')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = restaurant)

#Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	deleteMenu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	if request.method == 'POST':
		session.delete(deleteRestaurant)
		for item in deleteMenu:
			session.delete(item)
		session.commit()
		flash('Restaurant Successfully Deleted')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = deleteRestaurant)

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
		flash('Menu Item Created')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html',restaurant_id = restaurant_id,restaurant=restaurant)

#Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	itemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			itemToEdit.name = request.form['name']
		if request.form['description']:
			itemToEdit.description = request.form['description']
		if request.form['price']:
			itemToEdit.price = request.form['price']
		if request.form['course']:
			itemToEdit.course = request.form['course']
		session.add(itemToEdit)
		session.commit()
		flash('Menu Item Successfully Edited')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant=restaurant, item=itemToEdit)

#Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('Memu item successfully deleted')
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html',restaurant = restaurant, item = itemToDelete)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)