import tkinter
import re
from tkinter import PhotoImage
import math
from mysql.connector import connect
import matplotlib.pyplot as plt
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1) 

##Configuration génerale.   
root = tkinter.Tk()
L = 1250
h = 730
donnée_température = ['pas encore de mesure' for i in range(10)]
donnée_humidité = ['pas encore de mesure' for i in range(10)]

root.geometry('{}x{}'.format(L,h))
root.configure(bg='white')
root.title("Plant-project")
root.resizable(False,False)

icon = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\icon.png")
root.iconphoto(False,icon)

#UI-Componenants :
btn_actualiser = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\actualiser.png")
act_btn_actualiser = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\active-actualiser.png")
afficheur = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\afficheur.png")
dashboard = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\dashboard.png")
plant_statue = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\plant.png")
chart_temp = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\chart.png")
chart_hum = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\chart.png")
act_chart = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\act2_chart.png")
history_temp = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\history.png")
history_hum = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\history.png")
act_history = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\act_history.png")
stars = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\stars.png")
notification = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\notification.png")
notification_found = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\notification_found.png")
scroller = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\scroller.png")
title = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\title.png")
close = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\close.png")
active_close = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\active_close.png")
shadow = tkinter.PhotoImage(file=r"Python project\User Interface\Projet-de-prise-en-main\ressource\shadow.png")

#root components :
cnv = tkinter.Canvas(root,width=L,height=h,bg="white",highlightthickness=0)

############################## The dashboard for history data :#############################
color = '#aade87'
frame_dash_scroller = tkinter.Canvas(root,width=600,height=h,bg='white',highlightthickness=0,bd=0)
frame_dash_scroller.create_image(470,0,image=shadow,anchor='nw')
history_data = tkinter.Canvas(root,width=470,height=h,scrollregion=(0,0,0,4000),bg=color,bd=0,highlightthickness=0)
cnv.create_window(0,0,window=frame_dash_scroller,anchor='nw',tag='table')
frame_dash_scroller.create_window(0,0,window=history_data,anchor='nw')
frame_dash_scroller.create_line(485,50,485,h-50,width=2,fill='#008000')
frame_dash_scroller.create_image(485,50,image=scroller,anchor='center',tag='scroller')
frame_dash_scroller.create_image(472,5,image=close,activeimage=active_close,anchor='nw',tag='close')
history_data.create_image(30,30,image=title,anchor='nw')
cnv.itemconfigure('table',state='hidden')


for i in range(0,800) :
    x = 50
    y = 100
    history_data.create_oval(x-10-5,y+20*i-5,x-10+5,y+20*i+5,outline='',fill = 'lightgreen')
    history_data.create_text(x,y+20*i,text="",anchor = 'w',justify="right",tag='d{}'.format(i+1))

def textShow(donné:str):
    Digits = "\d{1,4}"
    Judge = "'.*'"
    lesDates = re.findall(Digits,donné)
    normalDate = lesDates[2]+'/'+lesDates[1]+'/'+lesDates[0]
    normalHour = lesDates[3]+':'+lesDates[4]+':'+lesDates[5]
    status = re.findall(Judge,donné)[0]
    valeur = lesDates[6]+'.'+lesDates[7]
    result = normalDate+'-'+'-'+normalHour+' : '+valeur+'->'+status
    return result

def temp_show(event):
    données = get_mesures(1000,'temperature')
    cnv.itemconfigure('table',state='normal')
    for i in range(1000):
        if i<len(données):
            donné = str(données[i])
            history_data.itemconfig('d{}'.format(i+1),text=textShow(donné))
        else:
            history_data.itemconfig('d{}'.format(i+1),text="")

def hum_show(event):
    données = get_mesures(1000,'humidité')
    cnv.itemconfigure('table',state='normal')

    for i in range(1000):
        if i<len(données):
            donné = str(données[i])
            history_data.itemconfig('d{}'.format(i+1),text=textShow(donné))
        else:
            history_data.itemconfig('d{}'.format(i+1),text="")

def closer(event):
    cnv.itemconfigure('table',state='hidden')

def scroll(event):
    x = event.x
    y = event.y
    if 50<=y<=h-50:
        frame_dash_scroller.coords('scroller',485,y)
        a = (y-50)/630.
        history_data.yview(tkinter.MOVETO,a)

frame_dash_scroller.tag_bind('close','<Button-1>',closer)
frame_dash_scroller.tag_bind('scroller','<B1-Motion>',scroll)
#########################################################################################
##Stars :
for i in range(1,6):
    cnv.create_oval(968+35*(i-1),88,988+35*(i-1),108,outline='',state='hidden',fill='#ffdd55',tag='star{}'.format(i))

cnv.create_image(41,85,image=dashboard,anchor='nw',tag='dashboard')
cnv.create_image(1076,675,image=btn_actualiser,activeimage=act_btn_actualiser,anchor='nw',tag='btn_actualiser')
cnv.create_image(355,82,image=chart_temp,activeimage = act_chart,anchor='nw',tag='chart_temp')
cnv.create_image(355,390,image=chart_hum,activeimage = act_chart,anchor='nw',tag='chart_hum')
cnv.create_image(310,80,image=history_temp,activeimage = act_history,anchor='nw',tag='history_temp')
cnv.create_image(310,388,image=history_hum,activeimage = act_history,anchor='nw',tag='history_hum')
cnv.create_rectangle(904,205,1194,535,outline='',fill='#dde9af',tag='indicator')
cnv.create_image(904,205,image=plant_statue,anchor='nw',tag='plant_statue')
cnv.create_image(965,88,image=stars,anchor='nw',tag='stars')
cnv.create_image(625,675,image=notification,anchor='nw',tag='notification')

##Positioning the components :
cnv.pack()

##Functions :

def evaluating(stars):
    for i in range(5):
        tag = 'star{}'.format(i+1)
        cnv.itemconfig(tag,state='hidden')
    for i in range(stars):
        tag = 'star{}'.format(i+1)
        cnv.itemconfig(tag,state='normal')
    if stars == 5 :
        cnv.itemconfig('indicator',fill='#44aa00')
    elif stars == 4 :
        cnv.itemconfig('indicator',fill='#5aa02c')
    elif stars == 3 :
        cnv.itemconfig('indicator',fill='#8dd35f')
    elif stars == 2 :
        cnv.itemconfig('indicator',fill='#cdde87')
    elif stars == 1 :
        cnv.itemconfig('indicator',fill='#e9ddaf')

############################## Tout Ce Qui est en relation avec La bas de données ######################

mydb = connect(host="localhost",user="root",password="ayoube essadeq",database="serre",)
cursor = mydb.cursor()

################################# LES FONCTIONS EN RELATION AVEC LA BASE #######################

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
        if (Parametre == "temperature"):
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

##########################################################################################################

def alerting(message):
    pass ##cette fonction permet d'envoyer un message

def measuring():
    pass ##les mesures de l'arduino

def données_TH(L,p_initial,typ):
    for i in range(len(L)) :
        x = p_initial[0]
        y = p_initial[1]
        cnv.create_oval(x-10-5,y+20*i-5,x-10+5,y+20*i+5,outline='',fill = 'lightgreen')
        cnv.create_text(x,y+20*i,text=L[i],anchor = 'w',justify="right",font = 'Arial',fill = 'white',tag=typ+'{}'.format(i+1))

def updater(L:list,valeur,typ):
    L.insert(0,valeur)
    L.pop()
    for i in range(len(L)):
        name = typ+'{}'.format(i+1)
        cnv.itemconfig(name,text=L[i])

données_TH(donnée_température,(80,160),'t')
données_TH(donnée_humidité,(80,460),'h')

#binding :
cnv.tag_bind('history_temp','<Button-1>',temp_show)
cnv.tag_bind('history_hum','<Button-1>',hum_show)
cnv.tag_bind('btn_actualiser','<Button-1>',lambda event: updater(donnée_température,'23C° incroyable','t'))
cnv.tag_bind('chart_temp','<Button-1>',lambda event: Graph('temperature',100))
cnv.tag_bind('chart_hum','<Button-1>',lambda event: Graph('humidité',100))

#the mainloop :
root.mainloop()