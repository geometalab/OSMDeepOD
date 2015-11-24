from PIL import Image
import numpy as np
import glob
from random import shuffle


class Crosswalk_dataset:
    def __init__(self):
        self.sourcefolder = None
        self.folder_crosswalk = "crosswalks/"
        self.folder_nocrosswalk = "nocrosswalks/"
        self.tag_crosswalk = [1, 0]
        self.tag_nocrosswalk = [0, 1]
        self.samples_crosswalk = None
        self.samples_nocrosswalk = None
        self.samples_shuffled = None

    @classmethod
    def from_sourcefolder(cls, sourcefolder):
        set = cls()
        set.sourcefolder = sourcefolder
        return set

    @classmethod
    def from_samples(cls, samples):
        set = cls()
        set.samples_shuffled = samples
        return set

    def read_samples(self):
        self.samples_crosswalk = Categorie.from_default(self.sourcefolder + self.folder_crosswalk, self.tag_crosswalk)
        self.samples_nocrosswalk = Categorie.from_default(self.sourcefolder + self.folder_nocrosswalk, self.tag_nocrosswalk)

        self.samples_crosswalk.read_folder()
        self.samples_nocrosswalk.read_folder()

        self.samples_shuffled = self.samples_nocrosswalk.samples + self.samples_crosswalk.samples
        shuffle(self.samples_shuffled)

    def load_images(self):
        self.samples_crosswalk.load_samples()
        self.samples_nocrosswalk.load_samples()

    def split_train_test(self, train_factor):
        nb_samples = len(self.samples_shuffled)
        split_id = int(nb_samples * train_factor)

        train_samples = self.samples_shuffled[0:split_id]
        test_samples = self.samples_shuffled[split_id:nb_samples]

        train_set = Crosswalk_dataset.from_samples(train_samples)
        test_set = Crosswalk_dataset.from_samples(test_samples)
        return (train_set, test_set)

    def to_input_response(self):
        inputs = []
        responses = []
        for sample in self.samples_shuffled:
            inputs.append(sample.numpy_array)
            responses.append(sample.tag)

        return (np.asarray(inputs), np.asarray(responses))







class Categorie:
    def __init__(self):
        self.sourcefolder = ""
        self.tag = None
        self.samples = []

    @classmethod
    def from_default(cls, sourcefolder, tag):
        categorie = cls()
        categorie.sourcefolder = sourcefolder
        categorie.tag = tag
        return categorie

    def read_folder(self):
        self.samples = []
        files = glob.glob(self.sourcefolder + "*.png")
        for file in files:
            sample = Sample.from_file(file, self.tag)
            sample.load_image()
            self.samples.append(sample)

    def load_samples(self):
        for sample in self.samples:
            sample.load_image()






class Sample:
    def __init__(self):
        self.filepath = None
        self.pil_image = None
        self.tag = None
        self.numpy_array = None

    @classmethod
    def from_file(cls, path, tag):
        sample = cls()
        sample.filepath = path
        sample.tag = tag

        return sample

    def load_image(self):
        self.pil_image = self._load_image(self.filepath)
        self.numpy_array = self._to_numpy_array_normalized(self.pil_image)

    def _load_image(self, filepath):
        img = Image.open(self.filepath)
        img.load()
        img = img.convert('RGB')
        return img

    def _to_numpy_array_normalized(self, img):
        img_size = 50
        np_arr = np.asarray(img, dtype="int32")
        np_arr = np_arr.reshape(3, img_size, img_size)
        np_arr = np_arr.astype("float32")
        np_arr /= 255
        return np_arr





folderPath = "/sevi/dataset/"



def load_filelist():
    files1 = glob.glob(folderPath + "crosswalks/" + "*.png")
    files2 = glob.glob(folderPath + "nocrosswalks/" + "*.png")
    return files1 + files2

filelist = load_filelist()

def load_imagex( infilename ):
    ret = []
    img = Image.open(infilename)
    img.load()
    img = img.convert('RGB')
    data = np.asarray(img, dtype="int32")
    ret.append(data)

    return ret

def load_images(folderpath):
    datas = []
    files = glob.glob(folderpath + "*.png")
    for f in files:
        imgs = load_imagex(f)
        datas += imgs

    return np.asarray(datas)

def load_imagesY():
    path1 = folderPath + "crosswalks/"
    i1 = load_images(path1)
    return i1

def load_imagesN():
    path = folderPath + "nocrosswalks/"
    return load_images(path)

def generate_list(value, count):
    ret = []
    for i in range(count):
	ret.append(value)
    return np.asarray(ret)

def swapD(dataset, i1, i2):
    ret = dataset
    x1 = np.copy(ret[0][i1])
    y1 = np.copy(ret[1][i1])
    x2 = np.copy(ret[0][i2])
    y2 = np.copy(ret[1][i2])

    ret[0][i1] = x2
    ret[1][i1] = y2
    ret[0][i2] = x1
    ret[1][i2] = y1

    return ret

def shuffleD(dataset):
    inputs = []
    outputs = []
    sete = []
    for i in range(len(dataset[0])):
	x = dataset[0][i]
	y = dataset[1][i]
	sample = [x,y]
	sete.append(sample)

    np.random.shuffle(sete)

    for i in range(len(sete)):
	x = sete[i][0]
	y = sete[i][1]
	inputs.append(x)
	outputs.append(y)
    inputs = np.asarray(inputs)
    outputs = np.asarray(outputs)

    return (inputs, outputs)
    
    
def generate_dataset(to_shuffle=True):
    y = load_imagesY()
    yresponse = generate_list([1,0],len(y))
    print len(y), "crosswalk images loaded"
 
    n = load_imagesN()
    nresponse = generate_list([0,1],len(n))
    print len(n), "other images loaded"

    dataset = [np.concatenate((y, n), axis=0), np.concatenate((yresponse, nresponse), axis=0)]

    if(to_shuffle):
        dataset = shuffleD(dataset) # https://youtu.be/uyUXoap67N8

    return dataset

def split_set(dataset):
    factor = 0.05
    examples_count = len(dataset[0])
    testlen = int(examples_count*factor)
    print "testset length:", testlen, "of", examples_count
    testsetX = dataset[0][0:testlen]
    testsetY = dataset[1][0:testlen]

    trainsetX = dataset[0][testlen:examples_count-1]
    trainsetY = dataset[1][testlen:examples_count-1]
    return (trainsetX, trainsetY), (testsetX, testsetY)

def load_data():
    dataset = generate_dataset()
    return np.asarray(split_set(dataset))

def toPil(ndimg):
    return Image.fromarray(np.uint8(ndimg))


    





