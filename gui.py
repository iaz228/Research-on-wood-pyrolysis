# Creator: Ian Zalewski on 5.7.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Use previous functions and programs in a easy to use GUI


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import folderSegmenter as fS


class imageSegmenterApp(tk.Tk):
    def __init__(self):
        #Gives access to functions of tk.Tk
        super().__init__()
        self.title("Image Processing for Pyrolosis Research")
        
        #Creates self varaibles to be passed through to the folder segmeneter function
        self.inputs = {"outputFilePath": "", "chopAmount": 0.1, "chopRate": 0.01, "shape": "Circle", "inputFilePath": ""}

        # Build the layout elements cleanly
        self.create_widgets()



    def create_widgets(self):
        inputFrame = tk.Frame()

        #For output file path gathering
        lOutputFilePath = tk.Label(text="File Path:", master=inputFrame)
        eOutputFilePath = tk.Entry(master=inputFrame)
        bOutputFilePath = tk.Button(master= inputFrame, command=lambda: self.generalEntryGet("outputFilePath", bOutputFilePath, eOutputFilePath, False))

        lOutputFilePath.grid(row=0, column=0, padx=5, pady=5)
        eOutputFilePath.grid(row=0, column=1, padx=5, pady=5)
        bOutputFilePath.grid(row=0, column=2, padx=5, pady=5)



        #For combo box for the shape that should be tested for 

        self.shapeLabel = tk.Label(text = "Shape: ", master = inputFrame)
        self.shapeCombobox = ttk.Combobox(inputFrame, values=["Circle", "Rectangle"])
        self.shapeCombobox.set("Circle")
        self.shapeCombobox.bind("<<ComboboxSelected>>", self.comboBoxSelectionChange)

        self.shapeLabel.grid(row=1, column=0, padx=5, pady=5)
        self.shapeCombobox.grid(row=1, column=1, padx=5,pady=5)




        #For output chop amount gathering
        lChopAmount = tk.Label(text="Chop Amount:", master=inputFrame)
        eChopAmount = tk.Entry(master=inputFrame)
        bChopAmount = tk.Button(master= inputFrame, command = lambda: self.generalEntryGet("chopAmount", bChopAmount, eChopAmount, True))

        lChopAmount.grid(row=2, column=0, padx=5, pady=5)
        eChopAmount.grid(row=2, column=1, padx=5, pady=5)
        bChopAmount.grid(row=2, column=2, padx=5, pady=5)



        #For output chop rate change gathering
        lChopRateChange = tk.Label(text="Chop Rate Change:", master=inputFrame)
        eChopRateChange = tk.Entry(master=inputFrame)
        bChopRateChange = tk.Button(master= inputFrame, command = lambda: self.generalEntryGet("chopRate", bChopRateChange, eChopRateChange, True))

        lChopRateChange.grid(row=3, column=0, padx=5, pady=5)
        eChopRateChange.grid(row=3, column=1, padx=5, pady=5)
        bChopRateChange.grid(row=3, column=2, padx=5, pady=5)


        #For getting input path, opens dialog when button is pressed
        self.lInputPath = tk.Label(text = "Input Path:", master=inputFrame)
        self.lInputPathText = tk.Label(text = "", master=inputFrame)
        self.bInputPath = tk.Button(master= inputFrame, command = self.getFilePath)
        
        self.lInputPath.grid(row=4, column = 0)
        self.bInputPath.grid(row=4, column = 1)
        self.lInputPathText.grid(row=4, column = 2)



        #Start Button
        self.startButton = tk.Button(width=20, height = 20, master = inputFrame, text = "START!", highlightbackground= "green", command = self.startSegmenting)

        self.startButton.grid(row = 5, column = 1)

        
        inputFrame.pack()


    #Gets entry from associated entry widget and changes button color if change in entry value has happened to signal input has been applied
    def generalEntryGet(self, dictKey, buttonObject, entryObject, numBool):
        temp = self.inputs[dictKey]

        if numBool:
            self.inputs[dictKey] = float(entryObject.get())
        else: 
            self.inputs[dictKey] = entryObject.get()

        if(temp != self.inputs[dictKey]):
            buttonObject.config(bg="green", highlightbackground="green")

        print(self.inputs[dictKey])



    def comboBoxSelectionChange(self):
        self.inputs["shape"] = self.shapeCombobox.get()


    def getFilePath(self):
        self.inputs["inputFilePath"] = filedialog.askdirectory()
        self.lInputPathText.config(text=self.inputs["inputFilePath"])

   
    def startSegmenting(self):
        print("STARTING!!!!!!!!!!")

        self.startButton.config(text = "In Progress", state="disabled")

        fS.segmentFolder(self.inputs["inputFilePath"], self.inputs["shape"], self.inputs["outputFilePath"])

        self.startButton.config(text = "Start!!!", state="active")








if __name__ == "__main__":
    app = imageSegmenterApp()
    app.mainloop()
