class Item:
    def __init__(self, name, icon, amount = 0):
        self.name = name
        self.icon = icon
        self.icon_rect = icon.get_rect()
        self.amount = amount