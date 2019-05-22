from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
app=Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine=create_engine('postgresql:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('menu.html',restaurant=restaurant,items=items)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuJSON(restaurant_id,menu_id):
    item=session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(item.serialize)

@app.route('/restaurants/<int:restaurant_id>/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if(request.method=='POST'):
        item=MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(item)
        flash("new menu item created!")
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenu.html',restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    if(request.method=='POST'):
        menuItem=session.query(MenuItem).filter_by(id=menu_id).one()
        menuItem.name=request.form['name']
        session.add(menuItem)
        flash("menu item edited!")
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        menuItem=session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('editmenu.html',item=menuItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    if(request.method=='POST'):
        menuItem=session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(menuItem)
        flash("menu item deleted!")
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        menuItem=session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('deletemenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,item=menuItem)

if __name__=='__main__':
    app.secret_key="super secret key"
    app.debug=True
    app.run('10.0.2.15',port=5000)
