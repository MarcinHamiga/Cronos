class Item:
    def __init__(self, name, icon, amount = 1):
        self.name = name
        self.icon = icon
        if self.icon is not None:
            self.icon_rect = icon.get_rect()
        self.amount = amount
        
    def __str__(self):
        return f"Name: {self.name}, amount: {self.amount}"
    
    
    
class Item_dict:
    def __init__(self, assets):
        self.item_dict = {
            "CANDY" : Item("Candy", assets["ITEM_CANDY"]),
            "SMALL HP RESTORE" : Item("Small HP Restore", None),
            "SMALL SP RESTORE" : Item("Small SP Restore", None)
        }