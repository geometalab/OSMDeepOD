class Node:
    def __init__(self):
        #<node id="265628814" version="3" timestamp="2012-11-22T21:11:23Z" uid="317694" user="daniloB" changeset="13991392" lat="47.22917" lon="8.8229775"/>
        self.ident = -1
        self.lat = -1
        self.lon = -1

    def __init__(self, ident, lat, lon):
        self.ident = ident
        self.lat = lat
        self.lon = lon
