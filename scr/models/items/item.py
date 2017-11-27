class Item(object):
    def __init__(self, name, price, url):
        self.url = url
        self.price = price
        self.name = name

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)
