# let's import the necessary inbuilt python module sqlite3
import sqlite3

# create a class object for the  Database Schema
class RedbusDatabaseConn:
	# initialize the connection and server to create a Table and Data Schema
	def __init__(self):
		self.conn = sqlite3.connect("redbusDB.db")
		self._db = self.conn.cursor()
		self._db.execute("""CREATE TABLE if not exists bus_routes
            (
                id              integer primary key autoincrement,
                route_name      text,
                route_link      text,
                busname         text,
                bustype         text,
                departing_time  text,
                duration        text,
                reaching_time   text,
                star_rating     real,
                price           real,
                seats_available integer
            ) """)
		self.conn.commit()
	# add a row of Data to the bus_routes table
	def Add(self,route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available):
		self._db.execute('insert into bus_routes (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available) values (?,?,?,?,?,?,?,?,?,?)', (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available))
		self.conn.commit()
	# retrieves all the data from the bus_routes table
	def ListRequest(self):
		self._db.execute('select * from bus_routes')
		return self._db
	# method to close the database connection after all executions
	def close(self):
		self.conn.close()
	# delete all the data from the table
	def deleteAll(self):
		self._db.execute('delete from bus_routes')
		self.conn.commit()