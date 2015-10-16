
class Constants:

    '''
    zoomCorrection:
    ###############################
    Bigger correction --> Sharpen image
    Lower correction --> zoom out
    Tested factors: 4, 2, 1, 0.5, 0.25, 0.125
    Max possible is 4
    2 for Recognition
    4 is zoom 20 (Not always possible)
    2 is zoom 19
    1 is zoom 18
    '''
    zoomCorrection = 2
    PIXEL_TILE19 = 350
    METER_PER_PIXEL = 0.404428571 / zoomCorrection
    TILE19_DISTANCE = METER_PER_PIXEL * PIXEL_TILE19
    squaredImage_PixelPerSide = 50

    TILE19_DISTANCE_LON = 0.00094
    TILE19_DISTANCE_LAT = 0.000638

    RANGE_TO_NODE = 5 #Distance in Meter

    SerializationFolder = "/home/osboxes/Documents/OSM-Crosswalk-Detection/tests/serializedProxies/"


    if(zoomCorrection > 4):
        print "Max zoom correction is 4. Bigger is not supported by Microsoft Bing"
        zoomCorrection = 4