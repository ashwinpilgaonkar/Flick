import sqlite3

class dbOperation():
    db = sqlite3.connect('SavedGestures.db')
    counter = 0

    def __init__(self):
        print ("Opened database successfully")

    def create(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS Gestures (ID INT, Name TEXT, Shortcut TEXT,
        F1X FLOAT, F1Y FLOAT, F1Z FLOAT,
        F2X FLOAT, F2Y FLOAT, F2Z FLOAT,
        F3X FLOAT, F3Y FLOAT, F3Z FLOAT,
        F4X FLOAT, F4Y FLOAT, F4Z FLOAT,
        F5X FLOAT, F5Y FLOAT, F5Z FLOAT);''')

    def insert(self, ID, Name, Shortcut, F1X, F1Y, F1Z, F2X, F2Y, F2Z, F3X, F3Y, F3Z, F4X, F4Y, F4Z, F5X, F5Y, F5Z):
        self.db.execute("INSERT INTO Gestures (ID, Name, Shortcut, F1X, F1Y, F1Z, F2X, F2Y, F2Z, F3X, F3Y, F3Z, F4X, F4Y, F4Z, F5X, F5Y, F5Z) \
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ID, Name, Shortcut, F1X, F1Y, F1Z, F2X, F2Y, F2Z, F3X, F3Y, F3Z, F4X, F4Y, F4Z, F5X, F5Y, F5Z))

        self.db.commit()

    def read(self):
        cursor = self.db.execute("SELECT ID, Name, Shortcut from Gestures")
        self.counter=0
        items = list()
        for row in cursor:
            #print ("ID = ", row[0])
            #print ("NAME = ", row[1])
            #print ("SHORTCUT = ", row[2], "\n")
            self.counter = self.counter + 1
            items.append(row[0])
            items.append(row[1])
            items.append(row[2])

        return items

    def getCount(self):
        return self.counter

    def delete(self, ID):
        self.db.execute("DELETE from Gestures where ID=?;", (ID))
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