from tkinter import Tk, Button, Frame, Text
import tkinter as tk

class Scanner_Gui():
   
    def __init__(self, root1):
        root = self.root = root1
        
        root.title("Simple Nmap")
        root.geometry("400x300")
        
        self.frame = Frame(root)
        self.frame.pack(pady=20)  
        
        self.scan_button = Button(self.frame, text="Start scanning", command=self.print_hello)
        self.scan_button.pack()
        
        self.outer_text = Text(root, height=8, width=30)  
        self.outer_text.pack()
        
    def print_hello(self):
        self.outer_text.delete("1.0","end")
        self.outer_text.insert("end", "Hello world\n")  
        
    def Port_Scanning(self, starting_port, Ending_port):
        pass
    
    def service_scanning(self, Target_port):
        pass

if __name__ == '__main__':
    root = Tk()
    Scanner = Scanner_Gui(root)
    root.mainloop()
