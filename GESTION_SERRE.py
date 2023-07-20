import math
from mysql.connector import connect
import matplotlib.pyplot as plt

mydb = connect(host="localhost",user="root",password="ayoube essadeq",database="serre",)

cursor = mydb.cursor()

############################################ LES FONCTIONS REELLEMENT UTILISEES #######################

def set_mesure(T: float, H: float):
    num = 0
    try:
        cursor.execute("SELECT num FROM main ORDER BY num DESC LIMIT 1")
        num = cursor.fetchall()[0][0]+1
    except:
        pass

    finally:
        query = f"INSERT INTO main VALUES({num},CURRENT_TIMESTAMP,{T},{H},'{Etat(T, H)}')"
        cursor.execute(query)
        mydb.commit()


def get_mesures(limit: int,type_données:str):
    try:
        cursor.execute(f"SELECT time_mesure,{type_données},Etat FROM main ORDER BY num DESC LIMIT "+str(limit))
        mesures_list_tuples = cursor.fetchall()
        return mesures_list_tuples
    except:
        return "Pas de mesures à afficher"


def delete_mesures(nbr_rows: int):
    try:
        cursor.execute("SELECT num FROM main ORDER BY num LIMIT 1")
        first_num = cursor.fetchall()[0][0]
        query = f"DELETE FROM main WHERE num BETWEEN {first_num} AND {first_num + nbr_rows}"
        cursor.execute(query)
        mydb.commit()
    except:
        print("Pas de mesures à supprimer!")

################################################ LES FONCTIONS ASSISTANTES #################################

def Etat(T: float, H: float):
    if (T <= 0):
        return "très froid"
    if (T > 0 and T < 10):
        return "froid"
    if (T >= 10 and T <= 30):
        if (H < 60):
            return "trés sec"
        if (H >= 60 and H <= 90):
            return "adequat"
        if (H > 90):
            return "trés sec"
    if (T > 30):
        return "trés chaud"


def Tri(Param_tri: str):
    try:
        cursor.execute(f"SELECT * FROM main ORDER BY {Param_tri} DESC ")
        mesures_list_tuples_triee = cursor.fetchall()
        return mesures_list_tuples_triee
    except:
        return "pas de mesures a trier"

################################################### LES GRPAH ################################################""


def Graph(Parametre: str, Last_n_mesures: int):
    try:
        cursor.execute(
            f"SELECT num,{Parametre} FROM main ORDER BY num DESC LIMIT {Last_n_mesures}")
        X = []
        Y = []
        for tuple in cursor.fetchall():
            X.append(tuple[0])
            Y.append(tuple[1])
        X.reverse()
        Y.reverse()

        xint = range(min(X), math.ceil(max(X))+1)
        plt.xticks(xint)

        font = {'family': 'serif',
                'weight': 'normal',
                'size': 16,
                }
        if (Parametre == "Temperature"):
            color = "orange"
            label = "T(°C)"
        else:
            color = "blue"
            label = "H(%)"

        plt.plot(X, Y, c=color, marker=".")
        plt.xlabel("num_mesure", fontdict=font, c="green")
        plt.ylabel(label, fontdict=font, c="green")
        plt.title(
            f"{Parametre} pour les {Last_n_mesures} derniers mesures", fontdict={'family': 'serif', 'weight': 'bold',
                                                                                 'size': 16}, c="red")
        plt.grid()
        plt.show()
    except:
        print("pas de mesures à afficher!")

print(get_mesures(100,'temperature'))