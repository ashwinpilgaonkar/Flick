import sqlite3

class dbOperation():
    db = sqlite3.connect('SavedGestures.db')

    def __init__(self):
        print ("Opened database successfully")

    def create(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS Gestures (ID INT, Name TEXT, Shortcut TEXT);''')

    def insert(self, ID, Name, Shortcut):
        self.db.execute("INSERT INTO Gestures (ID, Name, Shortcut) \
              VALUES (?, ?, ? )", (ID, Name, Shortcut));

        self.db.commit()

    def read(self):
        cursor = self.db.execute("SELECT ID, Name, Shortcut from Gestures")
        counter = 0
        for row in cursor:
            print ("ID = ", row[0])
            print ("NAME = ", row[1])
            print ("SHORTCUT = ", row[2], "\n")
            counter = counter + 1

        return counter

    def delete(self):
        self.db.execute("DELETE from Gestures where ID=1;")
        self.db.commit()

    def close(self):
        self.db.close()

def main():
    dbOp = dbOperation()
    dbOp.create()
    dbOp.insert(1, "ASD", "QWE")
    dbOp.delete()
    dbOp.read()
    dbOp.close()

if __name__ == '__main__':
    main()