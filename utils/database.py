import sqlite3
import os
from datetime import datetime
from itertools import zip_longest
from functools import wraps
import random

from cachetools import TTLCache, cached

from constants import DIRECTORY
from chattattack.foods import get_foods
from chattattack.fishes import get_fishes
from chattattack.toys import get_toys


class _DBDecorators:
    # * Private class incluing all database decorators

    @classmethod
    def separator(cls, func):
        # * Create some separation during the steps of the database checking.
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("{:-^30}".format(""))
            func(*args, **kwargs)
            print("{:-^30}".format(""))
        return wrapper

    @classmethod
    def check_db_exist(cls, func):
        # * Check the integrity of the database
        # * If the database dont exist, creates a new one
        # * Rows are empty
        @wraps(func)
        def wrapper(*args, **kwargs):
            # * The first element of the arg variable is the instance of DBManager
            # * The kwargs variable contain db cursor in the 'cursor' key
            
            print("[DB] Connection...")
            if kwargs["cursor"].execute("SELECT name FROM sqlite_master WHERE type='table';").fetchone(): # ? Check if the database is not empty
                print("[DB] Database found!")
            else:
                print("[DB] Database not found...")
                print("[DB] Creation of a new database, it will not be long.")
                DBInstance = args[0] # * Assign the DBManager instance in a variable to easily access to it
                DBInstance._create_main_table
                DBInstance._create_cat_table
                DBInstance._create_weapon_table
                DBInstance._create_food_table
                DBInstance._create_fish_table
                DBInstance._create_toy_table
                DBInstance._init_shop_table
            func(*args, **kwargs)
            print("[DB] Ready!")
        return wrapper
    
    @classmethod
    def auto_commit(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            DBInstance = args[0]
            DBInstance.connexion.commit()
        return wrapper
    

class DBSingletonMeta(type):
    # *  Metaclass Singleton to have a single database connection
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance[cls] = instance
        return cls._instance[cls]
        
class DBManager(metaclass=DBSingletonMeta):
    # * Represents the whole class which control the cat database.
    # * The class is a Singleton, each instance return the same class instance.
    
    DB = sqlite3.connect(os.path.join(DIRECTORY, "catdb.db")) # ? Connection to the cat sqlite3 DB
    
    def __init__(self):
        self._connexion = self.DB
        self._cursor = self.connexion.cursor()   
        self.on_db_launch(cursor=self._cursor)            
        
    @property
    def connexion(self):
        return self._connexion
    
    @connexion.setter
    def connexion(self, *args, **kwargs):
        raise AttributeError # ! Avoid user manually create a connection
    
    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, *args, **kwargs):
        raise AttributeError  # ! Avoid user manually create a cursor
    
    
    @_DBDecorators.separator
    @_DBDecorators.check_db_exist
    @_DBDecorators.auto_commit
    def on_db_launch(self, cursor):
        print("[DB] Initialization...")
        self.cursor.execute("PRAGMA foreign_keys = ON")
    
    @property 
    @_DBDecorators.auto_commit
    def _create_main_table(self) -> None:
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS main(
                    user_id INTEGER PRIMARY KEY, 
                    money INTEGER NOT NULL DEFAULT 0, 
                    fish TEXT NOT NULL DEFAULT '5/1|', 
                    food TEXT NOT NULL DEFAULT '|', 
                    toy TEXT NOT NULL DEFAULT '|', 
                    last_daily DATETIME NOT NULL DEFAULT(datetime('now', '-1 day')), 
                    daily_streak INTEGER NOT NULL DEFAULT 0, 
                    hp INTEGER NOT NULL DEFAULT 10, 
                    main_cat INTEGER, 
                    cat_team TEXT
                    );
                    """)
        print("[DB] User table successfully created!")
        
    @property
    @_DBDecorators.auto_commit
    def _create_cat_table(self) -> None:
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS cats(
                            cat_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            user_id INTEGER NOT NULL, 
                            name TEXT NOT NULL, 
                            level INTEGER NOT NULL, 
                            furtivity TEXT NOT NULL, 
                            intelligence TEXT NOT NULL, 
                            aggressivity TEXT NOT NULL, 
                            health TEXT NOT NULL, 
                            rarity INTEGER NOT NULL, 
                            hiden_bonus INTEGER NOT NULL, 
                            affection TEXT NOT NULL, 
                            energy TEXT NOT NULL, 
                            hygien TEXT NOT NULL, 
                            sleep TEXT NOT NULL, 
                            hunger TEXT NOT NULL, 
                            wiki TEXT NOT NULL, 
                            image TEXT NOT NULL, 
                            last_care DATETIME NOT NULL, 
                            FOREIGN KEY (user_id) REFERENCES main(user_id) ON DELETE CASCADE
                        );
                        """) 
        print("[DB] Cat table successfully created!")
        
    @property
    @_DBDecorators.auto_commit
    def _create_weapon_table(self) -> None:
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS weapon(
                        weapon_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        user_id INTEGER NOT NULL, 
                        cat_id INTEGER, 
                        type INTEGER NOT NULL DEFAULT 1, 
                        level INTEGER NOT NULL DEFAULT 1, 
                        material INTEGER NOT NULL DEFAULT 1, 
                        custom_stats TEXT NOT NULL DEFAULT '0 0', 
                        enchant TEXT NOT NULL DEFAULT '0', 
                        durability INTEGER NOT NULL DEFAULT 100, 
                        FOREIGN KEY (user_id) REFERENCES main(user_id) ON DELETE CASCADE
                    )
                    """)
        print("[DB] Weapon table successfully created!")
        
    @property
    @_DBDecorators.auto_commit
    def _create_food_table(self) -> None:
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS food(
                        food_id INTEGER PRIMARY KEY, 
                        name TEXT NOT NULL, 
                        quantity INTEGER NOT NULL DEFAULT 1
                    )
                    """)
        print("[DB] Food table successfully created!")
            
    @property
    @_DBDecorators.auto_commit
    def _create_toy_table(self) -> None:
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS toy(
                        toy_id INTEGER PRIMARY KEY, 
                        name TEXT NOT NULL, 
                        quantity INTEGER NOT NULL DEFAULT 1
                    )
                    """)
        print("[DB] Toy table successfully created!")
        
    @property
    @_DBDecorators.auto_commit
    def _create_fish_table(self) -> None:
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fish(
                        fish_id INTEGER PRIMARY KEY, 
                        name TEXT NOT NULL, 
                        quantity INTEGER NOT NULL DEFAULT 1
                    )
                    """)
        print("[DB] Fish table successfully created!") 
        
    def __get_quantity(self, base, index):
            is_in_sale = random.choice([0, 1])
            shortage = random.choice([1, 1.2, 1.5, 2, 3, 5]) 
            return base // shortage if is_in_sale or not index else 0
        
    @property
    def _init_shop_table(self) -> None:
        for i, (food, fish, toy) in enumerate(zip_longest(get_foods(), get_fishes(), get_toys())):
            if food:
                self.cursor.execute("""
                                    INSERT INTO food (name, quantity)
                                    VALUES (?, ?)
                                    """, (food[0], self.__get_quantity(food[1].QUANTITY, i)))
            if fish:
                self.cursor.execute("""
                                    INSERT INTO fish (name, quantity)
                                    VALUES (?, ?)
                                    """, (fish[0], self.__get_quantity(fish[1].QUANTITY, i)))
            if toy:
                self.cursor.execute("""
                                    INSERT INTO toy (name, quantity)
                                    VALUES (?, ?)
                                    """, (toy[0], self.__get_quantity(toy[1].QUANTITY, i)))
            self.connexion.commit()
        print("[DB] Shop items created!") 
    
    @cached(cache=TTLCache(maxsize=1024, ttl=60))
    def check_if_user_exists(self, user_id: int) -> bool:
        self.cursor.execute("""
                    SELECT EXISTS(
                        SELECT 1
                        FROM main
                        WHERE user_id = ?
                    );
                    """, (user_id, ))
        return self.cursor.fetchone()[0]

    @_DBDecorators.auto_commit
    def add_user(self, user_id: int) -> None:
        
        self.cursor.execute("""
            SELECT EXISTS(
                SELECT 1
                FROM main
                WHERE user_id = ?
            );
            """, (user_id, ))
        
        if self.cursor.fetchone()[0]:
            return 1
        
        self.cursor.execute("""
                    INSERT INTO main(user_id)
                    VALUES (?)
                    """, (user_id, ))

    @_DBDecorators.auto_commit
    def add_cat(self, *args, **kwargs) -> None:
        now_ = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S") # ? Database format
        self.cursor.execute("""
                    INSERT INTO cats (user_id, name, level, furtivity, intelligence, aggressivity, health, rarity, hiden_bonus, affection, energy, hygien, sleep, hunger, wiki, image, last_care)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (args[0], args[1], kwargs["level"], kwargs["furtivity"], kwargs["intelligence"], kwargs["aggressivity"], kwargs["health"], kwargs["rarity"], kwargs["hiden_bonus"], kwargs["affection"], kwargs["energy"], kwargs["hygien"], kwargs["sleep"], kwargs["hunger"], kwargs["wiki"], kwargs["image"], now_))
        
    def get_last_user_cat(self, user_id: int) -> int:
        self.cursor.execute("""
                    SELECT cat_id
                    FROM cats
                    WHERE user_id = ?
                    ORDER BY cat_id DESC
                    LIMIT 1
                    """, (user_id, ))
        return self.cursor.fetchone()[0]
        
    @_DBDecorators.auto_commit
    def set_cat_weapon(self, user_id: int) -> None:
        cat_id = self.get_last_user_cat(user_id)
        self.cursor.execute("""
                    INSERT INTO weapon (user_id, cat_id)
                    VALUES (?, ?)
                    """, (user_id, cat_id))

    @cached(cache=TTLCache(maxsize=1024, ttl=60))
    def get_all_user_cat(self, user_id: int) -> list:
        self.cursor.execute("""
                    SELECT name, level, rarity, cat_id
                    FROM cats
                    WHERE user_id = ?
                    ORDER BY rarity DESC, level DESC
                    """, (user_id, ))
        return self.cursor.fetchall()

    @cached(cache=TTLCache(maxsize=1024, ttl=60))
    def get_info_cat(self, user_id: int, cat_id: int) -> tuple:
        self.cursor.execute("""
                    SELECT *
                    FROM cats
                    WHERE cat_id = ? AND user_id = ?
                    """, (cat_id, user_id))
        return self.cursor.fetchone()

    @_DBDecorators.auto_commit
    def delete_user(self, user_id: int) -> None:
        self.cursor.execute("""
                    DELETE FROM main
                    WHERE user_id = ?;
                    """, (user_id, ))
        
    @_DBDecorators.auto_commit
    def update_cat_stat(self, cat_id: int, last_care: datetime, **kwargs) -> None:
        self.cursor.execute("""
                    UPDATE cats
                    SET affection = ?, energy = ?, hygien = ?, sleep = ?, hunger = ?, last_care = ?
                    WHERE cat_id = ?
                    """, (kwargs["affection"], kwargs["energy"], kwargs["hygien"], kwargs["sleep"], kwargs["hunger"], last_care.replace(tzinfo = None).strftime(r"%Y-%m-%d %H:%M:%S"), cat_id))
    
    def user_get_money(self, user_id: int) -> int:
        self.cursor.execute("""
                    SELECT money
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return self.cursor.fetchone()[0]
        
    @_DBDecorators.auto_commit
    def user_add_money(self, user_id: int, amount: int) -> None:
        amount += self.user_get_money(user_id)
        self.cursor.execute("""
                    UPDATE main
                    SET money = ?
                    WHERE user_id = ?
                    """, (amount, user_id))
        
    def __reformat_db_separator(self, **kwargs) -> str:

        add_object = kwargs["add"]
        objects = kwargs["values"]

        # ? Adding the object to the list of existing objects
        # ? If the object already exist, do the sum with the existing object
        # ? If the object dont exist, adding to the list of objects
        # ? If the objects list is empty, return the object
        # ! The separator between number and id is '/'
        # ! The separator between objects is '|'

        if objects:
            amount_add, id_add = add_object.split("/")
            final_object = []

            for obj in objects.split("|"):

                if not obj:
                    if id_add not in [i.split("/")[1] for i in ''.join(final_object).split("|") if i]:
                        final_object.append(f"{add_object}|")
                    break
                
                if obj.split("/")[1] == id_add: # * Old object
                    final_object.append(f"{max(int(obj.split('/')[0])+int(amount_add), 0)}/{obj.split('/')[1]}|") # * Sum of the objects
                elif obj.split("/")[1] in [i.split("/")[1] for i in objects.split("|") if i]: # * New object and id already exists
                    final_object.append(f"{obj}|") # * Add already existed object

            return ''.join(final_object)

        return f"{add_object}|" 
        
    def user_get_fish(self, user_id: int) -> str:
        self.cursor.execute("""
                    SELECT fish
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return self.cursor.fetchone()[0]

    @_DBDecorators.auto_commit
    def user_add_fish(self, user_id: int, fish: str) -> None:
        fishes = self.user_get_fish(user_id)
        data = self.__reformat_db_separator(add=fish, values=fishes)
      
        self.cursor.execute("""
                    UPDATE main
                    SET fish = ?
                    WHERE user_id = ?
                    """, (data, user_id))
        
    def user_get_food(self, user_id: int) -> str:
        self.cursor.execute("""
                    SELECT food
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return self.cursor.fetchone()[0]

    @_DBDecorators.auto_commit
    def user_add_food(self, user_id: int, food: str) -> None:
        foods = self.user_get_food(user_id)
        data = self.__reformat_db_separator(add=food, values=foods)
        
        self.cursor.execute("""
                    UPDATE main
                    SET food = ?
                    WHERE user_id = ?
                    """, (data, user_id))
        
    def user_get_toy(self, user_id: int) -> str:
        self.cursor.execute("""
                    SELECT toy
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return self.cursor.fetchone()[0]

    @_DBDecorators.auto_commit
    def user_add_toy(self, user_id: int, toy: str) -> None:
        toys = self.user_get_toy(user_id)
        data = self.__reformat_db_separator(add=toy, values=toys)

        self.cursor.execute("""
                    UPDATE main
                    SET toy = ?
                    WHERE user_id = ?
                    """, (data, user_id))
    
    def user_get_streak(self, user_id: int) -> int:
        self.cursor.execute("""
                    SELECT daily_streak
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return self.cursor.fetchone()[0]

    @_DBDecorators.auto_commit
    def user_add_streak(self, user_id: int, streak: int) -> None:
        self.cursor.execute("""
                    UPDATE main
                    SET daily_streak = ?
                    WHERE user_id = ?
                    """, (streak + 1, user_id))
    
    @_DBDecorators.auto_commit    
    def user_reset_streak(self, user_id: int) -> None:
        self.cursor.execute("""
                    UPDATE main
                    SET daily_streak = 0
                    WHERE user_id = ?
                    """, (user_id, ))
    
    def user_get_daily(self, user_id: int) -> datetime:
        self.cursor.execute("""
                    SELECT last_daily
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return datetime.strptime(self.cursor.fetchone()[0], r"%Y-%m-%d %H:%M:%S") # ? Database format

    @_DBDecorators.auto_commit
    def user_set_daily(self, user_id: int) -> None:
        now_ = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S") # ? Database format
        self.cursor.execute("""
                    UPDATE main
                    SET last_daily = ?
                    WHERE user_id = ?
                    """, (now_, user_id))
    
    def user_get_maincat(self, user_id: int) -> tuple:
        self.cursor.execute("""
                    SELECT main_cat
                    FROM main
                    WHERE user_id = ?
                    """, (user_id, ))
        return self.cursor.fetchone()   

    @_DBDecorators.auto_commit
    def user_set_maincat(self, user_id: int, cat_id: int) -> None:
        self.cursor.execute("""
                    UPDATE main
                    SET main_cat = ?
                    WHERE user_id = ?
                    """, (cat_id, user_id))
        
    @_DBDecorators.auto_commit
    def user_set_catname(self, user_id: int, cat_id: int, name: str) -> None:
        self.cursor.execute("""
                    UPDATE cats
                    SET name = ?
                    WHERE cat_id = ? AND user_id = ?
                    """, (name, cat_id, user_id))
        
    def reset_stocks(self):
        for i, (food, fish, toy) in enumerate(zip_longest(get_foods(), get_fishes(), get_toys())):
            if food:
                self.cursor.execute("""
                                    UPDATE food
                                    SET quantity = ?
                                    WHERE name = ?
                                    """, (self.__get_quantity(food[1].QUANTITY, i), food[0]))
            if fish:
                self.cursor.execute("""
                                    UPDATE fish
                                    SET quantity = ?
                                    WHERE name = ?
                                    """, (self.__get_quantity(fish[1].QUANTITY, i), food[0]))
            if toy:
                self.cursor.execute("""
                                    UPDATE toy
                                    SET quantity = ?
                                    WHERE name = ?
                                    """, (self.__get_quantity(toy[1].QUANTITY, i), food[0]))
            self.connexion.commit()
        print("[DB] Shop items restocked!")
        
    
    def get_food_stock(self):
        self.cursor.execute("""
                            SELECT *
                            FROM food
                            """)
        return self.cursor.fetchall()
    
    def get_fish_stock(self):
        self.cursor.execute("""
                            SELECT *
                            FROM fish
                            """)
        return self.cursor.fetchall()
    
    def get_toy_stock(self):
        self.cursor.execute("""
                            SELECT *
                            FROM toy
                            """)
        return self.cursor.fetchall()
    
    @_DBDecorators.auto_commit
    def add_food_stock(self, quantity, id_):
        print("adding food")
        updated_quantity = self.get_food_stock()[id_-1][2]
        print(updated_quantity, quantity, max(updated_quantity + quantity, 0))
        
        self.cursor.execute("""
                            UPDATE food
                            SET quantity = ?
                            WHERE food_id = ?
                            """, (max(updated_quantity + quantity, 0), id_))
        self.connexion.commit()
        
    @_DBDecorators.auto_commit
    def add_fish_stock(self, quantity, id_):
        updated_quantity = self.get_fish_stock()[id_-1][2]
        
        self.cursor.execute("""
                            UPDATE fish
                            SET quantity = ?
                            WHERE fish_id = ?
                            """, (max(updated_quantity + quantity, 0), id_))
        
    @_DBDecorators.auto_commit
    def add_toy_stock(self, quantity, id_):
        updated_quantity = self.get_toy_stock()[id_-1][2]
        
        self.cursor.execute("""
                            UPDATE toy
                            SET quantity = ?
                            WHERE toy_id = ?
                            """, (max(updated_quantity + quantity, 0), id_))
        
        


if __name__ == "__main__":
    
    s1 = DBManager()
    s2 = DBManager()
    print(id(s1), id(s2))
