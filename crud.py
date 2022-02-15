import sqlite3
import os
    
class CRUD:
    def __init__(self):
        #Cria um Banco de Dados caso não exista
        self.CreateDB()

    #Insere valores recebidos
    def Insert(exec:str,insert:tuple)->None:
        
        try:
            with sqlite3.connect('db/ComplaintDB.db') as db:
                cur = db.cursor()
                cur.execute(exec,insert)
                db.commit()

        except Exception:
            return Exception

    #Cria o DB e as suas tabelas
    def CreateDB(self)->None:
        try:
            if not os.path.exists('.\db'):
                os.makedirs('.\db')
            with sqlite3.connect("db/ComplaintDB.db") as db:
                query = """CREATE TABLE IF NOT EXISTS Complaint(
                    id TEXT UNIQUE,
                    Title TEXT DEFAULT '',
                    Company TEXT DEFAULT '',
                    Local TEXT DEFAULT '',
                    Date TEXT DEFAULT '',
                    Complaint TEXT DEFAULT '',
                    Status TEXT DEFAULT ''
                    );"""
               
                db.execute(query)
                db.commit()

        except Exception:
            print(Exception)


if __name__ =='__main__':
    CRUD()