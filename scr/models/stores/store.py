class Store(object):
    def __init__(self,name,url_prefix):
        self.url_prefix = url_prefix
        self.name = name

    def __repr__(self):
        return "<Store {}>".format(self.name)