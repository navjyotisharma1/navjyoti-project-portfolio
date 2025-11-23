from tkinter import*
from tkinter import ttk
import requests



'''cityname ="kerala"
data=requests.get("https://api.openweathermap.org/data/2.5/weather?q="+cityname+"&appid=1f8892d9a3e93f2741a5b04e3857df04").json()
print(data)'''

def dataget():
    city=cityname.get()
    data=requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=1f8892d9a3e93f2741a5b04e3857df04").json()
    name12.config(text=data["weather"][0]["main"])
    name21.config(text=data["weather"][0]["description"])
    name31.config(text=str(int(data["main"]["temp"]-273.15)))
    name41.config(text=data["main"]["pressure"])
    name51.config(text=str(int(data["main"]["temp_max"]-273.15)))
    name61.config(text=str(int(data["main"]["temp_min"]-273.15)))


win= Tk()

win.title("Weather report app")

win.config(bg="light pink")
win.geometry("700x550")


'''bg=PhotoImage("file=")
canvas1=Canvas(win,width=700,height=500)
canvas1.pack(fill="both",expand=True)
canvas1.create_image(0,0,image=bg,anchor="nw")'''


name=Label(win,text="WEATHER REPORT",font=("Script typeface",30,"bold"),bg="lightblue",fg="black")

name.place(x=90,y=90,height=30,width=400)

lists=["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
cityname=StringVar()
com=ttk.Combobox(win,text="latest weather app",values=lists,font=("Script typeface",15,"bold"),textvariable=cityname)
com.place(x=50,y=145,height=35,width=450)

name1=Label(win,text="weather climate :",font=("Script typeface",15,"bold"),bg="lightblue")
name1.place(x=70,y=265,height=35,width=170)

name12=Label(win,text=" ",font=("Script typeface",15,"bold",),bg="lightblue")
name12.place(x=235,y=265,height=35,width=170)

name2=Label(win,text="weather Description :",font=("Script typeface",13,"bold"),bg="lightblue")
name2.place(x=70,y=310,height=35,width=170)

name21=Label(win,text="",font=("Script typeface",13,"bold",),bg="lightblue")
name21.place(x=235,y=310,height=35,width=170)


name3=Label(win,text="temperature :",font=("Script typeface",15,"bold"),bg="lightblue")
name3.place(x=70,y=358,height=35,width=170)

name31=Label(win,text="",font=("Script typeface",15,"bold",),bg="lightblue")
name31.place(x=235,y=358,height=35,width=170)

name4=Label(win,text="pressure :",font=("Script typeface",14,"bold"),bg="lightblue")
name4.place(x=70,y=400,height=30,width=170)

name41=Label(win,text="",font=("Script typeface",14,"bold"),bg="lightblue")
name41.place(x=220,y=400,height=30,width=170)

name5=Label(win,text="temp max :",font=("Script typeface",13,"bold"),bg="lightblue")
name5.place(x=70,y=437,height=30,width=170)

name51=Label(win,text="",font=("Script typeface",13,"bold"),bg="lightblue")
name51.place(x=220,y=437,height=30,width=170)

name6=Label(win,text="temp min :",font=("Script typeface",13,"bold"),bg="lightblue")
name6.place(x=70,y=473,height=30,width=170)

name61=Label(win,text="",font=("Script typeface",13,"bold"),bg="lightblue")
name61.place(x=220,y=473,height=30,width=170)

done=Button(win,text="Search",font=("Time New Roman",20),command=dataget)
done .place(x=570,y=150,height=35,width=100)


win.mainloop()


