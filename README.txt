######################################################
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
