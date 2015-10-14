

class SampleData:
    def __init__(self, complexFrequencie, isCrosswalk):
        self.complexFrequencie = complexFrequencie
        self.isCrosswalk = isCrosswalk
        self.convert()

    def convert(self):
        self.input = []
        maxSize = 2000.0
        inputSize = 20
        count = 0
        for x in self.complexFrequencie:
            value = abs(x)/maxSize
            self.input.append(value)
            count += 1
            if(count > inputSize): break

    def save(self, filename):
        if(len(self.input) < 1): raise Exception("Inputlength smaller 1")
        line = ""
        for x in self.input:
            line += str(x) + ";\n"

        line += str(self.isCrosswalk) + ";"
        with open("Output.txt", "aw") as myfile:
            myfile.write(line)




