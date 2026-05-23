import tkinter as tk

class snake_canv:
    def __init__(self,root,row,column,cell_size):
        self.root = root
        self.row = row
        self.column = column
        self.cell_size = cell_size

        self.frame = tk.Frame(self.root,width = row*cell_size,
                              height = column*cell_size,bg='black') ; self.frame.pack(expand='True') #changes geomerty based on row and column
        self.canvas = tk.Canvas(self.frame,width=self.frame.cget('width'),height=self.frame.cget('height')) ; self.canvas.pack() #same size as frame so its in seperate place than root
        
        self.grid_loc = {}

        self.lab = tk.Label(self.root, #for testing
                            text=f'Cell Size: {self.cell_size}\nRow,Column: {self.row,self.column}\nSize of Frame/Canvas: {self.row*self.cell_size,self.column*self.cell_size}\nSize of window: {(self.row+2)*self.cell_size,(self.column+2)*self.cell_size}',
                            fg='black') ; self.lab.pack() #for test
        self.make()

    def make(self):
        x,y=0,0
        for i in range(self.row*self.column): #total boxes
            if i%2 == 0:
                grids = self.canvas.create_rectangle(x,y,x+self.cell_size,y+self.cell_size,fill='#1C1F2A') #grey
            else:
                grids = self.canvas.create_rectangle(x,y,x+self.cell_size,y+self.cell_size,fill='#0F0F14') #black

            self.grid_loc[grids] = (x,y)#stores location of each box with number

            self.canvas.tag_bind(grids,'<Button-1>',lambda e,g=grids:print(self.grid_loc.get(g)))

            if x<self.cell_size*self.row: #makes row
                x+=self.cell_size
                if x == self.cell_size*self.row: #makes column
                    x = 0
                    y += self.cell_size

if __name__ == '__main__':
    #cell_size , row , column = int(input('Cell Size: ')) , int(input('Row: ')) , int(input('Column: '))
    cell_size , row , column = 40 , 15 , 12
    root = tk.Tk()
    root.geometry(f'{(row+2)*cell_size}x{(column+2)*cell_size}') #changes geomerty based on input
    root.title('SNAKE_W_CANV')
    snake_canv(root,row,column,cell_size)
    root.resizable(False,False) #stops fullscreen
    root.mainloop()