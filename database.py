import sqlite3


class Database(object):
    
    def __init__(self):
        self.connection = sqlite3.connect('Cars.db')
        self.cursor = self.connection.cursor()
        
        
        
    def insert_data(self, number, description, status, comment=None):
        self.cursor.execute('''INSERT INTO car VALUES(?,?,?,?)''', (number, description, status,comment))
        self.connection.commit()
        
    
    def get_last_number(self, status):
        return self.cursor.execute('''SELECT number FROM car WHERE status = ?''', (status,)).fetchall()[0][-1]
    
    
    def get_description(self, number):
        return self.cursor.execute('''SELECT description FROM car WHERE number = ?''', (number,)).fetchall()[0]
    
    def update_description(self, description, number):
        self.cursor.execute('''UPDATE car SET description = ? WHERE number = ?''', (description, number))
        self.connection.commit()
    
    def get_data(self, status):
        return self.cursor.execute('''SELECT DISTINCT number, description, comment FROM car WHERE status = ?''', (status,)).fetchall()
    
    def update_line(self, number, status):
        self.cursor.execute('''UPDATE car SET status = ? WHERE number = ?''', (number, status,))
        self.connection.commit()
        
    def insert_comment(self, number, comment):
        self.cursor.execute('''UPDATE car SET comment = ? WHERE number = ?''', (comment, number))
        self.connection.commit()
        