# -*- coding: utf-8 -*-
"""
This is the GUI for connecting the OBIS_TIMER module to an interactive
Graphical interface.

This was set up using Tkinter. Originally I had planned to graph power
over time but decided a straight line would be a boring graph. but that is why
the matplotlib modules are commented out.

Created on Wed Jun  8 19:11:54 2016
@author: Brae
"""
import OBIS_TIMER as obt
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
from threading import Timer
import tkinter as tk
from tkinter import ttk
LARGE_FONT= ("Verdana", 12)
import time
i = 0

def update(function,papa,i):
    """We will update our tkinter page using this function"""
    #updatetimer = Timer(0.1,function)
    #updatetimer.start()
    #print(i)
    papa.after(1000, function)
    return i+1

    
class Framemaker(tk.Tk):
    """Opens Frames by using a for loop. This is great for creating
    multiple frames/windows that will have the same information on them
    or have the same settings."""

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "OBIS Laser Control")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont, info=None):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    """The only Page I use but if you wanted more you could add in a
    history or settings page. just create another class like start page and
    insert the class name in the For loop for Framemaker

    See pythonprogramming.net for examples on tkinter. Or Sentdex.

    """

    def __init__(self, parent, controller):
        self.ob=ob=obt.OBIS()
        self.controller = controller
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Go.TButton', font= LARGE_FONT, background="#ccffcc", foreground = "#009900")
        s.configure('Stop.TButton', font= LARGE_FONT, background="#ffb8bc", foreground = "#ce2732")
        s.configure("red.Horizontal.TProgressbar",foreground='red',background='red')
        s.configure("yellow.Horizontal.TProgressbar",foreground='yellow',background='yellow')
        s.configure("green.Horizontal.TProgressbar",foreground='green',background='green')
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Laser Timer Program", font=LARGE_FONT)
        label.grid(columnspan=4)
        self.modeltext=tk.Label(self, text= "")
        self.modeltext.grid(row =1 , column = 0 , columnspan=3)
        self.hourstext=tk.Label(self, text= "")
        self.hourstext.grid(row = 2, column = 0, columnspan=2)
        self.wavelengthtext=tk.Label(self, text= "")
        self.wavelengthtext.grid(row =3 , column = 0, columnspan=2)
        self.modetext=tk.Label(self, text= "")
        self.modetext.grid(row = 4, column = 0, columnspan=2)
        self.statustext=tk.Label(self, text= "")
        self.statustext.grid(row =5 , column = 0, columnspan=2)
        self.powertext=tk.Label(self, text= "")
        self.powertext.grid(row = 6, column = 0, columnspan=2)
        realpower=eval(self.ob.get_power_level())*1000
        self.powervar=tk.DoubleVar(value=realpower)
        self.powernumber=tk.Spinbox(self, width = 5,textvariable=self.powervar)
        self.powernumber.grid(row=7, column = 0 , padx=10, sticky = "E")
        self.powerbutton=ttk.Button(self, text = "Set Power Level", command= lambda: self.powerset())
        self.powerbutton.grid(row =7, column = 1)
        self.powerscale=ttk.Progressbar(self, orient="vertical")#self, to=0, resolution = 0.02)
        self.powerscale.grid(row=4, column = 2 , sticky = 'NW', rowspan = 4, padx=10)
        self.startbutton = ttk.Button(self, text = "All Start", style="Go.TButton", command= lambda:self.start())
        self.startbutton.grid(row=10, columnspan = 2, pady = 5)
        self.stopbutton= ttk.Button(self,text="All Stop", style="Stop.TButton", command = lambda: self.stop2())
        self.timerlabel=tk.Label(self, text = "Timer in minutes: ")
        self.timerlabel.grid(row = 8 , column = 0, sticky = "E")
        self.timerflag= False
        self.laserON=False
        self.laserOFF=False
        self.timerstopflag=False
        self.timernumber=tk.Spinbox(self, width = 6)
        self.timernumber.grid(row=8, column = 1, sticky = "W", padx = 5)
        self.timergo= ttk.Button(self,text = "TIME Laser", command = lambda: self.time())
        self.timergo.grid(row = 9, column= 1, sticky = "W" ,pady = 5)
        self.timerlapse=tk.Label(self,text="Time Remaining: --")
        self.timerlapse.grid(row=9, column = 0, sticky = " E " , padx = 10, pady = 5)
        self.powerflag=False
        self.i=update(self.updatelabels,controller,0)
    def short(self):
        """ This can help debug threading limits quickly """
        i = self.i
        if i%1024 < 1 :
            print(i)
        self.i+=1
        update(self.short,self.controller, self.i)
    def setlevel(self):
        print(3)
    def powerset(self):
        """Sets the power level!"""
        self.powerflag=True
       
    def start(self):
        """Starts the Obis, changes the start button to a stop button"""
        
        self.laserON=True
        self.stopbutton= ttk.Button(self,text="All Stop", style="Stop.TButton", command = lambda: self.stop2())
        
        self.hide_buttons(self.startbutton,self.stopbutton)
    def stop2(self):
        
        """Stops the OBIS, changes stop button to start button"""
        
        self.laserOFF=True
        self.startbutton = ttk.Button(self, text = "All Start", style="Go.TButton", command= lambda:self.start())
        
        self.hide_buttons(self.stopbutton,self.startbutton)
    def hide_buttons(self,bt1,bt2):
        k1=bt1.grid_info()
        bt1.forget()
        bt2.grid(k1)
    
        
        
        
    def updatelabels(self):
        """This update labels instruction was designed for threading
        my first program with threads so I wasn't sure the best way
        to be sure that the current thread wasn't interrupted by a user change.
        So each GUI button that will change a status of the OBIS sets off a flag
        that will change the OBIS during the next time the thread updates labels.

        Downside is because it updates every second, and it requires about 1 second to update
        a user can enter in two commands before the first has taken place. This so far has lead to
        problems only with the TIMER where the first timer was canceled and a new timer set before the
        threading cycle was completed, and the laser never shuts off.
        """
        if self.powerflag: # Check to see if we have a change power request
             num=eval(self.powernumber.get())
             print(num, "is num")
             self.ob.set_power_level(num)
             self.powerflag=False
        model = self.ob.get_model()
        hours = self.ob.get_diod_hour()  
        wavelength=self.ob.get_wavelength()
        mode =self.ob.get_mode()
        status = self.ob.get_status()
        power =eval(self.ob.get_max_power_level())*1000
        self.powerscale['maximum']=power
        realpower=eval(self.ob.get_power_level())*1000
        self.powerscale['value']=realpower
        #Determine if the timer has stopped
        if self.ob.turnoff:
            self.stop2()
            self.hide_buttons(self.timerstop,self.timergo)
            self.ob.turnoff=False
        #Determine if we should turn the Laser on
        if self.laserON:
            self.ob.change_status(True) # Turn laser on
            self.laserON=False
        if self.laserOFF:
            print('Did we turn off?')
            self.ob.change_status(False) #Turn Laser off
            self.laserOFF=False
        #Determine if we should stop the timer
        if self.timerstopflag:
            print('We have reached here', self.timerstopflag)
            #self.ob.t.cancel()
            self.timergo= ttk.Button(self,text = "TIME Laser", command = lambda: self.time())
            self.hide_buttons(self.timerstop,self.timergo)
            self.timerstopflag=False
        # Determine what color the progress bar should be
        if realpower/power > 0.88:
            self.powerscale['style']="red.Horizontal.TProgressbar"
        elif realpower/power > 0.75:
            self.powerscale['style']="yellow.Horizontal.TProgressbar"
        else:
            self.powerscale['style']="green.Horizontal.TProgressbar"
        #self.powerscale.set(realpower)
        #print(realpower, 'RP')
        self.modeltext['text']="{:}".format(model)
        self.hourstext['text']="{:>30}:     {:}".format("Hours",hours)
        self.wavelengthtext['text']="{:>30}:     {:}".format("Wavelength",wavelength)
        self.modetext['text']="{:>30}:     {:}".format("Mode",mode)
        self.statustext['text']="{:>30}:     {:}".format("Status",status)
        self.powertext['text']="{:>30}:     {:}".format("Power (mW)", "Cannot Exceed "+str(power)+" mW")
        #Determine time remaining for timer label
        if self.timerflag: # Are we timing? 
            if time.time()-self.start_time > self.seconds: # have enough seconds elapsed to turn off laser?
                self.timerflag=False
                # Turn off the laser
                self.ob.change_status(False)
                self.laserOFF = False
            else:
                lapsed=self.timertotal-(time.time()-self.start_time)/60/60
                hours=lapsed-lapsed%1
                minutes=lapsed%1*60
                self.timerlapse['text']= " Time Remaining: {:} hours {:.2f} minutes".format(hours,minutes)
        else:
            self.timerlapse['text']= "--"
        #self.updatetimer=None
        #self.update()
        #update(self.updatelabels)
        
        self.i = self.i-1 # This is a counter for debugging if we have any recursive updates
        #print("Finished {}".format(self.i))
        self.i = update(self.updatelabels,self.controller,self.i)
    def update(self):
        #self.updatetimer=Timer(1, self.updatelabels).start()
        #print("updating")
        while True:
            self.updatelabels()
            
        
    def time(self):
        """ Instead of using the threading Timer module, we simply compare clock times in order to turn off
        our timer during the updates."""
        self.timerflag = True
        self.start_time=time.time() # Creat our start time variable
        self.seconds = eval(self.timernumber.get())*60  # Retrieve the number of minutes and convert to seconds
        #self.ob.gui_set_timer(mini)
        print ("time stuff here {} minutes".format(self.seconds/60))
        self.timertotal=self.seconds/60/60
        self.timerstop= ttk.Button(self,text = "Stop Timer", command = lambda: self.timestop())
        self.hide_buttons(self.timergo,self.timerstop)
        #self.update()
    def timestop(self):
        self.timerstopflag=True
        self.timerflag = False
        
app = Framemaker()        

                
        
        

app.mainloop()
