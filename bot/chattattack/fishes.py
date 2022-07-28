from enum import Enum

class Fish(Enum):
    BAR = 1
    POISSON_CLOWN = 2
    POISSON_GLOBE = 3
    CREVETTE = 4
    CRABE = 5
    CALAMARD = 6
    HOMARD = 7
    POULPE = 8
    
class FishBuilder:
    pass
    # TODO enlever de la db ici

class Bar(FishBuilder):
    MODIFICATION = 1.0
    PRICE = 2
    EMOTE = "🐟"
    QUANTITY = 1000
    
class Clown(FishBuilder):
    MODIFICATION = 1.05
    PRICE = 5
    EMOTE = "🐠"
    QUANTITY = 500
    
class Globe(FishBuilder):
    MODIFICATION = 1.1
    PRICE = 8
    EMOTE = "🐡"
    QUANTITY = 400
    
class Crevette(FishBuilder):
    MODIFICATION = 1.15
    PRICE = 12
    EMOTE = "🦐"
    QUANTITY = 350
    
class Crabe(FishBuilder):
    MODIFICATION = 1.2
    PRICE = 15
    EMOTE = "🦀"
    QUANTITY = 250
    
class Calamard(FishBuilder):
    MODIFICATION = 1.4
    PRICE = 30
    EMOTE = "🦑"
    QUANTITY = 100
    
class Homard(FishBuilder):
    MODIFICATION = 1.7
    PRICE = 50
    EMOTE = "🦞"
    QUANTITY = 50
    
class Poulpe(FishBuilder):
    MODIFICATION = 2.0
    PRICE = 75
    EMOTE = "🐙"
    QUANTITY = 25

def get_fishes():
    return (
        ("BAR", Bar), 
        ("POISSON_CLOWN", Clown), 
        ("POISSON_GLOBE", Globe), 
        ("CREVETTE", Crevette), 
        ("CRABE", Crabe), 
        ("CALAMARD", Calamard), 
        ("HOMARD", Homard), 
        ("POULPE", Poulpe)
            )