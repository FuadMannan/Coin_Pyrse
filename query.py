class Query:
    
    def __init__(self, name, filter_list):
        self.name = name
        self.filter_list = filter_list
        
    def add_filter(self, search_filter):
        self.filter_list.append(search_filter)

    def remove_filter(self, search_filter):
        self.filter_list.remove(search_filter)
