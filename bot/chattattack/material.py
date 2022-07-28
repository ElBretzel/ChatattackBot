from enum import Enum
import math

class Material(Enum):
    PAPIER = 1
    CARTON = 2
    PLASTIQUE = 3
    VERRE = 4
    BOIS = 5
    OS = 6
    PIERRE = 7
    CUIVRE = 8
    FER = 9
    ARGENT = 10
    TITANE = 11
    OR = 12
    PLATINE = 13
    RUBIS = 14
    SAPHIR = 15
    EMERAUDE = 16
    DIAMANT = 17
    URANIUM = 18
    RADIANCE = 19
    DRAGONITE = 20
    
class MaterialBuilder:
    
    @property
    def material_damage(self):
        return self.DAMAGE * math.pow(self.durability/100, (1/3))
    
    @property
    def material_defenses(self):
        return self.DEFENSE * math.pow(self.durability/100, (1/3))
    
class Papier(MaterialBuilder):
    DAMAGE = 0.2
    DEFENSE = 0.1
    
    def __init__(self, durability):
        self.durability = durability


class Carton(MaterialBuilder):
    DAMAGE = 0.25
    DEFENSE = 0.4

    def __init__(self, durability):
        self.durability = durability
        
class Plastique(MaterialBuilder):
    DAMAGE = 0.4
    DEFENSE = 0.5

    def __init__(self, durability):
        self.durability = durability
        
class Verre(MaterialBuilder):
    DAMAGE = 0.5
    DEFENSE = 0.35

    def __init__(self, durability):
        self.durability = durability
        
class Bois(MaterialBuilder):
    DAMAGE = 0.65
    DEFENSE = 0.75

    def __init__(self, durability):
        self.durability = durability
        
class Os(MaterialBuilder):
    DAMAGE = 0.8
    DEFENSE = 1

    def __init__(self, durability):
        self.durability = durability
        
class Pierre(MaterialBuilder):
    DAMAGE = 1.2
    DEFENSE = 1.3

    def __init__(self, durability):
        self.durability = durability
        
class Cuivre(MaterialBuilder):
    DAMAGE = 1.5
    DEFENSE = 1.5

    def __init__(self, durability):
        self.durability = durability
        
class Fer(MaterialBuilder):
    DAMAGE = 2
    DEFENSE = 2.5

    def __init__(self, durability):
        self.durability = durability
        
class Argent(MaterialBuilder):
    DAMAGE = 2.3
    DEFENSE = 2.8

    def __init__(self, durability):
        self.durability = durability
        
class Titane(MaterialBuilder):
    DAMAGE = 3
    DEFENSE = 3

    def __init__(self, durability):
        self.durability = durability
        
class Or(MaterialBuilder):
    DAMAGE = 3.5
    DEFENSE = 3.2

    def __init__(self, durability):
        self.durability = durability
        
class Platine(MaterialBuilder):
    DAMAGE = 3.7
    DEFENSE = 3.5

    def __init__(self, durability):
        self.durability = durability
        
class Rubis(MaterialBuilder):
    DAMAGE = 4
    DEFENSE = 4.5

    def __init__(self, durability):
        self.durability = durability
        
class Saphir(MaterialBuilder):
    DAMAGE = 4.5
    DEFENSE = 5

    def __init__(self, durability):
        self.durability = durability
        
class Emeraude(MaterialBuilder):
    DAMAGE = 5
    DEFENSE = 5.5

    def __init__(self, durability):
        self.durability = durability
        
class Diamant(MaterialBuilder):
    DAMAGE = 5.5
    DEFENSE = 6

    def __init__(self, durability):
        self.durability = durability
        
class Uranium(MaterialBuilder):
    DAMAGE = 6.5
    DEFENSE = 6.3

    def __init__(self, durability):
        self.durability = durability
        
class Radiance(MaterialBuilder):
    DAMAGE = 7
    DEFENSE = 7

    def __init__(self, durability):
        self.durability = durability
        
class Dragonite(MaterialBuilder):
    DAMAGE = 7.5
    DEFENSE = 7.5

    def __init__(self, durability):
        self.durability = durability

def get_materials():
    return (
        ("PAPIER", Papier), 
        ("CARTON", Carton), 
        ("PLASTIQUE", Plastique), 
        ("VERRE", Verre), 
        ("BOIS", Bois), 
        ("OS", Os), 
        ("PIERRE", Pierre), 
        ("CUIVRE", Cuivre), 
        ("FER", Fer), 
        ("ARGENT", Argent), 
        ("TITANE", Titane), 
        ("OR", Or), 
        ("PLATINE", Platine), 
        ("RUBIS", Rubis), 
        ("SAPHIR", Saphir), 
        ("EMERAUDE", Emeraude), 
        ("DIAMANT", Diamant), 
        ("URANIUM", Uranium), 
        ("RADIANCE", Radiance),
        ("DRAGONITE", Dragonite)
        )