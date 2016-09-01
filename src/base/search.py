from src.base.tag import Tag


class Search:
    def __init__(self, word='crosswalk', key='highway', value='crossing', zoom_level=19, compare=True):
        self.word = word
        self.tag = Tag(key=key, value=value)
        self.zoom_level = zoom_level
        self.barrier = 0.99
        self.compare = compare

    def hit(self, prediction):
        return prediction[self.word] > self.barrier
