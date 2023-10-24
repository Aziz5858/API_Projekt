from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import uvicorn
import psycopg2
import os
import sys
from datetime import datetime


#pydantic Datenmodelle

#Bücher klassen

class Buch(BaseModel):
    id: int
    titel: str
    autor: str
    erscheinungsjahr: int
    herausgeber: str
    seitenanzahl: int
    preis: float
    auf_lager: bool


class E_Book(BaseModel):
    id: int
    titel: str
    autor: str
    erscheinungsjahr: int
    herausgeber: str
    seitenanzahl: int
    preis: float


class Film(BaseModel):
    id: int
    titel: str
    produzent: str
    erscheinungsjahr: int
    seitenanzahl: int
    preis: float
    auf_lager: bool




#Cafe Klassen

class Americano(BaseModel):
    id: int
    preis: float
    
    

class Apfelschorle(BaseModel):
    id: int
    preis: float
    
    

class Latte(BaseModel):
    id: int
    preis: float
   
    

class Limonade(BaseModel):
    id: int
    preis: float
    
    

class Backstock(BaseModel):
    id: int
    kuhmilch: int
    hafermilch: int
    kaffebohnen: int
    limonade: int
    apfelschorle: int
    wasser: int



use_reload = "--reload"in sys.argv 



# App erstellen

app = FastAPI(title="Bücher_Cafe_API",
              description="Made by Gruppe 4",
              version="1.0")





# Funktion zum SQL-Verbindung generieren

def get_con():
    conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password=os.environ['DB_PASSWORD'],
    database="Bücher-Datenbank")
    return conn



def get_con_cafe():
    conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password=os.environ['DB_PASSWORD'],
    database="Cafe-Datenbank")
    return conn



@app.get("/")
def grueße():
    return "Hallo Bücherwurm!"



# ENDPUNKTE BUCH


#alle Bücher ausgeben
@app.get("/buch")
def get_all_entries(con=Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("select * from buch")
    books = cursor.fetchall()
    cursor.close()
    return books


#Bestimmtes Buch ausgeben
@app.get("/buch/{id}")
def get_specific_entrie(id: int, con=Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("""
            select * from buch
            where id = %s
        """,
        (id,))
    book = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return book
    


#Buch updaten
@app.put("/buch/{id}")
def modify_entrie(id: int, buch: Buch, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update buch
            set titel = %s,
                autor = %s,
                erscheinungsjahr = %s,
                herausgeber = %s,
                seitenanzahl = %s,
                preis = %s,
                auf_lager = %s
            where id = %s
        """,
        (buch.titel, buch.autor, buch.erscheinungsjahr, buch.herausgeber, buch.seitenanzahl, buch.preis, buch.auf_lager, id))
        con.commit()
        result = {"changed": id, "new": buch}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#Buch hinzufügen
@app.post("/buch")
def add_entrie(buch: Buch, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into buch (id, titel, autor, erscheinungsjahr, herausgeber, seitenanzahl, preis, auf_lager)
                    values ( %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (buch.id, buch.titel, buch.autor, buch.erscheinungsjahr, buch.herausgeber, buch.seitenanzahl, buch.preis, buch.auf_lager)
        )
        con.commit()
        result = {"added": buch}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result
    


# Buch löschen
@app.delete("/buch/{id}")
def delete_entrie(id: int, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from buch WHERE id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result




#ENDPUNKTE E-BOOK


#alle E-Bücher ausgeben
@app.get("/e-book")
def get_all_entries(con = Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("select * from ebook")
    ebooks = cursor.fetchall()
    cursor.close()
    return ebooks



#Bestimmtes E-Buch ausgeben
@app.get("/e-book/{id}")
def get_specific_entrie(id: int, con = Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("""
            select * from ebook
            where id = %s
        """,
        (id,))
    ebook = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return ebook
    


#E-Buch updaten
@app.put("/e-book/{id}")
def modify_entrie(id: int, buch: E_Book, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update ebook
            set titel = %s,
                autor = %s ,
                erscheinungsjahr = %s,
                herausgeber = %s,
                seitenanzahl = %s,
                preis = %s
            where id = %s
        """,
        (buch.titel, buch.autor, buch.erscheinungsjahr, buch.herausgeber, buch.seitenanzahl, buch.preis, id))
        con.commit()
        result = {"changed": id, "new": buch}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result




#E_book hinzufügen
@app.post("/e-book")
def add_entrie(buch: E_Book, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into ebook (id, titel, autor, erscheinungsjahr, herausgeber, seitenanzahl, preis)
                    values (%s, %s, %s, %s, %s, %s, %s)
            """,
            (buch.id, buch.titel, buch.autor, buch.erscheinungsjahr, buch.herausgeber, buch.seitenanzahl, buch.preis)
        )
        con.commit()
        result = {"added": buch}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#E_book löschen
@app.delete("/e-book/{id}")
def delete_entrie(id: int, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from ebook where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()

    return result





#ENDPUNKTE FILM


#alle Filme asugeben
@app.get("/film")
def get_all_entries(con=Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("select * from film")
    film = cursor.fetchall()
    cursor.close()
    return film



#Bestimmten Film ausgeben
@app.get("/film/{id}")
def get_specific_entrie(id: int, con=Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("""
            select * from film
            where id = %s
        """,
        (id,))
    film = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return film
    


#Film updaten
@app.put("/film/{id}")
def modify_entrie(id: int, film:Film, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update film
            set titel = %s,
                produzent = %s,
                erscheinungsjahr = %s,
                preis = %s,
                auf_lager = %s
            where id = %s
        """,
        (film.titel, film.produzent, film.erscheinungsjahr, film.preis, film.auf_lager, id))
        con.commit()
        result = {"changed": id, "new": film}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#film hinzufügen
@app.post("/film")
def add_entrie(film:Film, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into film (id, titel, produzent, erscheinungsjahr, preis, auf_lager)
                    values (%s, %s, %s, %s, %s, %s)
            """,
            (film.id, film.titel, film.produzent, film.erscheinungsjahr, film.preis, film.auf_lager)
        )
        con.commit()
        result = {"added": film}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result




#Film löschen
@app.delete("/film/{id}")
def delete_entrie(id: int, con = Depends(get_con)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from film where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()

    return result






#ENDPUNKTE BACKSTOCK

#Lagerbestand ausgeben(alle)
@app.get("/backstock")
def get_all_entries(con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("select * from backstock")
    backstock = cursor.fetchall()
    cursor.close()
    return backstock



#Lagerbestand ausgeben(id)
@app.get("/backstock/{id}")
def get_specific_entrie(id: int, con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("""
            select * from backstock
            where id = %s
        """,
        (id,))
    backstock = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return backstock
    


#Lager updaten
@app.put("/backstock/{id}")
def modify_entrie(id: int, backstock: Backstock, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update backstock
            set kuhmilch = %s,
                hafermilch = %s,
                kaffeebohnen = %s,
                limonade = %s,
                apfelschorle = %s,
                wasser = %s
            where id = %s
        """,
        (backstock.kuhmilch, backstock.hafermilch, backstock.kaffebohnen, backstock.limonade, backstock.apfelschorle, backstock.wasser, id))
        con.commit()
        result = {"changed": id, "new": backstock}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#Lagerbestand hinzufügen
@app.post("/backstock")
def add_entrie(backstock: Backstock, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into backstock (id, kuhmilch, hafermilch, kaffeebohnen, limonade, apfelschorle, wasser)
                    values (%s, %s, %s, %s, %s, %s, %s)
            """,
            (backstock.id, backstock.kuhmilch, backstock.hafermilch, backstock.kaffebohnen, backstock.limonade, backstock.apfelschorle, backstock.wasser)
        )
        con.commit()
        result = {"added": backstock}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#Lagerbestand löschen
@app.delete("/backstock/{id}")
def delete_entrie(id: int, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from backstock where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result






#ENDPUNKTE americano

#Lagerbestand ausgeben(alle)
@app.get("/americano")
def get_all_entries(con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("select * from americano")
    americano = cursor.fetchall()
    cursor.close()
    return americano



#Lagerbestand ausgeben(id)
@app.get("/americano/{id}")
def get_specific_entrie(id: int, con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("""
            select * from americano
            where id = %s
        """,
        (id,))
    americano = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return americano
    


#Lager updaten
@app.put("/americano/{id}")
def modify_entrie(id: int, americano: Americano, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update americano
            set preis = %s,
                bestelldatum = %s
            where id = %s
        """,
        (americano.preis, datetime.now(), id))
        con.commit()
        result = {"changed": id, "neuer Preis": americano.preis}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#Lagerbestand hinzufügen
@app.post("/americano")
def add_entrie(americano: Americano, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into americano (id, preis, bestelldatum)
                    values (%s, %s, %s)
            """,
            (americano.id, americano.preis, datetime.now())
        )
        con.commit()
        result = {"added": americano}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#Lagerbestand löschen
@app.delete("/americano/{id}")
def delete_entrie(id: int, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from americano where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result






#ENDPUNKTE APFELSCHORLE

#Lagerbestand ausgeben(alle)
@app.get("/apfelschorle")
def get_all_entries(con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("select * from apfelschorle")
    americano = cursor.fetchall()
    cursor.close()
    return americano



#Lagerbestand ausgeben(id)
@app.get("/apfelschorle/{id}")
def get_specific_entrie(id: int, con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("""
            select * from apfelschorle
            where id = %s
        """,
        (id,))
    apfelschorle = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return apfelschorle
    


#Lager updaten
@app.put("/apfelschorle/{id}")
def modify_entrie(id: int, apfelschorle:Apfelschorle, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update apfelschorle
            set preis = %s,
                bestelldatum = %s
            where id = %s
        """,
        (apfelschorle.preis, datetime.now(), id))
        con.commit()
        result = {"changed": id, "neuer Preis": apfelschorle.preis}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#Lagerbestand hinzufügen
@app.post("/apfelschorle")
def add_entrie(apfelschorle:Apfelschorle, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into apfelschorle (id, preis, bestelldatum)
                    values (%s, %s, %s)
            """,
            (apfelschorle.id, apfelschorle.preis, datetime.now())
        )
        con.commit()
        result = {"added": apfelschorle}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#Lagerbestand löschen
@app.delete("/apfelschorle/{id}")
def delete_entrie(id: int, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from apfelschorle where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result





#ENDPUNKTE LATTE

#Lagerbestand ausgeben(alle)
@app.get("/latte")
def get_all_entries(con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("select * from latte")
    latte = cursor.fetchall()
    cursor.close()
    return latte



#Lagerbestand ausgeben(id)
@app.get("/latte/{id}")
def get_specific_entrie(id: int, con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("""
            select * from latte
            where id = %s
        """,
        (id,))
    latte = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return latte
    


#Lager updaten
@app.put("/latte/{id}")
def modify_entrie(id: int, latte:Latte, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update latte
            set preis = %s,
                bestelldatum = %s
            where id = %s
        """,
        (latte.preis, datetime.now(), id))
        con.commit()
        result = {"changed": id, "neuer Preis": latte.preis}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#Lagerbestand hinzufügen
@app.post("/latte")
def add_entrie(latte:Latte, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into latte (id, preis, bestelldatum)
                    values (%s, %s, %s)
            """,
            (latte.id, latte.preis, datetime.now())
        )
        con.commit()
        result = {"added": latte}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#Lagerbestand löschen
@app.delete("/latte/{id}")
def delete_entrie(id: int, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from latte where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result





#ENDPUNKTE limonade

#Lagerbestand ausgeben(alle)
@app.get("/limonade")
def get_all_entries(con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("select * from limonade")
    limonade = cursor.fetchall()
    cursor.close()
    return limonade



#Lagerbestand ausgeben(id)
@app.get("/limonade/{id}")
def get_specific_entrie(id: int, con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("""
            select * from limonade
            where id = %s
        """,
        (id,))
    limonade = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return limonade
    


#Lager updaten
@app.put("/limonade/{id}")
def modify_entrie(id: int, limonade:Limonade, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
            update limonade
            set preis = %s,
                bestelldatum = %s
            where id = %s
        """,
        (limonade.preis, datetime.now(), id))
        con.commit()
        result = {"changed": id, "neuer Preis": limonade.preis}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#Lagerbestand hinzufügen
@app.post("/limonade")
def add_entrie(limonade:Limonade, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("""
                insert into limonade (id, preis, bestelldatum)
                    values (%s, %s, %s)
            """,
            (limonade.id, limonade.preis, datetime.now())
        )
        con.commit()
        result = {"added": limonade}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    
    return result



#Lagerbestand löschen
@app.delete("/limonade/{id}")
def delete_entrie(id: int, con = Depends(get_con_cafe)):
    cursor = con.cursor()
    try:
        cursor.execute("delete from limonade where id = %s", (id,))
        con.commit()
        result = {"deleted": id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        con.close()
    return result



#anzahl Bücher
@app.get("/buch_bestand")
def get_specific_entrie( con=Depends(get_con)):
    cursor = con.cursor()
    cursor.execute("""
            select count(*), sum(preis) from buch
            where auf_lager = True
        """)
    bestand = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return {"Anzahl der vorhandenen Bücher": bestand[0][0], "Gesamtwert der Bücher": bestand[0][1]}


#summe preis
@app.get("/film_bestand")
def get_specific_entrie( con=Depends(get_con_cafe)):
    cursor = con.cursor()
    cursor.execute("""
            select count(*), sum(preis) from film
            where auf_lager = True
        """)
    bestand = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return {"Anzahl der vorhandenen Filme": bestand[0][0], "Gesamtwert der Filme": bestand[0][1]}





if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port=8000, reload=use_reload)