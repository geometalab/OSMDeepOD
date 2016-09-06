# -*- coding: utf-8 -*-

# Source: http://www.swisstopo.admin.ch/internet/swisstopo/en/home/topics/survey/sys/refsys/projections.html (see PDFs under "Documentation")
# Updated 9 dec 2014
# Please validate your results with NAVREF on-line service: http://www.swisstopo.admin.ch/internet/swisstopo/en/home/apps/calc/navref.html (difference ~ 1-2m)

# Convert WGS lat/long (� dec) to CH y

def WGStoCHy(lat, lng):
    # Converts decimal degrees to sexagecimal seconds

    lat = DECtoSEX(lat)

    lng = DECtoSEX(lng)

    # Auxiliary values (% Berne)

    lat_aux = (lat - 169028.66) / 10000

    lng_aux = (lng - 26782.5) / 10000

    # Process Y

    y = (600072.37

         + 211455.93 * lng_aux

         - 10938.51 * lng_aux * lat_aux

         - 0.36 * lng_aux * lat_aux ** 2

         - 44.54 * lng_aux ** 3)

    return y


# Convert WGS lat/long (� dec) to CH x

def WGStoCHx(lat, lng):
    # Converts decimal degrees to sexagecimal seconds

    lat = DECtoSEX(lat)

    lng = DECtoSEX(lng)

    # Auxiliary values (% Bern)

    lat_aux = (lat - 169028.66) / 10000

    lng_aux = (lng - 26782.5) / 10000

    # Process X

    x = (200147.07

         + 308807.95 * lat_aux

         + 3745.25 * lng_aux ** 2

         + 76.63 * lat_aux ** 2

         - 194.56 * lng_aux ** 2 * lat_aux

         + 119.79 * lat_aux ** 3)

    return x


# Convert CH y/x to WGS lat

def CHtoWGSlat(y, x):
    # Converts military to civil and to unit = 1000km

    # Auxiliary values (% Bern)

    y_aux = (y - 600000.) / 1000000

    x_aux = (x - 200000.) / 1000000

    # Process lat

    lat = (16.9023892

           + 3.238272 * x_aux

           - 0.270978 * y_aux ** 2

           - 0.002528 * x_aux ** 2

           - 0.0447 * y_aux ** 2 * x_aux

           - 0.0140 * x_aux ** 3)

    # Unit 10000" to 1 " and converts seconds to degrees (dec)

    lat = lat * 100. / 36

    return lat


# Convert CH y/x to WGS long

def CHtoWGSlng(y, x):
    # Converts military to civil and  to unit = 1000km

    # Auxiliary values (% Bern)

    y_aux = (y - 600000.) / 1000000

    x_aux = (x - 200000.) / 1000000

    # Process long

    lng = (2.6779094

           + 4.728982 * y_aux

           + 0.791484 * y_aux * x_aux

           + 0.1306 * y_aux * x_aux ** 2

           - 0.0436 * y_aux ** 3)

    # Unit 10000" to 1 " and converts seconds to degrees (dec)

    lng = lng * 100. / 36

    return lng


# Convert decimal angle to sexagesimal seconds

def DECtoSEX(angle):
    # Extract DMS

    deg = int(angle)

    mnt = int((angle - deg) * 60)

    sec = (((angle - deg) * 60) - mnt) * 60


    # Result in seconds

    return sec + mnt * 60. + deg * 3600.;
