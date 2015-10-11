
class Constants:

    '''
    zoomCorrection:
    ###############################
    Bigger correction --> Sharpen image
    Lower correction --> zoom out
    Tested factors: 4, 2, 1, 0.5, 0.25, 0.125
    Max possible is 4
    4 for Recognition
    '''
    zoomCorrection = 0.5
    PIXEL_TILE19 = 350
    METER_PER_PIXEL = 0.404428571 / zoomCorrection
    TILE19_DISTANCE = METER_PER_PIXEL * PIXEL_TILE19
    squaredImage_PixelPerSide = 80



    if(zoomCorrection > 4):
        print "Max zoom correction is 4. Bigger is not supported by Microsoft Bing"
        zoomCorrection = 4