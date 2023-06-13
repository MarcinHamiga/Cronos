class Item:
    
    def __init__(self, name, icon, amount=1):
        self.name = name
        self.icon = icon
        if self.icon is not None:
            self.icon_rect = icon.get_rect()
        self.amount = amount
        
    def __str__(self):
        return f"Name: {self.name}, amount: {self.amount}"

    
class Candy(Item):
    
    def __init__(self, icon, amount=1):
        super().__init__("Candy", icon, amount)
    
    def use(self, target):
        if target.check_if_down():
            target.revive()
            self.amount -= 1

    
class Small_hp_restore(Item):
    
    def __init__(self, icon, amount=1):
        super().__init__("Small HP restore", icon, amount)

    def use(self, target):
        target.heal(50)
        self.amount -= 1

    
class Small_sp_restore(Item):
    
    def __init__(self, icon, amount=1):
        super().__init__("Small SP restore", icon, amount)
        
    def use(self, target):
        target.recover_sp(10)
        self.amount -= 1


class Item_dict:
    def __init__(self, assets):
        self.item_dict = {
            "CANDY": Candy(assets["ITEM_CANDY"]),
            "SMALL HP RESTORE": Small_hp_restore(assets["ITEM_SMALL_HP_RESTORE"]),
            "SMALL SP RESTORE": Small_sp_restore(assets["ITEM_SMALL_SP_RESTORE"])
        }