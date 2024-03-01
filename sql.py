import sqlite3

class borne:
    def __init__(self, id, date, name, x, y, alt, city, wiki, discord_userid, discord_username, discord_email, discord_avatar, is_valid):
        self.id = id
        self.date = date
        self.name = name
        self.x = x
        self.y = y
        self.alt = alt
        self.city = city
        self.wiki = wiki
        self.discord_userid = discord_userid
        self.discord_username = discord_username
        self.discord_email = discord_email
        self.discord_avatar = discord_avatar
        self.is_valid = is_valid

class db:
    def __init__(self):
        self.conn = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
    
    def insert_borne(self, borne):
        self.cursor.execute('''
            INSERT INTO bornes (name, x, y, alt, city, wiki, discord_userid, discord_username, discord_email, discord_avatar)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (borne.name, borne.x, borne.y, borne.alt, borne.city, borne.wiki, borne.discord_userid, borne.discord_username, borne.discord_email, borne.discord_avatar))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_user_bornes(self, discord_userid):
        query = '''
            SELECT id, date, name, x, y, alt, city, wiki, description, is_valid
            FROM bornes
            WHERE discord_userid = ?
        '''
        self.cursor.execute(query, (discord_userid,))
        
        bornes = self.cursor.fetchall()
        return bornes