import time
import threading
from tkinter import ttk,PhotoImage,TclError
from tkinter import *
import pygame
from pygame import mixer
import random 
import winsound
import PIL
from PIL import Image


# count = 0
# anim = None



mixer.init()
class PomodorroTimer:
    def __init__(self):
        self.musics=['The Fall of Marley (New Version) (Episode 18 OST) (Attack on Titan - The Final Season).mp3','Attack on Titan S4 Part 2 Episode 4 OST - Grisha and Zeke Theme (Past and Future) _ HQ EPIC COVER.mp3']
        self.root=Tk()
        self.root.geometry("680x300")
        self.root.title("Pomodoro")
        self.root.call('wm','iconphoto',self.root._w,PhotoImage(file='tomato_121938.png'))
        self.s=ttk.Style()
        self.s.configure('TNotebook.Tab',font=("Ubuntu",16))
        self.s.configure("TButton",font=("Ubuntu",16))
        self.tabs=ttk.Notebook(self.root)
        self.tabs.pack(fill="both",pady=10,expand=True)
        
        self.tab1=ttk.Frame(self.tabs,width=600,height=100)
        self.tab2=ttk.Frame(self.tabs,width=600,height=100)
        self.tab3=ttk.Frame(self.tabs,width=600,height=100)
        
        #self.photo1=PhotoImage(file="college-studying-GIF-source.gif")
        self.gif_index = 0
        self.tabs.add(self.tab1,text='Pomodoro')
        self.tabs.add(self.tab2,text='short break')
        self.tabs.add(self.tab3,text='Long break')
        self.pomodoro_timer_label=ttk.Label(self.tab1,text="25:00",font=("Ubuntu",48))
        mixer.music.load(random.choice(self.musics))
        #mixer.music.play(-1)
        self.pomodoro_timer_label.pack(pady=20)
    

        
        self.pomodoro_short_break=ttk.Label(self.tab2,text="05:00",font=("Ubuntu",48))
        self.pomodoro_short_break.pack(pady=20)
        self.pomodoro_long_break=ttk.Label(self.tab3,text="15:00",font=("Ubuntu",48))
        self.pomodoro_long_break.pack(pady=20)
        self.grid_layout=ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        self.start_button=ttk.Button(self.grid_layout,text="Start",command=self.start_timer_thread)
        self.start_button.grid(row=0,column=0)
        self.start_button=ttk.Button(self.grid_layout,text="Skip",command=self.skip_timer)
        self.start_button.grid(row=0,column=1)
        self.start_button=ttk.Button(self.grid_layout,text="Reset",command=self.reset)
        self.start_button.grid(row=0,column=2)
        self.pomodoro_counter=ttk.Label(self.grid_layout,text="Pomodoros:0",font=("Ubuntu",16))
        self.pomodoro_counter.grid(row=1,column=0,columnspan=3)
        self.pomodoros=0
        self.skipped=False
        self.stopped=False
        self.running=False
                
        self.root.mainloop()


    def start_timer_thread(self):
        if not self.running:
            
            t=threading.Thread(target=self.start_timer)
            t.start()
            self.running=True
    def start_timer(self):
        self.stopped=False
        self.skipped=False
        timer_id=self.tabs.index(self.tabs.select())+1
        #mixer.music.play(10)
        if timer_id==1:
            full_seconds=60*25
            
            
            while full_seconds>0 and not self.stopped:
                winsound.PlaySound('clock-ticking-2.wav', winsound.SND_ASYNC)
                minutes,seconds=divmod(full_seconds, 60)
                self.pomodoro_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds-=1
            if not self.stopped or self.skipped:
                self.pomodoros+=1
                self.pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros%3==0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()
            
            if full_seconds==0:
                winsound.PlaySound('alarm-clock-01.wav', winsound.SND_ASYNC)
            
                
        elif timer_id==2:
                full_seconds=60*5
                winsound.PlaySound('alarm-clock-01.wav', winsound.SND_ASYNC)
                while full_seconds>0 and not self.stopped:
                    winsound.PlaySound('clock-ticking-2.wav', winsound.SND_ASYNC)
                    minutes,seconds=divmod(full_seconds,60)
                    self.pomodoro_short_break.config(text=f"{minutes:02d}:{seconds:02d}")
                    self.root.update()
                    time.sleep(1)
                    full_seconds-=1
                if not self.stopped or self.skipped:
                    self.tabs.select(0)
                    self.start_timer()
                if full_seconds==0:
                    winsound.PlaySound('alarm-clock-01.wav', winsound.SND_ASYNC)
                    
        elif timer_id ==3:
                    
                    full_seconds=60*15
                    winsound.PlaySound('alarm-clock-01.wav', winsound.SND_ASYNC)
                    while full_seconds>0 and not self.stopped:
                        winsound.PlaySound('clock-ticking-2.wav', winsound.SND_ASYNC)
                        minutes,seconds=divmod(full_seconds,60)
                        self.pomodoro_long_break.config(text=f"{minutes:02d}:{seconds:02d}")
                        self.root.update()
                        time.sleep(1)
                        full_seconds-=1
                    if not self.stopped or self.skipped:
                        self.tabs.select(0)
                        self.start_timer()
                        winsound.PlaySound('alarm-clock-01.wav', winsound.SND_ASYNC)
                    
        else:
                    print('Error')
                    

    def reset(self):
        mixer.music.unload()
        mixer.music.load(random.choice(self.musics))
        
        self.stopped=True
        self.skipped=False
        self.pomodoros=0
        self.pomodoro_timer_label.config(text="25:00")
        self.pomodoro_short_break.config(text="05:00")
        self.pomodoro_long_break.config(text="15:00")
        self.pomodoro_counter.config(text="Pomodoros:0")
        self.running=False
        
    def skip_timer(self):
        current_tab=self.tabs.index(self.tabs.select())
        if current_tab==0:
            self.pomodoro_timer_label.config(text="25:00")
        elif current_tab==1:
            self.pomodoro_short_break.config(text="05:00")
        elif current_tab==2:
            self.pomodoro_long_break.config(text="15:00")
        self.stopped=True
        self.skipped=True
PomodorroTimer()