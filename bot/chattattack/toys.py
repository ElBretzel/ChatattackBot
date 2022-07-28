from enum import Enum

class Toy:
    DE = 1
    BALLON = 2
    FILS = 3
    YO_YO = 4
    NOUNOURS = 5
    PEINTURE = 6
    PUZZLE = 7
    ECHEC = 8
    CONSOLE = 9
    TELESCOPE = 10
    
class ToyBuilder:
    pass
    # TODO enlever de la db ici

class De(ToyBuilder):
    MODIFICATION = 5
    PRICE = 5
    QUANTITY = 500
    EMOTE = "🎲"
    
class Ballon(ToyBuilder):
    MODIFICATION = 10
    PRICE = 10
    QUANTITY = 250
    EMOTE = ":balloon:"
    
class Fils(ToyBuilder):
    MODIFICATION = 12
    PRICE = 12
    QUANTITY = 100
    EMOTE = "🧶"
    
class Yoyo(ToyBuilder):
    MODIFICATION = 15
    PRICE = 14
    QUANTITY = 75
    EMOTE = ":yo_yo:"
    
class Nounours(ToyBuilder):
    MODIFICATION = 20
    PRICE = 18
    QUANTITY = 65
    EMOTE = "🧸"
    
class Peinture(ToyBuilder):
    MODIFICATION = 25
    PRICE = 22
    QUANTITY = 50
    EMOTE = ":art:"
    
class Puzzle(ToyBuilder):
    MODIFICATION = 35
    PRICE = 28
    QUANTITY = 25
    EMOTE = "🧩"
    
class Echec(ToyBuilder):
    MODIFICATION = 45
    PRICE = 34
    QUANTITY = 15
    EMOTE = "♟"
    
class Console(ToyBuilder):
    MODIFICATION = 75
    PRICE = 44
    QUANTITY = 10
    EMOTE = "🕹"
    
class Telescope(ToyBuilder):
    MODIFICATION = 100
    PRICE = 56
    QUANTITY = 5
    EMOTE = "🔭"
    
def get_toys():
    return (
        ("DE", De), 
        ("BALLON", Ballon), 
        ("FILS", Fils), 
        ("YO_YO", Yoyo), 
        ("NOUNOURS", Nounours), 
        ("PEINTURE", Peinture), 
        ("PUZZLE", Puzzle), 
        ("ECHEC", Echec), 
        ("CONSOLE", Console), 
        ("TELESCOPE", Telescope)
            )
