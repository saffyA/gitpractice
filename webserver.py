from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

from database_setup import Restaurant, Base, MenuItem

engine=create_engine('postgresql:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output='';
                output+="<html><body><h1>List of Restaurants</h1>"
                restaurants=session.query(Restaurant).all()
                for restaurant in restaurants: 
                    output+="<h2> %s </h2>" % restaurant.name
                    output+="<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output+="<br><a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id

                output+="<br><a href='/restaurants/new'>Create New Restaurant</a>"
                output+="</html></body>"
 
                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                params=self.path.rsplit("/",2)
                params[1]

                output='';
                output+="<html><body>"
                output+="<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h2>Enter Updated Restaurant Name</h2><input name='updated_restaurant_name' type='text'/><input type='submit' value='Submit'/></form>" % params[1]
                output+="</html></body>"
 
                self.wfile.write(output)
                return

            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                params=self.path.rsplit("/",2)
                print params[1]

                restaurant=session.query(Restaurant).filter_by(id=params[1]).one()
                print restaurant.name

                output='';
                output+="<html><body>"
                output+="<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><h2>Are you sure you want to delete %s</h2><input type='submit' value='Yes'/></form>" % (params[1],restaurant.name)
                output+="</html></body>"
 
                self.wfile.write(output)
                return
            
        except IOError:
            self.send_response(404,"File not found %s" % self.path)

        try:
            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output='';
                output+="<html><body>"
                output+="<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter Restaurant Name</h2><input name='restaurant_name' type='text'/><input type='submit' value='Submit'/></form>"
                output+="</html></body>"

                self.wfile.write(output)
                return
            
        except IOError:
            self.send_response(404,"File not found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            if self.path.endswith('/new'):
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                restaurant_name=fields.get('restaurant_name')

                #Inserting restaurant into database
                newRestaurant=Restaurant(name=restaurant_name[0])
                session.add(newRestaurant)
                session.commit()

                output='';
                output+="<html><body><h1>List of Restaurants</h1>"
                restaurants=session.query(Restaurant).all()
                for restaurant in restaurants: 
                    output+="<h2> %s </h2>" % restaurant.name
                    output+="<a href='/restaurants/edit/%s'>Edit</a>" % restaurant.id
                    output+="<br><a href='/restaurants/delete/%s'>Delete</a>" % restaurant.id

                output+="<br><br><a href='/restaurants/new'>Create New Restaurant</a>"
                output+="</html></body>"
 
                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                restaurant_name=fields.get('updated_restaurant_name')

                params=self.path.rsplit("/",2)

                print restaurant_name[0]
                print params[1]

                #Updating restaurant
                restaurant=session.query(Restaurant).filter_by(id=params[1]).one()
                print "editing %s" % restaurant.name
                restaurant.name=restaurant_name[0]
                session.add(restaurant)
                session.commit()
        
                output='';
                output+="<html><body><h1>List of Restaurants</h1>"
                restaurants=session.query(Restaurant).all()
                for restaurant in restaurants: 
                    output+="<h2> %s </h2>" % restaurant.name
                    output+="<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output+="<br><a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id

                output+="<br><a href='/restaurants/new'>Create New Restaurant</a>"
                output+="</html></body>"        
 
                self.wfile.write(output)
                return

            if self.path.endswith('/delete'):

                params=self.path.rsplit("/",2)
                print params[1]

                #Deleting restaurant
                restaurant=session.query(Restaurant).filter_by(id=params[1]).one()
                print "deleting %s" % restaurant.name
                session.delete(restaurant)
                session.commit()
        
                output='';
                output+="<html><body><h1>List of Restaurants</h1>"
                restaurants=session.query(Restaurant).all()
                for restaurant in restaurants: 
                    output+="<h2> %s </h2>" % restaurant.name
                    output+="<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output+="<br><a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id

                output+="<br><a href='/restaurants/new'>Create New Restaurant</a>"
                output+="</html></body>"        
 
                self.wfile.write(output)
                return

        except:
            pass
        

def main():
    print "in main"
    try:
        port=5000
        server=HTTPServer(('10.0.2.15',port),webserverHandler)
        print "web server running on port %s" % port
        server.serve_forever()
        

    except KeyboardInterrupt:
        print ("^C was pressed")
        server.socket.close()


if __name__== '__main__':
    main()
