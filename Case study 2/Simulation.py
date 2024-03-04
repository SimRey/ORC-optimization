from fileinput import filename
import os
from re import A
from tokenize import String
from typing import Union, Dict, Literal
import win32com.client as win32
import numpy as np
import time


class Simulation():
    AspenSimulation = win32.gencache.EnsureDispatch("Apwn.Document")

    def __init__(self, AspenFileName, WorkingDirectoryPath, VISIBILITY=False):
        os.chdir(WorkingDirectoryPath)
        self.AspenSimulation.InitFromArchive2(os.path.abspath(AspenFileName))
        self.AspenSimulation.Visible = VISIBILITY
        self.AspenSimulation.SuppressDialogs = True
    
    def Give_AspenDocumentName(self):
        return self.AspenSimulation.FullName


    def CloseAspen(self):
        AspenFileName = self.Give_AspenDocumentName()
        self.AspenSimulation.Close(os.path.abspath(AspenFileName))
    
    
    @property
    def BLK(self):
        return self.AspenSimulation.Tree.Elements("Data").Elements("Blocks")

    @property
    def STRM(self):
        return self.AspenSimulation.Tree.Elements("Data").Elements("Streams")

    def EngineRun(self):
        self.AspenSimulation.Run2()

    def EngineStop(self):
        self.AspenSimulation.Stop()

    def EngineReinit(self):
        self.AspenSimulation.Reinit()

    def Convergence(self):
        converged = self.AspenSimulation.Tree.Elements("Data").Elements("Results Summary").Elements(
                           "Run-Status").Elements("Output").Elements("PER_ERROR").Value
        return converged == 0
    
    def Reinitialize(self):
        self.STRM.RemoveAll()
        self.BLK.RemoveAll()
        self.AspenSimulation.Reinit()



class Stream(Simulation):
    def __init__(self, inlet=False):
        self.name = "S1"       
        self.inlet = inlet

        if self.inlet:
            self.inlet_stream()
    
    def inlet_stream(self):
        T = self.inlet[0]
        P = self.inlet[1]
        comp = self.inlet[2]

        self.STRM.Elements(self.name).Elements("Input").Elements("TEMP").Elements("MIXED").Value = T
        self.STRM.Elements(self.name).Elements("Input").Elements("PRES").Elements("MIXED").Value = P
        self.STRM.Elements(self.name).Elements("Input").Elements("TOTFLOW").Elements("MIXED").Value = 1.0

        for chemical in comp:
            self.STRM.Elements(self.name).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(
                chemical).Value = comp[chemical]
    
    def get_temp(self):
        return self.STRM.Elements(self.name).Elements("Output").Elements("TEMP_OUT").Elements("MIXED").Value
    
    def get_press(self):
        return self.STRM.Elements(self.name).Elements("Output").Elements("PRES_OUT").Elements("MIXED").Value
    
    def get_molar_flow(self, compound):
        return self.STRM.Elements(self.name).Elements("Output").Elements("MOLEFLOW").Elements("MIXED").Elements(compound).Value
    
    def get_total_molar_flow(self):
        return self.STRM.Elements(self.name).Elements("Output").Elements("MOLEFLMX").Elements("MIXED").Value
    
    def get_vapor_fraction(self):
        return self.STRM.Elements(self.name).Elements("Output").Elements("STR_MAIN").Elements("VFRAC").Elements("MIXED").Value



class Block(Simulation):
    def __init__(self, name):
        self.name = name.upper()


# -------------------------------------------------- UNIT OPERATIONS ------------------------------------------------
class Boiler(Block):
    def __init__(self, name="BOILER"):
        super().__init__(name)
        self.name = name
    
    def enery_consumption(self):
        q = abs(self.BLK.Elements(self.name).Elements("Output").Elements("QCALC").Value)
        return q

class Condenser(Block):
    def __init__(self, name="COND"):
        super().__init__(name)
        self.name = name
    
    def enery_consumption(self):
        q = abs(self.BLK.Elements(self.name).Elements("Output").Elements("QCALC").Value)
        return q


class Pump(Block):
    def __init__(self, press, name="PUMP"):
        super().__init__(name)
        self.press = press
        self.name = name
  
    def enery_consumption(self):
        q = abs(self.BLK.Elements(self.name).Elements("Output").Elements("WNET").Value)
        return q


class Turbine(Block):
    def __init__(self, name="TURB"):
        super().__init__(name)
        self.name = name
  
    def enery_consumption(self):
        q = abs(self.BLK.Elements(self.name).Elements("Output").Elements("WNET").Value)
        return q











