import tkinter as tk
import random

def convert(char):
    char_dict = {'w':'Up','W':'Up','s':'Down','S':'Down','d':'Right','D':'Right','a':'Left','A':'Left'}
    return char_dict.get(char,char)

class snake_canv:
    def __init__(self,root,game_values):
        self.root = root
        self.game_values = game_values

        self.perm_tick_speed = 100 #for speed of snake
        self.game_state = {'start':False,'die':False} #state of game
        self.tick_speed = self.perm_tick_speed

        self.frame = tk.Frame(self.root,width = game_values['row']*game_values['cell_size'],
                              height = game_values['column']*game_values['cell_size'],bg='black') ; self.frame.pack(expand='True') #changes geomerty based on game_values['row'] and game_values['column']
        self.canvas = tk.Canvas(self.frame,width=self.frame.cget('width'),height=self.frame.cget('height')) ; self.canvas.pack() #same size as frame so its in seperate place than root
        
        self.grid_loc = {} #stores every grids position (x,y) along with their id
        self.grid_loc_reverse = {} #stores every grids id along with their position (x,y)

        self.lab = tk.Label(self.root, #for testing
                            text=f"Cell Size: {self.game_values['cell_size']}\nRow,Column : {self.game_values['row'],self.game_values['column']}\nSize of Frame/Canvas: {self.game_values['row']*self.game_values['cell_size'],self.game_values['column']*self.game_values['cell_size']}\nSize of window: {(self.game_values['row']+2)*self.game_values['cell_size'],(self.game_values['column']+2)*self.game_values['cell_size']}",
                            fg='black') ; self.lab.pack()

        self.make() #makes grid for game
        self.make_apple() #makes apple

        self.last_pressed = 'Up'
        self.root.bind('<Key>',self.change_key)

    def change_key(self,event):
        opp = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}
        current_pressed = self.last_pressed #for checking if new event is not opposite to old so you die immediately
        if event.char in ['w','a','s','d','W','A','S','D']:
            if current_pressed == opp[convert(event.char)]: #so you cant press w then s to immediately die
                ...
            else: #if not opposites then take the input
                self.last_pressed = convert(event.char)

        elif event.keysym in ['Up','Down','Left','Right']:
            if current_pressed == opp[event.keysym]: #so you cant press Up then Down to immediately die
                ...
            else: #if not opposites then take the input
                self.last_pressed = event.keysym

        elif event.char == ' ' and self.game_state['start'] == False: #to start game press space
            self.game_state['start'] = True
            self.move(self.last_pressed) #actually starts game

    def make(self):
        x,y=0,0
        for i in range(self.game_values['row']*self.game_values['column']): #total boxes
            if i%2 == 0:
                grids = self.canvas.create_rectangle(x,y,x+self.game_values['cell_size'],y+self.game_values['cell_size'],
                                                     fill='#1C1F2A',tag = 'snake_bg') #grey color with snake_bg tag
            else:
                grids = self.canvas.create_rectangle(x,y,x+self.game_values['cell_size'],y+self.game_values['cell_size'],
                                                     fill='#0F0F14',tag = 'snake_bg') #black color with snake_bg tag

            self.grid_loc[grids] = (x,y)#stores location of each box with number
            self.grid_loc_reverse[(x,y)] = grids

            self.canvas.tag_bind(grids,'<Button-1>',lambda e,g=grids:print(f'Number: {g}, Coord: {self.grid_loc.get(g)}'))

            if x<self.game_values['cell_size']*self.game_values['row']: #makes game_values['row']
                x+=self.game_values['cell_size']
                if x == self.game_values['cell_size']*self.game_values['row']: #makes game_values['column']
                    x = 0
                    y += self.game_values['cell_size']

        self.body_pos = [] #stores body pos

        #for getting heads location
        head_x , head_y = self.game_values['row']//2*self.game_values['cell_size'] , self.game_values['column']//2*self.game_values['cell_size'] #get coord of head position in center of board
        head_grid_no = self.grid_loc_reverse[(head_x,head_y)]
        # ^^ gets index of head then converts it into a number;first changes into string then into int

        for i in range(self.game_values['snake_size']): #runs till body size
            self.body_pos.append(self.grid_loc[head_grid_no]) #stores body id
            head_grid_no += self.game_values['row'] #cause diff btwn game_values['row'] is same so add to get other position

        #makes and colors body
        for index,item in enumerate(self.body_pos): #remakes evrything with new body position
            if index == 0: #colors head
                self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#189f11',tag = 'snake_body') #bbox gets coords of object
            elif index == len(self.body_pos) - 1: #colors tail also -1 cause index stop at len -1
                self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#175e13',tag = 'snake_body')
            else: #colors body
                self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#168211',tag = 'snake_body')
    
    def make_apple(self):
        self.canvas.delete('apple')
        x = random.randrange(0 , (self.game_values['row']  *self.game_values['cell_size']) , self.game_values['cell_size'])
        y = random.randrange(0 , (self.game_values['column'] * self.game_values['cell_size']) , self.game_values['cell_size'])

        while (x,y) in self.body_pos: #repeats this function as long as apples position exists inside snakes body
            x = random.randrange(0 , (self.game_values['row']  *self.game_values['cell_size']) , self.game_values['cell_size'])
            y = random.randrange(0 , (self.game_values['column'] * self.game_values['cell_size']) , self.game_values['cell_size'])

        self.apple_pos_main = (x,y,x+self.game_values['cell_size'],y+self.game_values['cell_size']) #this is for making apple shape
        self.apple_pos = (x,y) #apple position to compare

        self.canvas.create_oval(self.apple_pos_main,tag='apple',fill="#C11B1B")

    def move(self,event):
        x,y = self.body_pos[0]
        if self.game_state['die'] == False:
            if event == 'Up':
                self.body_pos.insert(0,(x,y-self.game_values['cell_size'])) #adds new item in front (head) also changes coordinates of head based on cell size picked
            elif event == 'Down':
                self.body_pos.insert(0,(x,y+self.game_values['cell_size']))
            elif event == 'Left':
                self.body_pos.insert(0,(x-self.game_values['cell_size'],y))
            elif event == 'Right':
                self.body_pos.insert(0,(x+self.game_values['cell_size'],y))

            if self.body_pos[0] != self.apple_pos:
                self.body_pos.pop() #removes last item (tail) if apple is not eaten
            else:
                self.make_apple() #if apple is eaten remake the apple in different position

            #this is for checking if dead and remaking body
            self.die_check()
            self.remake_body()

            self.root.after(self.tick_speed,lambda :self.move(self.last_pressed))

    def remake_body(self):
        #die check
        top = (0 , -self.game_values['cell_size']) #this is if head is over top border condition (y axis)
        bottom = (0 , self.game_values['column']*self.game_values['cell_size']) #this is if head is below bottom border condition (y axis)
        left = (-self.game_values['cell_size'] , 0) #this is if head is over left border condition (x axis)
        right = (self.game_values['row']*self.game_values['cell_size'] , 0) #this is if head is over right border condition (x axis)

        if (self.body_pos[0][1]) != (top[1]) and (self.body_pos[0][1]) != (bottom[1]) and (self.body_pos[0][0]) != (left[0]) and (self.body_pos[0][0]) != (right[0]): #remaking of snake only when it is inside border
            
            self.canvas.delete('snake_body') #deletes everything with the tag 'snake_body'

            #makes and colors body
            for index,item in enumerate(self.body_pos): #remakes evrything with new body position
                if index == 0: #colors head
                    self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#189f11',tag = 'snake_body') #bbox gets coords of object
                elif index == len(self.body_pos) - 1: #colors tail also -1 cause index stop at len -1
                    self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#175e13',tag = 'snake_body')
                else: #colors body
                    self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#168211',tag = 'snake_body')
        
        else:
            if self.game_values['mode'] in ['normal','n']: #for normal gamemode
                self.body_pos[0] = (0,0) #makes it so error doesnt occur and game stops in normal mode
                self.game_over()

            elif self.game_values['mode'] in ['infinite','i']: #for infinite gamemode

                if self.body_pos[0][1] == top[1]: #this is if it goes over top border
                    y = self.body_pos[0][1] + self.game_values['column']*self.game_values['cell_size'] #makes new coords for head
                    x = self.body_pos[0][0]

                    del self.body_pos [0] #deletes old coords
                    self.body_pos.insert(0,(x,y)) #inserts new coords in place of head

                elif self.body_pos[0][1] == bottom[1]: #this is if it goes below bottom border
                    y = self.body_pos[0][1] - self.game_values['column']*self.game_values['cell_size'] #makes new coords for head
                    x = self.body_pos[0][0]

                    del self.body_pos [0] #deletes old coords
                    self.body_pos.insert(0,(x,y)) #inserts new coords in place of head
                
                elif self.body_pos[0][0] == left[0]: #this is if it goes over left border
                    y = self.body_pos[0][1]
                    x = self.body_pos[0][0] + self.game_values['row']*self.game_values['cell_size'] #makes new coords for head

                    del self.body_pos [0] #deletes old coords
                    self.body_pos.insert(0,(x,y)) #inserts new coords in place of head

                elif self.body_pos[0][0] == right[0]: #this is if it goes over right border
                    y = self.body_pos[0][1]
                    x = self.body_pos[0][0] - self.game_values['row']*self.game_values['cell_size'] #makes new coords for head

                    del self.body_pos [0] #deletes old coords
                    self.body_pos.insert(0,(x,y)) #inserts new coords in place of head

                self.remake_body()

    def die_check(self):
        if self.body_pos[0] in self.body_pos[1:]: #checks if head collides with body
            self.game_state['die'] = True #sets snake to dead
            self.game_over()

    def game_over(self,event=None):
        if event == None: #when game is first over
            print('You died')
            self.root.unbind('<Key>') #to remove changing keys from keybind
            self.root.bind('<Key>',lambda event:self.game_over(event))

        else: #when user presses key
            if event.char == ' ': #if user presses spacebar activates restart function
                self.restart()
                self.root.unbind('<Key>')
    
    def restart(self):
        #sets every function to default
        self.game_state = {'start':False,'die':False}

        #remakes body position to default
        self.body_pos = []

        head_x , head_y = self.game_values['row']//2*self.game_values['cell_size'] , self.game_values['column']//2*self.game_values['cell_size']
        head_grid_no = self.grid_loc_reverse[(head_x,head_y)]

        for i in range(self.snake_size):
            self.body_pos.append(head_grid_no)
            head_grid_no += self.game_values['row']

if __name__ == '__main__': #this only makes snake run on this file so this wont affect menu
    game_values = {'cell_size': int(input('Cell Size: ')) , 'row': int(input('Row: ')), 'column': int(input('Column: ')), 'snake_size': int(input('Size of snake (when starting): ')), 'mode': input('Gamemode (normal[n]/infinite[i]): ').lower()}

    #game_values = {'cell_size': 40 , 'row': 15, 'column': 12, 'snake_size': 4, 'mode': 'i'}

    if game_values['row']%2 == 0: #if game_values['row'] is even no the checkerboard wont appear
        game_values['row']+=1

    root = tk.Tk()
    root.focus_force() #puts focus in the game window once done typing inputs
    root.geometry(f"{(game_values['row']+2)*game_values['cell_size']}x{(game_values['column']+3)*game_values['cell_size']}") #changes geomerty based on input
    root.title('SNAKE_W_CANV')
    snake_canv(root,game_values)
    root.resizable(False,False) #stops fullscreen
    root.mainloop()