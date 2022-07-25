import tkinter as tk
from tkinter import ttk
import languages as lang
from pprint import pprint, pformat

#pprint(lang.PAN.conjugateVerb('amitha'))

LANGUAGES = ["Proto-North-Anfean","Proto-North-Anfean","-Proto-Yamic","-Žahare","--Classical Ahazar","---Later Ahazar","----Old Kinwan","-----Modern Kinwan","-Ohhiyo"]

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title('Inflections')
        self.geometry('1000x800')
        self.resizable(True, True)
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        self.iconbitmap('icon.ico')

        self.optionsFrame = ttk.Frame(self)
        self.optionsFrame.grid(row=0,column=0,sticky="NS")

        self.languagesFrame = ttk.LabelFrame(self.optionsFrame, text="Select Language")
        self.languagesFrame.grid(row=0,column=0,padx=10,pady=10,sticky="EW")

        self.langVars = tk.StringVar(self.languagesFrame)
        self.langDropDown = ttk.OptionMenu(self.languagesFrame, self.langVars, *LANGUAGES)
        self.langDropDown.pack(fill=tk.X)

        self.inputFrame = ttk.LabelFrame(self.optionsFrame, text="Input Word")
        self.inputFrame.grid(row=1,column=0,padx=10,pady=0,sticky="EW")
        self.inputWord=ttk.Entry(self.inputFrame, exportselection=0,)
        self.inputWord.pack(fill=tk.X)

        self.outputFrame = ttk.LabelFrame(self, text="Output Text")
        self.outputFrame.grid(row=0,column=1,padx=10,pady=10,sticky="NSEW")
        self.outputText = tk.Text(self.outputFrame)#, height = 100, width = 500)
        self.outputText.pack(expand=True, fill='both')

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.radioFrame = ttk.LabelFrame(self.optionsFrame, text="Part of Speech")
        self.radioFrame.grid(row=2,column=0,padx=10,pady=10,sticky="EW")

        self.radioVars = tk.StringVar(self.radioFrame)
        self.nounRadio = ttk.Radiobutton(self.radioFrame,text="Noun",variable=self.radioVars, val=1)
        self.verbRadio = ttk.Radiobutton(self.radioFrame,text="Verb",variable=self.radioVars, val=2)
        self.nounRadio.pack(side=tk.LEFT)
        self.verbRadio.pack(side=tk.RIGHT)

        self.detail = tk.IntVar()
        self.detailButton = ttk.Checkbutton(self.optionsFrame,text="Detail",variable=self.detail,onvalue=1,offvalue=0)
        self.detailButton.grid(row=4,column=0,padx=10,pady=0,sticky="E")

        self.runButton = ttk.Button(self.optionsFrame, text="Inflect",command=self.writeToOutput)
        self.runButton.grid(row=3,column=0,padx=10,pady=0,sticky="EW")


    def writeToOutput(self):
        self.outputText.delete(1.0,tk.END)
        pos = int(self.radioVars.get()) # 1 = noun | 2 = verb
        language = str(self.langVars.get())
        print(self.inputWord.get())
        self.outputText.insert(tk.INSERT,lang.LangSorter(language,
                                                         pos,
                                                         str(self.inputWord.get()),
                                                         int(self.detail.get())))


if __name__ == "__main__":
    app = App()
    app.mainloop()
