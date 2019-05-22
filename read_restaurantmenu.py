from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

#engine = create_engine('sqlite:///restaurantmenu.db')
engine=create_engine('postgresql:///restaurantmenu')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
spinachIcecream=session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
session.delete(spinachIcecream)
session.commit()

spinachIcecream=session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print spinachIcecream.restaurant.name




