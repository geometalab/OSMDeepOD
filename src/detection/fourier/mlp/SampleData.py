

class SampleData:
    def __init__(self):
        self.fourier2d = None
        self.isCrosswalk = False

    @classmethod
    def fromAbsoluteFourier2d(cls, fourier2d, isCrosswalk = False):
        data = cls()
        data.fourier2d = fourier2d
        data.isCrosswalk = isCrosswalk
        return data



    def getInputArray(self):
        input = []
        for rows in self.fourier2d:
            for value in rows:
                input.append(value)
        return input

    def getNormalizedInputArray(self):
        max = 10000
        input = self.getInputArray()
        for i in range(len(input)):
            input[i] = input[i]/max
        return input


    def getOutputArray(self):
        if(self.isCrosswalk):
            return [1]
        else:
            return [0]



