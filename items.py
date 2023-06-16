import random

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

    
class SmallHPRestore(Item):
    
    def __init__(self, icon, amount=1):
        super().__init__("Small HP restore", icon, amount)

    def use(self, target):
        if not target.check_if_down() and target.health != target.max_health:
            target.heal(50)
            self.amount -= 1


class HPRestore(Item):

    def __init__(self, icon, amount=1):
        super().__init__("HP restore", icon, amount)

    def use(self, target):
        if not target.check_if_down() and target.health != target.max_health:
            target.heal(100)
            self.amount -= 1


class SmallSPRestore(Item):
    
    def __init__(self, icon, amount=1):
        super().__init__("Small SP restore", icon, amount)
        
    def use(self, target):
        if not target.check_if_down() and target.special_points != target.max_special_points:
            target.recover_sp(10)
            self.amount -= 1


class SPRestore(Item):

    def __init__(self, icon, amount=1):
        super().__init__("SP Restore", icon, amount)

    def use(self, target):
        if not target.check_if_down() and target.special_points != target.max_special_points:
            target.recover_sp(25)
            self.amount -= 1


class Catcher(Item):

    def __init__(self, icon, amount=1):
        super().__init__("Catcher", icon, amount)

    def use(self, target):
        self.amount -= 1
        if int(target.health / target.max_health * 100) < 40:
            roll = random.randint(0, 100)
            if roll < 60:
                return True
            else:
                return False
        return False


class Item_dict:
    def __init__(self, assets):
        self.item_dict = {
            "CANDY": Candy(assets["ITEM_CANDY"]),
            "SMALL HP RESTORE": SmallHPRestore(assets["ITEM_SMALL_HP_RESTORE"]),
            "SMALL SP RESTORE": SmallSPRestore(assets["ITEM_SMALL_SP_RESTORE"]),
            "HP RESTORE": HPRestore(assets["ITEM_HP_RESTORE"]),
            "SP RESTORE": SPRestore(assets["ITEM_SP_RESTORE"]),
            "CATCHER": Catcher(assets["ITEM_CANDY"])
        }