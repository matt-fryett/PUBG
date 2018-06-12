class item():
    def __init__(self,id,stack,category,subCategory,attached):
        self.id = id
        self.stack = int(stack)
        self.category = category
        self.subCategory = subCategory
        self.attached = attached[1:-1].split(",")
        #print(self.attached)