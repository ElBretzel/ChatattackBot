from enum import Enum
import math
import random

from chattattack.material import *

class Weapon(Enum):

    GRIFFE = 1
    POING_AMERICAIN = 2
    CAILLOU = 3
    FLECHETTE = 4
    SHURIKEN = 5
    TOMAHAWK = 6
    BATON = 7
    CANIF = 8
    CUTTER = 9
    POIGNARD = 10   
    DAGUE = 11
    GOURDIN = 12
    STYLET = 13
    MACHETTE = 14
    SABRE = 15
    EPEE = 16
    SERPE = 17
    HACHE = 18
    MARTEAU = 19
    HALLEBARDE = 20
    
class WeaponBuilder:
    def __init__(self, level, material, custom_stats, enchantment, durability):
        self.level = level
        self.durability = durability
        self.material = self.get_material(material)
        self.enchantment = enchantment
        self.custom_stats = custom_stats
        
    @property
    def weapon_damage(self):
        return (self.BASE*math.sqrt(self.level))+self.custom_stats[0]*random.uniform(0.25, 0.5)+self.material.material_damage
    
    @property
    def combo_attack(self):
        return random.randint(0, 100) < self.COMBO+self.custom_stats[1]
    
    @property
    def miss_attack(self):
        return random.randint(0, 100) < self.MISS
    
    def get_material(self, material):
        material_name = Material(material).name
        return get_weapons()[material_name](self.durability)
    
class Griffe(WeaponBuilder):
    BASE = 1.25
    COMBO = 50
    MAX_COMBO = 100
    MISS = 0
    def __init__(self, *args):
        super().__init__(*args)    

class PoingAmericain(WeaponBuilder):
    BASE = 0.75
    COMBO = 80
    MAX_COMBO = 5
    MISS = 5
    def __init__(self, *args):
        super().__init__(*args)    
        
class Caillou(WeaponBuilder):
    BASE = 0.25
    COMBO = 80
    MAX_COMBO = 100
    MISS = 2
    def __init__(self, *args):
        super().__init__(*args)       

class Flechette(WeaponBuilder):
    BASE = 1.0
    COMBO = 70
    MAX_COMBO = 5
    MISS = 10
    def __init__(self, *args):
        super().__init__(*args)     
        
class Shuriken(WeaponBuilder):
    BASE = 0.8
    COMBO = 80
    MAX_COMBO = 8
    MISS = 5
    def __init__(self, *args):
        super().__init__(*args)     

class Tomahawk(WeaponBuilder):
    BASE = 3
    COMBO = 30
    MAX_COMBO = 3
    MISS = 10
    def __init__(self, *args):
        super().__init__(*args)    
        
class Baton(WeaponBuilder):
    BASE = 2
    COMBO = 50
    MAX_COMBO = 3
    MISS = 15
    def __init__(self, *args):
        super().__init__(*args)    

class Canif(WeaponBuilder):
    BASE = 1.5
    COMBO = 65
    MAX_COMBO = 4
    MISS = 15
    def __init__(self, *args):
        super().__init__(*args)    
        
class Cutter(WeaponBuilder):
    BASE = 2.5
    COMBO = 50
    MAX_COMBO = 3
    MISS = 20
    def __init__(self, *args):
        super().__init__(*args)    

class Poignard(WeaponBuilder):
    BASE = 5
    COMBO = 10
    MAX_COMBO = 2
    MISS = 25
    def __init__(self, *args):
        super().__init__(*args)    

class Dague(WeaponBuilder):
    BASE = 3.5
    COMBO = 35
    MAX_COMBO = 3
    MISS = 25
    def __init__(self, *args):
        super().__init__(*args)    

class Gourdin(WeaponBuilder):
    BASE = 6
    COMBO = 0
    MAX_COMBO = 1
    MISS = 30
    def __init__(self, *args):
        super().__init__(*args)    
        
class Stylet(WeaponBuilder):
    BASE = 4
    COMBO = 35
    MAX_COMBO = 2
    MISS = 35
    def __init__(self, *args):
        super().__init__(*args)    

class Machette(WeaponBuilder):
    BASE = 5.5
    COMBO = 10
    MAX_COMBO = 2
    MISS = 35
    def __init__(self, *args):
        super().__init__(*args)    
        
class Sabre(WeaponBuilder):
    BASE = 4.5
    COMBO = 15
    MAX_COMBO = 2
    MISS = 30
    def __init__(self, *args):
        super().__init__(*args)    

class Epee(WeaponBuilder):
    BASE = 3.5
    COMBO = 35
    MAX_COMBO = 4
    MISS = 25
    def __init__(self, *args):
        super().__init__(*args)    
        
class Serpe(WeaponBuilder):
    BASE = 2.0
    COMBO = 70
    MAX_COMBO = 100
    MISS = 25
    def __init__(self, *args):
        super().__init__(*args)    

class Hache(WeaponBuilder):
    BASE = 6
    COMBO = 10
    MAX_COMBO = 2
    MISS = 35
    def __init__(self, *args):
        super().__init__(*args)    
        
class Marteau(WeaponBuilder):
    BASE = 7
    COMBO = 0
    MAX_COMBO = 1
    MISS = 55
    def __init__(self, *args):
        super().__init__(*args)    

class Hallebarde(WeaponBuilder):
    BASE = 5.5
    COMBO = 20
    MAX_COMBO = 2
    MISS = 40
    def __init__(self, *args):
        super().__init__(*args)    
        
def get_weapons():
    return (
    ("GRIFFE", Griffe), 
    ("POING_AMERICAIN", PoingAmericain), 
    ("CAILLOU", Caillou), 
    ("FLECHETTE", Flechette), 
    ("SHURIKEN", Shuriken), 
    ("TOMAHAWK", Tomahawk), 
    ("BATON", Baton), 
    ("CANIF", Canif), 
    ("CUTTER", Cutter), 
    ("POIGNARD", Poignard), 
    ("DAGUE", Dague), 
    ("GOURDIN", Gourdin), 
    ("STYLET", Stylet), 
    ("MACHETTE", Machette), 
    ("SABRE", Sabre), 
    ("EPEE", Epee), 
    ("SERPE", Serpe), 
    ("HACHE", Hache), 
    ("MARTEAU", Marteau), 
    ("HALLEBARDE", Hallebarde)
    )
    
    
if __name__ == "__main__":
    weapon_type, weapon_level, weapon_material, weapon_custom_stats, weapon_enchant, weapon_durability = 1, 1, 1, (0, 0), 0, 100
    weapon_name = Weapon(weapon_type).name
    weapon = get_weapons()[weapon_name](weapon_level, weapon_material, weapon_custom_stats, weapon_enchant, weapon_durability)
    
    combos = 0
    damages = 0
    while True:
        if weapon.miss_attack:
            break
        combos += 1
        damages += weapon.weapon_damage
        if not weapon.combo_attack or weapon.MAX_COMBO == combos:
            break
        
    print(f"Dégats: {damages}\nCombos: {combos}")
   
    
    
    
# custom stat: tuple
# tranchant
# combo (chance)