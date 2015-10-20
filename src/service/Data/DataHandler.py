import psycopg2
import json

class DataHandler:

    def __init__(self):
        with open('config.json') as data_file:
            self.config = json.load(data_file)
        self.connection_string = "dbname='" + self.config['dbname']+ "' host='" + self.config['host']+ "' port='" + \
                                 self.config['port'] + "' user='" + self.config['user'] + "' password='" + self.config['password'] + "'"
        print self.connection_string


    def connect(self):
        try:
            self.connection = psycopg2.connect(self.connection_string)
            print "I am loged in!"
        except:
            print "I am unable to connect to the databas"


    def insert(self, point, streetId):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO crosswalks (lat, lon, streetid) VALUES (%s, %s, %s)", (point.latitude, point.longitude, streetId))
            self.connection.commit()
            cursor.close()
        except Exception as err:
            print err

    def select(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM crosswalks")
            rows = cursor.fetchall()
            for row in rows:
                print row
            cursor.close()
        except Exception as err:
            print err

