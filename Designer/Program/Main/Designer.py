################################################################################################################################
# Programming Start
################################################################################################################################

# -------------------------------------------------------------------------------------------------------------------------------
# Import Libraries
# -------------------------------------------------------------------------------------------------------------------------------
# Custom Libraries
from Nucleon import Gluonix
from Program.Base import Custom

# Default Libraries
import os
import time
import datetime
import _thread
import requests
import inspect
import warnings

# Program
from Program import Initial
from Program import View

# -------------------------------------------------------------------------------------------------------------------------------
# Customization
# -------------------------------------------------------------------------------------------------------------------------------
warnings.filterwarnings("ignore", category=DeprecationWarning)

# -------------------------------------------------------------------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------------------------------------------------------------------
Database = Gluonix.SQL("./Data/NGD.dll")
Title = "Gluonix Designer - Nucleon Automation"
Error_List = []
Error_Display = True
Error_Log = True
Log_Folder = "./Log"
Log_File = "Designer_Error.log"
Popup = []
Widget = []
Width = 16*80
Height = 9*80
Left = 50
Top = 50
Background = "#F0F0F0"

# -------------------------------------------------------------------------------------------------------------------------------
# Database Variables
# -------------------------------------------------------------------------------------------------------------------------------
Variable_Data = {}
Variable_Data_Temp = Database.Get("SELECT * FROM `Variable`", Keys=True)
for Each in Variable_Data_Temp:
        Variable_Data[Each['ID']] = Each['Data']

# -------------------------------------------------------------------------------------------------------------------------------
# Global Functions
# -------------------------------------------------------------------------------------------------------------------------------
def Error(E):
    global Error_List, Error_Display
    Error_Time = int(time.time())
    Error_List.append([E, Error_Time])
    if Error_Display:
        print(E)
    if Error_Log:
        if not os.path.exists(Log_Folder):
            os.makedirs(Log_Folder)
        Log_Path = os.path.join(Log_Folder, Log_File)
        Date = datetime.datetime.fromtimestamp(Error_Time)
        Date = Date.strftime("%Y-%m-%d %H:%M:%S")
        Line = f"{Date} - {E}"
        File_Content = []
        if os.path.exists(Log_Path):
            with open(Log_Path, "r") as File:
                File_Content = File.readlines()
            if len(File_Content) >= 10000:
                File_Content.pop()
        with open(Log_Path, "w") as File:
            File.write(Line.rstrip("\r\n") + "\n")
            File.writelines(File_Content)


def Error_Clear():
    try:
        global Error_List
        Error_List = []
    except Exception as E:
        Error("Error_Clear -> " + str(E))


def Image(Name, Ext="png"):
    try:
        Path = f"./Data/Image/{Name}.{Ext}"
        if os.path.exists(Path):
            return Path
        else:
            return "./Data/Image/Black.png"
    except Exception as E:
        Error("Image -> " + str(E))


def Data(Name):
    try:
        Path = f"./Data/{Name}"
        if os.path.exists(Path):
            return Path
        else:
            return ""
    except Exception as E:
        Error("Data -> " + str(E))


def Hide(Widget=[]):
    for Each in Widget:
        try:
            Each.Hide()
        except Exception as E:
            Error("Hide -> " + str(E))


def StartUp():
    try:
        global Main
        Main = View.Main(globals())
        Main.Frame.Show()
        Loading.Hide()
    except Exception as E:
        Error("StartUp -> " + str(E))
        
def On_Close():
    try:
        global Database
        if Main.Design.Database:
            Main.Design.Database.Close()
        Database.Close()
    except Exception as E:
        Error("On_Close -> " + str(E))
    


# -------------------------------------------------------------------------------------------------------------------------------
# GUI
# -------------------------------------------------------------------------------------------------------------------------------
GUI = Gluonix.GUI()
GUI.Config(Width=Width, Height=Height, Left=Left, Top=Top)
GUI.Config(Title=Title, Background=Background, Icon=Image("Icon", "ico"), Resizable=False)
GUI.Config(Error_Log=Error_Log, Error_Display=Error_Display)
GUI.Bind(On_Close=lambda: On_Close())
GUI.Create()

# -------------------------------------------------------------------------------------------------------------------------------
# Run GUI Initial Class
# -------------------------------------------------------------------------------------------------------------------------------
# Loading Frame
Loading = Initial.Loading(globals())
# Message Frame
Message = Initial.Message(globals())

# -------------------------------------------------------------------------------------------------------------------------------
# Run GUI View Class
# -------------------------------------------------------------------------------------------------------------------------------
# Main Frame
Main = False
Loading.Show()

# -------------------------------------------------------------------------------------------------------------------------------
# Auto Run Functions
# -------------------------------------------------------------------------------------------------------------------------------
_thread.start_new_thread(StartUp, ())

# -------------------------------------------------------------------------------------------------------------------------------
# Start GUI
# -------------------------------------------------------------------------------------------------------------------------------
GUI.Start()

################################################################################################################################
# Programming End
################################################################################################################################
