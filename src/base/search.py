from src.base.tag import Tag


class Search:
    def __init__(self, word='crosswalk', tag=Tag(key='highway', value='crossing')):
        self.word = word
        self.tag = tag
        self.barrier = 0.99

    def hit(self, prediction):
        return prediction[self.word] > self.barrier