import sqlite3

con = sqlite3.connect('highscore.db')
cur = con.cursor()
try:
    cur.execute("""CREATE TABLE HighScore(
                Name TEXT,
                Wave INTEGER,
                Kills INTEGER
                )""")
except:
    pass

con.commit()
def insert_score(score):
    with con:
        cur.execute('INSERT INTO HighScore VALUES (:Name,:Wave,:Kills)',{'Name': score.Name, 'Wave':score.Wave, 'Kills': score.Kills})
    con.commit()
def PrintOut():
    cur.execute('SELECT Name, Wave, Kills FROM HighScore')
    return cur.fetchall()
con.close()

class score():
    def __init__(self,Name, Wave, Kills):
        self.Name = Name 
        self.Wave = Wave 
        self.Kills = Kills