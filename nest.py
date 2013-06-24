from Tkinter import *

class MyApp:
  def __init__(self, parent):
    
    self.myParent = parent 

    self.myContainer1 = Frame(parent) 
    self.myContainer1.pack()
    
    self.top_frame = Frame(self.myContainer1) 
    self.top_frame.pack(side=TOP,
      fill=BOTH, 
      expand=YES,
      )  

    self.left_frame = Frame(self.top_frame, background="red",
      borderwidth=5,  relief=RIDGE,
      height=250, 
      width=50, 
      )
    self.left_frame.pack(side=LEFT,
      fill=BOTH, 
      expand=YES,
      )

    self.right_frame = Frame(self.top_frame, background="tan",
      borderwidth=5,  relief=RIDGE,
      width=250,
      )
    self.right_frame.pack(side=RIGHT,
      fill=BOTH, 
      expand=YES,
      ) 


root = Tk()
myapp = MyApp(root)
root.mainloop()


           
       
