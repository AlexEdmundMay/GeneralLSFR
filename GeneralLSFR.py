# -*- coding: utf-8 -*-
"""
Alexander May       Thu Jun 11 2020
_______________________________________________________________________________
GeneralLSFR.py
(Least Squares Fitting Routine)
_______________________________________________________________________________
Creates Graphical User Interface Which Allows User to:
    -Input Data
    -Enter an Equation With Fitting Parameters
    -Press a Button to Perform a Fit and Plot a Graph (With Residuals)
_______________________________________________________________________________
"""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from sympy import symbols, sympify, solve, lambdify
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

class Gui():
    """
    GUI class which is called to configure and run the graphical user interface
    Handles any user feedback using functions defined below
    """
    def __init__(self, window):
        """
        creates instance of GUI class and configures it.
        """
        self.window = window
            
    def setup(self):
        """
        Adds Widgets to GUI
        """
        #Gets window's frame
        frame = tk.Frame(self.window).grid()
        
        #Create a Frame for LabelFrames to be placed Into
        tFrame = tk.Frame(frame,width=650)
        tFrame.place(x=800,y=60)
        
        #Fit-Tolerence Frame
        self.tolFrame = tk.LabelFrame(tFrame,text="Input the Fit Tolerence:",
                                      width=650,height=300)
        self.tolFrame.grid()
        
        #Create Entry Box for Tolerence Input
        negFloatVal = self.window.register(self.checkNegFloat)
        self.tolEntry = tk.Entry(self.tolFrame,width=50, validate="all",
                                  validatecommand=(negFloatVal, '%P'))
        self.tolEntry.grid()
        self.tolEntry.insert(0,"0.00000001")
        
        #Fit-Parameters Frame
        self.fitParamFrame = tk.LabelFrame(tFrame,text="Input Initial Guesses"
                                 +" for Fit Parameters:",width=650,height=300)
        self.fitParamFrame.grid()
        
        #Constant-Parameters Frame
        self.constParamFrame=tk.LabelFrame(tFrame,text="Input Constant Values:"
                                 ,width=650,height=50)
        self.constParamFrame.grid()
        
        # Creates "How to Use" Button
        self.infoButton = tk.Button(frame,text="How To Use",
                                 command=self.getInfo).place(x=20, y=20)
        
        #Graph-Title Entry
        tk.Label(frame, text="Graph Title:").place(x=20, y=100)
        self.graphTitleEntry = tk.Entry(frame,width=40)
        self.graphTitleEntry.place(x=200,y=100)
        self.graphTitleEntry.insert(0,"Graph Title")
        
        #x-Axis Labels Entry
        tk.Label(frame, text="x-Axis Label:").place(x=20, y=150)
        self.xAxEntry = tk.Entry(frame,width=40)
        self.xAxEntry.place(x=200,y=150)
        self.xAxEntry.insert(0,"x-Axis Label")
        
        #y-Axis Label Entry     
        tk.Label(frame, text="y-Axis Label:").place(x=20, y=200)
        self.yAxEntry = tk.Entry(frame,width=40)
        self.yAxEntry.place(x=200,y=200)
        self.yAxEntry.insert(0,"y-Axis Label")
        
        #Searches Text for Parameters. Updates/Destroys Entry Boxes
        eqnCheck = self.window.register(self.findParams)
        
        #Equation Entry Label and Text
        tk.Label(frame, text="Enter Equation:"
                 +" (Include x and y Terms)").place(x=20, y=275)
        tk.Label(frame, text="0 = ").place(x=20, y=325)
        
        self.eqEntry = tk.Entry(frame,width=50, validate="all",
                                validatecommand=(eqnCheck,'%P'))
        self.eqEntry.place(x=70,y=325)
        self.eqEntry.insert(0,"f1*x+f2-y")      #Insert Linear Eqn as Default 
        
        #Creates Text Widget to Display Data
        self.dataText = tk.Text(frame)
        self.dataText.place(x=20,y=400, width = 700,height = 300)
        self.dataText.insert(tk.INSERT,"No Data Selected")
        self.dataText.configure(state=tk.DISABLED)
        
        #Read Data Button
        self.readDataButton = tk.Button(frame,text="Read Data",
                                 command=self.dataFromFile).place(x=20, y=710)
        self.plotDataButton = tk.Button(frame,text="Plot Data",
                                 command=self.fitData).place(x=600, y=710)
        
        #Create Label to Show the User any StatusProblems
        self.errorText = tk.Label(frame, text="Status:")
        self.errorText.place(x=20, y=800)
  
    def getInfo(self):
        """
        Display Window Which Tells User How to Use the Program
        """
        try:
            self.infoWindow         #check if window already open
            self.infoWindow.attributes("-topmost", True)     #bring to front
        except:
            #create new window to place widgets onto
            self.infoWindow = tk.Toplevel(self.window)
            self.infoWindow.title("Help Page")
            infoGui = Gui(self.infoWindow)
            infoGui.window.minsize(width=1250, height=750)
            infoGui.window.attributes("-topmost", True)     #bring to front
           
            #Info Text String
            infoString = """######################################################
GENERAL LSFR - HELP:
######################################################

Alexander May	2020
alexander.may-2@student.manchester.ac.uk
The University Of Manchester
General Equation - Least Squares Fitting Routine
Version 1.0

######################################################
ABOUT:
######################################################
This Program Uses the scipi.optimise Function curve_fit(...),
Available at:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

This Returns the Best Fit Parameters for a General Equation
As Well as the Covariance Matrix From Which the Uncertainties
Can be Calculated

######################################################
ENTERING EQUATION:
######################################################
When Entering an Equation many common functions can be used
For Example:
	-exp()
	-sin()
	-cos()...etc
To Raise Something to a power, use "**". E.g. "x**2" for x
Squared.

In Order To Perform the Fit, There Must be Fitting Parameters
To Insert a Fitting Parameter Into Your Equation type 'f'
Followed By a positive Integer. e.g. "f1","f45"...etc.After
Typing These Into Your Equation, Make Sure Their Initial Values
are Inputted on the Right Hand Side of The Screen

Constants Can Also Be Defined Using 'k' Followed by a Positive
Integer. E.g. "k1", "k2"...etc. After Typing These Into Your
Equation, Make Sure They are Defined on the Right Hand Side Of
The Screen

Make Sure That Both x and y Appear in Your Equation
e.g. The Default Linear Equation:
	"0 = f1*x + f2 - y"

######################################################
SELECTING DATA:
######################################################
Data Can be Selected Using The "Read Data" Button.

Data Should be a .csv File or .txt File (Separated by Tabs)

The File Should Have Three Columns of Data:
1. The Left Column Should Contain the x-Data
2. The Central Column Should Contain the y-Data
3. The Right Column Should Contain the y-Errors

The Data Should Have Enough Points Depending On The Number Of
Fitting Parameters

######################################################
PLOTTING DATA:
######################################################
Before Pressing the "Plot Data" Button, Make Sure:
- Data has Been Selected
- The Equation has Been Entered
- Constant Parameters Have Been Inputted
- The Fitting Parameters' Initial Values Have Been Inputted.

When Pressing the Button, If No Problems Occur, a Graph Will Be
Plotted and the Fitting Parameter Values Will Be Shown
"""
            #Creates Data Text
            infoGui.infoText = tk.Text(infoGui.window)
            infoGui.infoText.place(x=0,y=0, width = 1250,height = 750)
            infoGui.infoText.insert(tk.INSERT,infoString)
            infoGui.infoText.configure(state=tk.DISABLED)
            infoGui.window.mainloop()       #runs GUI's main loop
            
    def showFitParams(self, results):
        """
        Creates New Window Displaying The Reduced Chi-Squared, and the Values
            of Any Fitting Parameters Used
        Results is an Array containing the Reduced Chi-Squared,
            The Fitting Parameters and their Uncertainties
        """
        try:
            self.fitParamsWindow         #check if window already open
            self.fitParamsWindow.deiconify()    #If Hidden, Reopen it
            fitParamsGui = Gui(self.fitParamsWindow)   #Create New Gui Instance

        except:
            #Create New Window to Place Widgets Onto
            self.fitParamsWindow = tk.Toplevel(self.window)
            self.fitParamsWindow.title("Fitting Parameters")
            fitParamsGui = Gui(self.fitParamsWindow)   #Create New Gui Instance
        
        fitParamsGui.window.minsize(width=750, height=750)  #Set Size
        fitParamsGui.window.attributes("-topmost", True)     #Bring to Front
            
        #Creates Text Widget to Display the Text
        fitParamsGui.fitParamText = tk.Text(fitParamsGui.window)
        fitParamsGui.fitParamText.grid(row=0, column=0)
        
        #Creates String to Show Fit Results To The User            
        guiString = "Reduced Chi-Squared: "+str(results[1])+"\n"
        
        #For Each Parameter Add Data to String
        for i in range(len(self.fitParams)):
            key = list(self.fitParams.keys())[i]
            strUncert = str(np.sqrt(results[2][i][i]))
            guiString = guiString+key+": "+str(results[0][i])+"±"+strUncert+"\n"
        
        fitParamsGui.fitParamText.insert(tk.INSERT,guiString)   #Show guiString
        fitParamsGui.fitParamText.configure(state=tk.DISABLED)#No Text Editting
        fitParamsGui.window.mainloop()       #runs GUI's main loop

        
    def findParams(self,string):
        """
        Searches Equation for Fitting Parameters(f#) & Constant Parameters (k#)
        Creates Dictionaries to Be Used To Create Text Entry Boxes for Each
            Param
        string is a String Passed in by Equation Entry to Be Validated
        """
        fArray = re.findall(r'\bf\d+\b', string)#Instances of f Followed by int
        kArray = re.findall(r'\bk\d+\b', string)#Instances of k Followed by int
        
        #Make Dictionaries of Fit and Const Params With Their Values
        try:
            #If New Fit Param, Add String Value as Key in Dictionary
            for key in fArray:
                if not key in self.fitParams:
                    self.fitParams[key]=None
                    
            #If Fit Param Has Been Removed From Equation, Remove it From Dict
            keys = list(self.fitParams.keys())
            for key in keys:
                if not key in fArray:
                    self.fitParams[key][1].destroy()    #Removes Param's Entry
                    self.fitParams[key][2].destroy()    #Removes Param's Label
                    self.fitParams.pop(key)     #Removes Item From Dict
        except:
            #If No fitParams Dict, Make One From fArray  
            self.fitParams=dict.fromkeys(fArray)
        try:
            #If New Const Param, Add String Value as Key in Dictionary
            for key in kArray:
                if not key in self.constParams:
                    self.constParams[key]=None
            
            #If Const Param Has Been Removed From Equation, Remove it From Dict
            keys = list(self.constParams.keys())
            for key in keys:
                if not key in kArray:
                    self.constParams[key][1].destroy()   #Removes Param's Entry
                    self.constParams[key][2].destroy()   #Removes Param's Label
                    self.constParams.pop(key)       #Removes Item From Dict
        except:
            #If No constParams Dict, Make One From fArray
            self.constParams=dict.fromkeys(kArray)
        
        #Make Entry Boxes From Dictionaries
        self.makeParamEntries(self.fitParams,self.fitParamFrame)
        self.makeParamEntries(self.constParams,self.constParamFrame)
        
        return True     #Allow Text To be Editted
    
    def makeParamEntries(self,params,frame):
        """
        Create Entry Boxes in a Given Frame for Each Member of the Params Dict
            With a Key But No Item Inside
        Params is a Dict
        Frame is a TKinter Frame
        """
        #only allow negative floats to be entered
        negFloatVal = self.window.register(self.checkNegFloat)
        
        #Search for Empty Members of params
        for key in params.keys():
            if params[key] == None:
                #Create Text With the Name of the Fitting Parameter
                text1 = tk.Label(frame, text=key+":")
                text1.grid(sticky = "W")
                
                #Create Entry Which Only allows Negative Floats
                entry1 = tk.Entry(frame,width=50, validate="all",
                                  validatecommand=(negFloatVal, '%P'))
                entry1.grid()
                entry1.insert(0,"0.0")      #Set Default Value to 0.0
                
                #Set Dict Value to Array Containing Default Entry Value
                #and the Two Widgets
                params[key] = [0.0,entry1,text1]
                
    def checkNegFloat(self, string):
        """
        Returns True if String Can Be Cast as a Float
        string is a String Passed in by an Entry Widget to Be Validated
        """
        try:
            if string == "" or string == "-": #Allows the Empty String or Minus
                return True
            float(string)   #Checks if String Can Be Converted to a Float
            return True
        except:     #Raised If String Cannot Be Converted to a Float
            return False    #Do Not Allow Non-Floats   
        
    def fitData(self):
        """
        Function Called When "Plot Data" Button is Pressed
        Retrieves Equation, Parameter Symbols and Initial Values, the Tolerence
            And Performs a Fit Using these Values
        Scales the Reduced Chi-Squared and the Covariance Matrix
        Plots the Data With the Best Fit Line
        Shows User The Best Fit Parameters and Reduced Chi-Squared
        """
        #Check That There are Fit Params
        if self.fitParams == {}:
            self.errorText.config(text="Status: No Fitting Parameters")
        else:
            #Attempt to Retreive Equation from Equation Entry
            try:
                equation = getEquation(self.eqEntry.get())[0]   #Get Equation
            except:
                self.errorText.config(text="Status: Equation Invalid."+
                                      " Check equation contains only x,y,Known"
                                      +" Functions,Fitting Parameters and"
                                      +"Defined Constants")
                return  #Do Not Attempt Fit
            
            #Get Keys and Symbols From Param Dictionaries
            fkeys,fSymbols = self.symbolsFromParams(self.fitParams)
            kkeys,kSymbols = self.symbolsFromParams(self.constParams)
            
            #For Each Fit Parameter, Update Dictionary If Entry not Empty 
            for fkey in fkeys:
                if self.fitParams[fkey][1].get() != "":
                    self.fitParams[fkey][0]=float(self.fitParams[fkey][1].get())
                else:
                    #Otherwise Update Entry With Last Known Value
                    self.fitParams[fkey][1].insert(tk.END,
                                                   str(self.fitParams[fkey][0]))
            
            #For Each Const Parameter, Update Dictionary If Entry not Empty,
            #Substitute That Value Into the Equation
            for kkey,kSymbol in zip(kkeys,kSymbols):
                if self.constParams[kkey][1].get() != "":
                    self.constParams[kkey][0]=float(self.constParams[kkey][1].get())
                else:
                    #Otherwise Update Entry With Last Known Value
                    self.constParams[kkey][1].insert(tk.END,
                                                     str(self.constParams[kkey][0]))
                
                #Sub Constant Into Equation
                equation = equation.subs(kSymbol,self.constParams[kkey][0])
            
            #Get Initial Guesses For Fitting Parameters
            initialGuesses = [self.fitParams[i][0] for i in fkeys]
            
            #Check Data File Exists
            try:
                self.dataFile
            except:
                #Tell User That No Data Was Loaded
                self.errorText.config(text="Status: No Data Loaded")
                
                return  #Do Not Attempt Fit
            try:
                #Get Tolerence
                if self.tolEntry.get() != "":
                    ftol=abs(float(self.tolEntry.get()))
                else:
                    ftol=0.00000001
                    self.fitParams[fkey][1].insert(tk.END,str(self.fitParams[fkey][0]))
                    
                #Perform the Fit
                fitResults, cov = curve_fit(returnFunction1(fSymbols,equation),
                                            self.dataFile[:,0],self.dataFile[:,1]
                                            ,p0=initialGuesses,absolute_sigma=True
                                            ,ftol=ftol,sigma =self.dataFile[:,2])
                
                #Define a Scaling Factor to Scale the Cov Matrix & Chi-Squared
                scalingFactor = (len(self.dataFile)-len(self.fitParams))
                
                #Get Chi-Squared and Reduced Chi-Squared
                chiSqrd   = chiSquared(fitResults,self.dataFile,equation,fSymbols)                     
                redChiSqrd = chiSqrd/scalingFactor
                
                #Scale Cov Matrix to Extract Uncertainties
                cov = cov*scalingFactor/(scalingFactor+2)
                
                #Tell User that Fit Occured
                self.errorText.config(text="Status: Fit Done")
            except:
                #Tell User that Fit Failed
                self.errorText.config(text="Status: Could Not Perform Fit."+
                                      " Check Fit Parameters and Make sure "+
                                      "Equation Contains Only Valid Symbols")
                
                return  #Do Not Attempt Plot
            try:
                #Substitute in the Fit Parameters
                for i in range(len(fSymbols)):
                    equation = equation.subs(fSymbols[i],fitResults[i])
                    
                #Choose Graph's Line Colour Based on Reduced Chi-Squared
                if 0.5<=redChiSqrd<=2.0:
                    col = "b"   #Blue Line
                else:
                    col = "r"   #Red Line
                
                #Convert Equation into Function
                x = symbols("x")
                f = lambdify(x, equation)
                
                #Plot Equation and Show Fit Params
                plotEquation(f,self,col)
                self.showFitParams([fitResults,redChiSqrd,cov])
                
            except:
                #Tell User that Plot Failed 
                self.errorText.config(text="Status: Plot Failed")
                
                return      #Go back to Previous Function
    
    def symbolsFromParams(self,params):
        """
        Extracts the Keys From the params Dictionary
        Creates Sympy Symbols from those Keys
        Returns the Keys and the Symbols
        """
        
        keys = list(params.keys())      #Get Keys From params Dict
        try:
            symb = symbols(" ".join(keys))       #Try to Extract Symbols
            
            if not isinstance(symb,tuple):     #If single Symbol, make tuple
                symb = (symb,)
                
            return keys, symb   #Return Keys and Symbols
        
        except:
            symb = ()   #If 'try:' Failed Return Empty Tuple
            self.errorText.config(text="Status: No Fitting Parameters")
            
            return keys, symb   #Return Keys and Symbols
        
    def dataFromFile(self):
        """
            Opens File Select Window to Select a File
            Loads File if it is a .CSV or .TXT and Has More Than 1 Data Point
        """    
        filename, delim = getFileName()     #Get Filename and Delimiter
        
        if filename != "":
            
            #reads in data file
            self.dataFile = np.genfromtxt(filename, comments='%',
                                          delimiter = delim)   
            
            self.dataText.configure(state=tk.NORMAL)    #Make Editable
            
            if len(self.dataFile) <= 1:    #Not Enough Useable Data 
                
                #Edit text
                self.dataText.delete('1.0', tk.END)
                self.dataText.insert(tk.END,"File contained no useable data")
            else:       #Enough Data to load (Not Necessarily Enough to Fit)
                
                #Edit text
                self.dataText.delete('1.0', tk.END)
                self.dataText.insert(tk.END,self.dataFile)
                
            self.dataText.configure(state=tk.DISABLED)  #Make Uneditable
            self.errorText.config(text="Status: Selected "+filename.split("/")[-1])
        else:
            self.errorText.config(text="Status: Invalid Input, Please Select"+
                                  " a .csv or .txt File")

def chiSquared(guesses, data, equation, fitParams):
    """
    Calculates and Returns the Chi-Squared
    Requires the Data File (Array), the Equation Being Fit (Sympy Expression),
        The Fit Params (Sympy Symbols) and their Guess Values (array)
    """
    #Define x Symbol
    x = symbols("x")
    
    #Extract x,y and y_err Data from inputted Data Array
    x_data = data[:,0]
    y_data = data[:,1]
    y_err = data[:,2]

    #y-value given by inputted equation
    expr = equation
    for param,guess in zip(fitParams,guesses):
        #Substitute in Guesses
        expr = expr.subs(param, guess)
        
    try:   
        #Try to Create Function from Sympy Expression
        f = lambdify([x], expr)   
        
        #Get y-values Predicted by Expression
        yEquationValues = f(x_data)
    except:
        print("Error")
        raise SystemExit
    
    #Calculate  and Return the Chi-Squared       
    chiSquared = np.sum(((y_data-yEquationValues)/y_err)**2)
    return chiSquared      
 
def plotEquation(func,gui,col):
    """
    Plots the Data Stored in gui (Member of Gui() Class)
    Plots func(x) (The Fitted Data Function)
    Plots Residuals
    col is a String Determining the Colour of the Fit Line
    """
    #Define Data
    data = gui.dataFile
    
    #Extract x,y and y_err Data from inputted Data Array
    x_data = data[:,0]
    y_data = data[:,1]
    y_err = data[:,2]
    
    plt.close(1)    #Close Figure 1 if One is Already Open
    fig = plt.figure(1)     #Open New Figure 1
    
    #Define two Axes
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    
    #Set Grid to On
    ax1.grid(b=True)
    ax2.grid(b=True)
    
    #Set Labels For Each of the Axes
    ax1.set_title(gui.graphTitleEntry.get())
    ax1.set_ylabel(gui.yAxEntry.get())
    ax2.set_ylabel("Residuals")
    ax2.set_xlabel(gui.xAxEntry.get())

    #Plot Main Axes
    ax1.errorbar(x_data,y_data,y_err, linestyle='none', color='k')  #plot data
    ax1.plot(x_data,func(x_data), color=col)    #plot fit
    
    #Plot Residual Axes
    ax2.errorbar(x_data,y_data-func(x_data),y_err,linestyle='none', color='k')
    ax2.plot(x_data,np.zeros(len(x_data)), color=col)    #plot fit
    
    plt.show()  #Show Plot
    
def getEquation(string):
    """
    Given a String Value, Convert Into a SymPy Expression and Solve for y
    Returns the SymPy Expression
    """ 
    #Define y Symbol
    y = symbols("y")
    
    #Convert to SymPy Expression
    expression = sympify(string)
    
    #Solve for y
    expression = solve(expression,y)
    return expression

def returnFunction1(*args):
    """
    Nested Function so That Extra Variables Can be Passed Into Curve_Fit
    Extra Variables are fitSymbols (Array of SymPy Symbols) and equation
        (SymPy Expression)
    Returns the Equation Inputted With the Curve_Fit Trial Guesses Substituted
        Into the Equation
    """
    #Define fitSymbols and Equation
    fitSymbols,equation = args
    
    #Define Nested Function
    def returnFunction2(x,*param):
        
        #Define fitSymbols and Equation
        fitSymbols,equation = args
        
        #Define x Symbol
        xSymb = symbols("x")
        
        #For Each Fit Symbol, Substitute its Respective Trial Value into
        #the Equation
        for i in range(len(fitSymbols)):
            equation = equation.subs(fitSymbols[i],param[i])    #Sub in Symbol
            
        #Convert SymPy Expression to Function of x
        f = lambdify(xSymb, equation)
        
        #Returns the Value of the Function Applied to the x Values
        return f(x)
    
    #Call Nested Function
    return returnFunction2

def getFileName():
    """
    Opens File Selection Window and if Selected File is a .csv or .txt
    Returns the Filename and the Delimeter
    """
    #Opens File Selector and Brings it to Front
    fileName = askopenfilename()
    
    #If Cancel Pressed, Exit Program
    if fileName == "":
        print("No File Selected")
        
    #Check  ends in ".csv" or ".txt"
    split = fileName.split(".")
    
    if split[1] != "csv" and split[1] != "txt":     #Neither .csv or .txt
        #Return Empty Strings
        return "",""
    
    elif split[1] == "csv":     #File is a .csv
        #Return File Name and "," as the Delimeter
        return fileName, ","
    
    elif split[1] == "txt":     #File is a .txt
        #Return File Name and a Tab as the Delimeter
        return fileName, "\t"
    
def main():
    """
    Main Function, Opens Gui, Sets it Up and Runs It's Main Loop
    """
    try:
        #Create New Window to Place Widgets Onto
        window = tk.Tk()    
        
        #Initialise  and Set-Up Graphical User Interface
        gui = Gui(window)   
        gui.window.title("General LSFR")
        gui.window.minsize(width=1500, height=850)
        gui.setup()         #adds widgets to window
        
        #window bring to front
        window.attributes("-topmost", True)  
        
        #runs GUI's main loop
        gui.window.mainloop()       
        window.withdraw()
        
    except SystemExit:      #catch any attempt to end program
        print("Terminating program")
        
        #Close Any Open Windows By Closing Main Gui (Does Not Close Graphs)
        gui.window.destroy()        #closes window
    
    except tk.TclError:      #catch any attempt to close GUI
        print("Terminating program")

#Run Main Function    
if __name__ == "__main__":
    main()
                    