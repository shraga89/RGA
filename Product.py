class Product:
    def __init__(self, name):
        self.name = name


class DataProduct(Product):

    def __init__(self, name, domain, number_of_examples, number_of_features, additional_features):
        super(DataProduct, self).__init__(name)
        self.domain = domain
        self.number_of_examples = number_of_examples
        self.number_of_features = number_of_features
        self.additional_features = additional_features

    def __hash__(self):
        return hash((self.name,self.domain))

    def __eq__(self, other):
        return self.name == other.name and self.domain == other.domain


    def __str__(self):
        return self.name+" - "+self.domain