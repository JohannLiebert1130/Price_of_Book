class Store(object):
    def __init__(self, name, url_prefix, tag_name, query):
        self.tag_name = tag_name
        self.url_prefix = url_prefix
        self.name = name
        self.query = query

    def __repr__(self):
        return "<Store {}>".format(self.name)