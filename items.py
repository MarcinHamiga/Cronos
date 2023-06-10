class Item:
    
    def __init__(self, name, icon, amount = 1):
        self.name = name
        self.icon = icon
        if self.icon is not None:
            self.icon_rect = icon.get_rect()
        self.amount = amount
        
    def __str__(self):
        return f"Name: {self.name}, amount: {self.amount}"
    
    
    # Wszystkie poniższe funkcje powinny zostać przeciążone w klasach pochodnych
    def use(self, target):
        pass
    
class Candy(Item):
    
    def __init__(self, name, icon, amount = 1):
        super().__init__(name, icon, amount)
    
    def use(self, target):
        pass
    
class Small_hp_restore(Item):
    
    def __init__(self, name, icon, amount = 1):
        super().__init__(name, icon, amount)
        
        
    def use(self, target):
        pass
    
class Small_sp_restore(Item):
    
    def __init__(self, name, icon, amount = 1):
        super().__init__(name, icon, amount)
        
    def use(self, target):
        pass
    
class Item_dict:
    def __init__(self, assets):
        self.item_dict = {
            "CANDY" : Item("Candy", assets["ITEM_CANDY"]),
            "SMALL HP RESTORE" : Item("Small HP Restore", assets["ITEM_SMALL_HP_RESTORE"]),
            "SMALL SP RESTORE" : Item("Small SP Restore", assets["ITEM_SMALL_SP_RESTORE"])
        }