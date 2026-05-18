import tkinter as tk
import json
import random

class snake:
    def __init__(self,root):
        try:
            with open('snake_score.json','r') as file:
                self.data = json.load(file)
        except:
            self.data = 0

        self.root = root

        self.root.config(bg='black')
        
        self.pos_1 = [67+15*i for i in range(5)]
        self.tick_speed = 400
        self.last_pressed = ''
        self.start = False #so snake doesnt speed up when pressing space
        self.die = False #for changing text
        self.apple_eaten = 0

        self.label_main = tk.Label(self.root,text='PRESS SPACE TO START',font=('Comic Sans MS','20','bold'),
                                   bg='black',fg='white') ; self.label_main.pack()

        self.btn_msg_1 = tk.Button(self.root,text='',font=('Comic Sans MS','15','bold'),
                                   bg='black',fg='white',relief='flat') ; self.btn_msg_1.pack()
        self.btn_msg_2 = tk.Button(self.root,text='',font=('Comic Sans MS','15','bold'),
                                   bg='black',fg='white',relief='flat') ; self.btn_msg_2.pack()
        self.btn_msg_3 = tk.Button(self.root,text='',font=('Comic Sans MS','15','bold'),
                                   bg='black',fg='white',relief='flat') ; self.btn_msg_3.pack()
        self.btn_msg_4 = tk.Button(self.root,text='',font=('Comic Sans MS','15','bold'),
                                   bg='black',fg='white',relief='flat') ; self.btn_msg_4.pack()

        self.root.bind('<Key>',self.change_key)
        self.root.bind('<Button-1>',lambda e:print(e))

        self.btn_pos_dict = {} #cause old method made it lag hard

        self.bg_make() #makes background
        self.make_apple() #making of apple and coloring of bg

        self.root.bind('<FocusIn>',lambda e=None:print('yes')) #for testing
        self.root.bind('<FocusOut>',lambda e=None:print('no'))

    def change_key(self,event):
        if event.char in ['w','a','s','d','W','A','S','D']:
            self.last_pressed = event.char.lower()

        elif event.keysym in ['Up','Down','Left','Right']:
            self.last_pressed = event.keysym

        elif event.char == ' ' and self.start == False: #to start game press space
            self.last_pressed = 'w'
            self.start = True
            self.move(self.last_pressed) #actually starts game

    def make_apple(self):
        self.apple_pos = random.randint(0,180) #makes apple in random position
        while self.apple_pos in self.pos_1: #apple doesnt spawn in snakes body
            self.apple_pos = random.randint(0,180)
        
        self.bg_color() #makes bg after apple has been made

    def bg_make(self):
        x,y = 45,80 # 40x45 (y,x) x is 15 times y is 12 times and diff btwn 2 x is 15
        for i in range(180): #makes all the buttons
            btn = tk.Button(text=i,width=5,height=2) ; btn.pack()
            btn.place(x=x,y=y)

            self.btn_pos_dict[i] = btn

            if x <= 16*45:
                x += 45
                if x == 16*45:
                    x = 45
                    y += 40
    
    def bg_color(self):
        for i,c in enumerate(self.btn_pos_dict):
            if c%2 == 0:
                self.btn_pos_dict[i].config(bg='#1C1F2A',fg='#1C1F2A') #make everything black
            else:
                self.btn_pos_dict[i].config(bg="#0F0F14",fg='#0F0F14')
            
        for i in self.pos_1:
            self.btn_pos_dict[i].config(bg='#168211',fg="#168211") #make things in list green//body
            
        self.btn_pos_dict[self.pos_1[0]].config(bg="#189f11",fg='#189f11') #head

        self.btn_pos_dict[self.pos_1[-1]].config(bg="#175e13",fg='#175e13') #tail
        #fg = white shows current position in button

        self.btn_pos_dict[self.apple_pos].config(bg='#FF0000',fg='#FF0000') #make apple red

    def move(self,event):
        try: # this is for hitting the top and bottom giving list error
            self.label_main.config(text='')
            if self.die == False:
                self.btn_msg_1.config(text=f'Length of Snake: {len(self.pos_1)}')
                self.btn_msg_2.config(text=f'Score: {self.apple_eaten}')
                self.btn_msg_3.config(text=f'Highest Score: {self.data}')
                self.btn_msg_4.config(text=f'Delay in speed: {self.tick_speed}')

                self.btn_msg_1.place(x=80,y=25)
                self.btn_msg_2.place(x=300,y=25)
                self.btn_msg_3.place(x=420,y=25)
                self.btn_msg_4.place(x=290,y=550)
            elif self.die == True:
                self.label_main.config(text='You Died')
                self.btn_msg_1.config(text='')
                self.btn_msg_2.config(text='')
                self.btn_msg_3.config(text='')
                self.btn_msg_4.config(text='')

                self.btn_msg_1.place(x=0,y=0) #cause it gives black spot on main label
                self.btn_msg_2.place(x=0,y=0)
                self.btn_msg_3.place(x=0,y=0)
                self.btn_msg_4.place(x=0,y=0)

            if event == 'a' or event == 'Left': #left
                self.pos_1.insert(0,self.pos_1[0]-1) #assigns new position for head
            
            elif event == 'd' or event == 'Right': #right
                self.pos_1.insert(0,self.pos_1[0]+1)

            elif event == 'w' or event == 'Up': #up
                self.pos_1.insert(0,self.pos_1[0]-15)
            
            elif event == 's' or event == 'Down': #down
                self.pos_1.insert(0,self.pos_1[0]+15)
            
            elif event == 'q': #stop game?
                return

            if self.apple_pos == self.pos_1[0]:
                ... #doesnt remove tail if apple is eaten
            else:
                self.pos_1.pop() #removes tail

            self.bg_color() #makes things green again according to self.pos_1
            self.root.after(self.tick_speed,lambda:self.move(self.last_pressed)) #auto move

            self.die_check()
            self.apple_check()

        except:
            self.label_main.config(text='You Died')
            self.btn_msg_1.config(text='')
            self.btn_msg_2.config(text='')
            self.btn_msg_3.config(text='')
            self.btn_msg_4.config(text='')

            self.btn_msg_1.place(x=0,y=0)
            self.btn_msg_2.place(x=0,y=0)
            self.btn_msg_3.place(x=0,y=0)
            self.btn_msg_4.place(x=0,y=0)
    
    def apple_check(self): #this is for scores and making the body bigger
        if self.apple_pos == self.pos_1[0]:
            self.apple_eaten+=1 #increases apple
            if self.data < self.apple_eaten:
                self.data = self.apple_eaten #changes datas value to match high score
                try:
                    with open('snake_score.json','w') as file:
                        json.dump(self.data,file)
                except: ... #does nothing in except
            self.make_apple() #remakes everything gives it a cool white flash vfx

            if self.apple_eaten%5 == 0:
                if self.tick_speed > 50:
                    self.tick_speed-=50

    def die_check(self):
        if self.pos_1[0] in self.pos_1[1:]: #if head is in body
            self.die = True
            self.last_pressed = 'q'
            for i in self.btn_pos_dict:
                self.btn_pos_dict[i].config(state='disabled')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f'{45*17}x{40*15}') #(y,x)
    root.title('Snake')
    root.resizable(False, False)
    snake(root)
    root.mainloop()
