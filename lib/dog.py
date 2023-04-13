import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        
        self.id = CURSOR.execute("SELECT last_insert_rowid()").fetchone()[0]
        
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        new_dog = cls(row[1], row[2])
        new_dog.id = row[0]
        return new_dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        CURSOR.execute(sql)
        return [cls.new_from_db(row) for row in CURSOR.fetchall()]
    
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        result = CURSOR.execute(sql, (name,))
        row = result.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None
    
    @classmethod
    def find_by_id(cls, name):
        sql = """
            select * from dogs
            WHERE id=?
        """
        CURSOR.execute(sql, (name,))
        return cls.new_from_db(CURSOR.fetchone())
    
    @classmethod
    def find_by_breed(cls, name):
        sql = """
            select * from dogs
            WHERE breed=?
        """
        CURSOR.execute(sql, (name,))
        return cls.new_from_db(CURSOR.fetchone())
    
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog and dog.breed == breed:
            return dog
        else:
            return cls.create(name, breed)
        
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
    
    
