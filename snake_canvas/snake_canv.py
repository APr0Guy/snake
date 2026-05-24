import tkinter as tk

def convert(char):
    if char in ['w','W']:
        return 'Up'
    elif char in ['s','S']:
        return 'Down'
    elif char in ['d','D']:
        return 'Right'
    elif char in ['a','A']:
        return 'Left'

class snake_canv:
    def __init__(self,root,row,column,cell_size,snake_size,mode):
        self.root = root
        self.row = row
        self.column = column
        self.cell_size = cell_size
        self.snake_size = snake_size #for size of snake
        self.mode = mode

        self.perm_tick_speed = 500 #for speed of snake
        self.start = False #for detecting if game has started
        self.die = False #for making moving only work if not dead
        self.tick_speed = self.perm_tick_speed

        self.frame = tk.Frame(self.root,width = row*cell_size,
                              height = column*cell_size,bg='black') ; self.frame.pack(expand='True') #changes geomerty based on row and column
        self.canvas = tk.Canvas(self.frame,width=self.frame.cget('width'),height=self.frame.cget('height')) ; self.canvas.pack() #same size as frame so its in seperate place than root
        
        self.grid_loc = {}

        self.lab = tk.Label(self.root, #for testing
                            text=f'Cell Size: {self.cell_size}\nRow,Column: {self.row,self.column}\nSize of Frame/Canvas: {self.row*self.cell_size,self.column*self.cell_size}\nSize of window: {(self.row+2)*self.cell_size,(self.column+2)*self.cell_size}',
                            fg='black') ; self.lab.pack() #for test
        self.make()

        self.last_pressed = 'Up'
        self.root.bind('<Key>',self.change_key)
    
    def change_key(self,event):
        if event.char in ['w','a','s','d','W','A','S','D']:
            self.last_pressed = convert(event.char)

        elif event.keysym in ['Up','Down','Left','Right']:
            self.last_pressed = event.keysym

        elif event.char == ' ' and self.start == False: #to start game press space
            self.start = True
            self.move(self.last_pressed) #actually starts game

    def make(self):
        x,y=0,0
        for i in range(self.row*self.column): #total boxes
            if i%2 == 0:
                grids = self.canvas.create_rectangle(x,y,x+self.cell_size,y+self.cell_size,
                                                     fill='#1C1F2A',tag = 'snake_bg') #grey
            else:
                grids = self.canvas.create_rectangle(x,y,x+self.cell_size,y+self.cell_size,
                                                     fill='#0F0F14',tag = 'snake_bg') #black

            self.grid_loc[grids] = (x,y)#stores location of each box with number

            self.canvas.tag_bind(grids,'<Button-1>',lambda e,g=grids:print(f'Number: {g}, Coord: {self.grid_loc.get(g)}'))

            if x<self.cell_size*self.row: #makes row
                x+=self.cell_size
                if x == self.cell_size*self.row: #makes column
                    x = 0
                    y += self.cell_size

        self.body_pos = [] #stores body pos
        self.pos = [] #stores oval pos

        #for getting heads location
        head_x , head_y = self.row//2*self.cell_size , self.column//2*self.cell_size #get coord of head position in center of board
        head_grid_no = int(''.join([str(i) for i in self.grid_loc if self.grid_loc[i] == (head_x,head_y)]))
        # ^^ gets index of head then converts it into a number;first changes into string then into int

        for i in range(self.snake_size): #runs till body size
            self.body_pos.append(head_grid_no) #stores body id
            head_grid_no += self.row #cause diff btwn row is same so add to get other position

        #makes and colors body
        for i in self.body_pos:
            if self.body_pos.index(i) == 0: #colors head
                self.canvas.create_oval(self.canvas.bbox(i),fill='#189f11',tag = 'snake_body') #bbox gets coords of object i is id of object
            elif self.body_pos.index(i) == len(self.body_pos) - 1: #colors tail also -1 cause index stop at len -1
                self.canvas.create_oval(self.canvas.bbox(i),fill='#175e13',tag = 'snake_body')
            else: #colors body
                self.canvas.create_oval(self.canvas.bbox(i),fill='#168211',tag = 'snake_body')

    def move(self,event):
        if self.die == False:
            if event == 'Up':
                self.body_pos.insert(0,self.body_pos[0]-self.row) #adds new item in front (head)
            elif event == 'Down':
                self.body_pos.insert(0,self.body_pos[0]+self.row) #adds new item in front (head)
            elif event == 'Left':
                self.body_pos.insert(0,self.body_pos[0]-1) #adds new item in front (head)
            elif event == 'Right':
                self.body_pos.insert(0,self.body_pos[0]+1) #adds new item in front (head)

            self.body_pos.pop() #removes last item (tail)
            self.remake_body()
            self.die_check()
            self.root.after(self.tick_speed,lambda :self.move(self.last_pressed))

    def die_check(self):
        if self.body_pos[0] in self.body_pos[1:-1]:
            self.die = True
            print('You died')
            if self.mode == 'normal':
                ...
            elif self.mode == 'infinite':
                ...
            self.game_over()

    def game_over(self):
        ...

    def remake_body(self):
        self.canvas.delete('snake_body') #deletes everything with the tag 'snake_body'
        for index,item in enumerate(self.body_pos): #remakes evrything with new body position
            if index == 0: #colors head
                self.canvas.create_oval(self.canvas.bbox(item),fill='#189f11',tag = 'snake_body') #bbox gets coords of object i is id of object
            elif index == len(self.body_pos) - 1: #colors tail also -1 cause index stop at len -1
                self.canvas.create_oval(self.canvas.bbox(item),fill='#175e13',tag = 'snake_body')
            else: #colors body
                self.canvas.create_oval(self.canvas.bbox(item),fill='#168211',tag = 'snake_body')

if __name__ == '__main__': #this only makes snake run on this file so this wont affect menu 
    #cell_size , row , column , snake_size , mode = int(input('Cell Size: ')) , int(input('Row: ')) , int(input('Column: ')), int(input('Size of snake (when starting): ')) , input('Gamemode (normal/infinite): ')
    cell_size , row , column , snake_size , mode = 40 , 15 , 12 , 4 , 'normal'

    if row%2 == 0: #if row is even no the checkerboard wont appear
        row+=1

    root = tk.Tk()
    root.geometry(f'{(row+2)*cell_size}x{(column+3)*cell_size}') #changes geomerty based on input
    root.title('SNAKE_W_CANV')
    snake_canv(root,row,column,cell_size,snake_size,mode)
    root.resizable(False,False) #stops fullscreen
    root.mainloop()