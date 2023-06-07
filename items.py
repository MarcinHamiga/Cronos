class Item:
    def __init__(self, name, icon, amount = 0):
        self.name = name
        self.icon = icon
        if self.icon is not None:
            self.icon_rect = icon.get_rect()
        self.amount = amount
        
    def __str__(self):
        return f"Name: {self.name}, amount: {self.amount}"