from enum import Enum

class Fish(Enum):
    APPLE = 1
    PEACH = 2
    BANANA = 3
    MELON = 4
    CAROTT = 5
    POTATO = 6
    BREAD = 7
    CHEESE = 8
    MILK = 9
    DONUTS = 10
    CHICKEN = 11
    MEAT = 12
    SANDWICH = 13
    NOODLES = 14
    SPAGHETTI = 15
    BURRITOS = 16
    TACOS = 17
    SUSHI = 18
    PIE = 19
    BENTO = 20

class FoodBuilder:
    pass

class Apple(FoodBuilder):
    MODIFICATION = 4
    PRICE = 5
    QUANTITY = 500
    EMOTE = "🍎"
    
class Peach(FoodBuilder):
    MODIFICATION = 4
    PRICE = 5
    QUANTITY = 500
    EMOTE = "🍑"
    
class Banana(FoodBuilder):
    MODIFICATION = 4
    PRICE = 5
    QUANTITY = 500
    EMOTE = "🍌"
    
class Melon(FoodBuilder):
    MODIFICATION = 10
    PRICE = 8
    QUANTITY = 100
    EMOTE = "🍉"
    
class Carrot(FoodBuilder):
    MODIFICATION = 8
    PRICE = 7
    QUANTITY = 150
    EMOTE = "🥕"
    
class Potato(FoodBuilder):
    MODIFICATION = 8
    PRICE = 7
    QUANTITY = 150
    EMOTE = "🥔"
    
class Bread(FoodBuilder):
    MODIFICATION = 12
    PRICE = 10
    QUANTITY = 75
    EMOTE = "🍞"
    
class Cheese(FoodBuilder): 
    MODIFICATION = 15
    PRICE = 13
    QUANTITY = 50
    EMOTE = "🧀"
    
class Milk(FoodBuilder):
    MODIFICATION = 15
    PRICE = 12
    QUANTITY = 50
    EMOTE = "🥛"
    
class Donuts(FoodBuilder):
    MODIFICATION = 18
    PRICE = 14
    QUANTITY = 40
    EMOTE = "🍩"
    
class Chicken(FoodBuilder):
    MODIFICATION = 20
    PRICE = 15
    QUANTITY = 30
    EMOTE = "🍗"
    
class Meat(FoodBuilder):
    MODIFICATION = 20
    PRICE = 15
    QUANTITY = 30
    EMOTE = "🥩"
    
class Sandwich(FoodBuilder):
    MODIFICATION = 25
    PRICE = 20
    QUANTITY = 25
    EMOTE = "🥪"
    
class Noodles(FoodBuilder):
    MODIFICATION = 30
    PRICE = 25
    QUANTITY = 20
    EMOTE = "🍜"
    
class Spaghetti(FoodBuilder):
    MODIFICATION = 30
    PRICE = 25
    QUANTITY = 20
    EMOTE = "🍝"
    
class Burrito(FoodBuilder):
    MODIFICATION = 50
    PRICE = 35
    QUANTITY = 15
    EMOTE = "🌯"
    
class Tacos(FoodBuilder):
    MODIFICATION = 50
    PRICE = 35
    QUANTITY = 15
    EMOTE = "🌮"
    
class Sushi(FoodBuilder):
    MODIFICATION = 60
    PRICE = 45
    QUANTITY = 12
    EMOTE = "🍣"
    
class Pie(FoodBuilder):
    MODIFICATION = 75
    PRICE = 50
    QUANTITY = 10
    EMOTE = "🥧"
    
class Bento(FoodBuilder):
    MODIFICATION = 100
    PRICE = 65
    QUANTITY = 5
    EMOTE = "🍱"
    
def get_foods():
    return (
        ("POMME", Apple), 
        ("PECHE", Peach), 
        ("BANANE", Banana), 
        ("MELON", Melon), 
        ("CAROTTE", Carrot), 
        ("PATATE", Potato), 
        ("PAIN", Bread), 
        ("FROMAGE", Cheese), 
        ("LAIT", Milk), 
        ("DONUTS", Donuts), 
        ("POULET", Chicken), 
        ("STEAK", Meat), 
        ("SANDWICH", Sandwich), 
        ("NOODLES", Noodles), 
        ("SPAGHETTI", Spaghetti), 
        ("BURRITO", Burrito), 
        ("TACOS", Tacos), 
        ("SUSHI", Sushi), 
        ("TARTE", Pie)
            )
