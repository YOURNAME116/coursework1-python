import os
import tkinter as tk
import time

class Reading_wordlist:
    def __init__(self, path, output_frame):
        self.path_to_file = path
        self.output_frame = output_frame

    def Reading_file(self):
        words = set()

        try:
            if os.path.splitext(self.path_to_file)[1] == ".txt":
                if os.path.isfile(self.path_to_file):
                    with open(self.path_to_file, "r") as file:
                        words = {line.strip() for line in file if line.strip()}
                    return words
                else:
                    self.output_frame.insert(tk.END, f'"{self.path_to_file}" file path not found\n')
            else:
                self.output_frame.insert(tk.END, "File extension is not supported, Make sure to use '.txt' file\n")
        except FileNotFoundError:
            pass

def run_tk():
    def on_button_click():
        path = entry.get()
        word_set = Reading_wordlist(path, output_frame).Reading_file()
        if word_set is not None:
            output_frame.insert(tk.END, word_set)
        count = 1
        while word_set is None:
            count = count + 1
            if count > 3:
                output_frame.insert(tk.END,"********************************* Quitting !! Due to incorrect input for 3 times ****")

        

    app = tk.Tk()
    app.title("Reading Wordlist")

    label = tk.Label(app, text="Enter the path to the wordlist:")
    label.pack()

    entry = tk.Entry(app)
    entry.pack()

    button = tk.Button(app, text="Read Wordlist", command=on_button_click)
    button.pack()

    output_frame = tk.Text(app, height=10, width=80)
    output_frame.pack()

    app.mainloop()

if __name__ == "__main__":
    run_tk()
