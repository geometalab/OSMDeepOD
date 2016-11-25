class Tag:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return self.key + "=" + self.value
