import psycopg2

class DataHandler:

    def __init__(self):
        pass

    def connect(self):
        try:
            self.connection = psycopg2.connect("dbname='crosswalkdb' user='crosswalk' host='152.96.56.62' port='40000' password='crosswalkUser'")
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

