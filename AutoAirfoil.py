from tkinter import *

GREY="#2e2e2e"


root=Tk()
root.title("AutoAirfoil")
root.geometry("1280x720")

flowOpts=["Laminar","Turbulent"]
flowChoice=StringVar()
flowChoice.set(flowOpts[0])
flowMenu=OptionMenu(root,flowChoice,*flowOpts)
flowMenu.place(x=40,y=40)

cruiseSpeed=StringVar()
cruiseSpdEntry=Entry(root,textvariable=cruiseSpeed)
cruiseSpdEntry.place(x=40,y=100)

tkoffSpeed=StringVar()
tkoffSpeedEntry=Entry(root,textvariable=tkoffSpeed)

topSpeed=StringVar()
topSpeedEntry=Entry(root,textvariable=topSpeed)

payload=StringVar()
payloadEntry=Entry(root,textvariable=payload)


root.mainloop()