#!/usr/bin/env python3

from commonImport import *

class TagManager:
    def __init__(self,options):
        self.options = options
        self.tagname = self.options.tagName
        self.recordname = self.options.recordName
        self.filename   = self.options.inputfile[0] 
        self.idGranularity = self.options.idGranularity

        self.detPartValues = {"EB"  : {},
                             "EEp" : {},
                             "EEm" : {}
                       }  
        self.detPartMap = {"EB"  : None,  # eta(y-axis) vs phi(x-axis)
                           "EEp" : None,
                           "EEm" : None
                       }  # equivalent to self.detPartValues but uses TH2D, might drop one of the two
        
        self.initializeHistograms()
        self.convertTxtIntoDict(self.filename)

    def __str__(self):
        mystr  = f"file name: {self.filename}\n"
        mystr += f"tag name : {self.tagname}\n"
        return mystr

    def initializeHistograms(self):
        if self.idGranularity == "crystal":
            # for EB have ieta from -85 to 85, excluding ieta = 0, and iphi from 1 to 360
            # for EE have ix and iy from 1 to 100
            self.detPartMap["EB"]  = ROOT.TH2D("EB", "Tag valus for EB", 360,0.5,360.5, 171,-85.5,85.5)
            self.detPartMap["EEp"] = ROOT.TH2D("EEp","Tag valus for EE+",100,0.5,100.5,100,0.5,100.5)
            self.detPartMap["EEm"] = ROOT.TH2D("EEm","Tag valus for EE-",100,0.5,100.5,100,0.5,100.5)
        elif self.idGranularity == "tower":
            # for EB a trigger tower is a square of 5x5 crystals, so 2448 TTs in full EB
            # for EE it is more complex, not implemented for now
            self.detPartMap["EB"]  = ROOT.TH2D("EB", "Tag valus for EB",34,-17,17,72,0.5,72.5)
        else:
            pass
            logging.warning("Has to implement this granularity (not crystal nor tower)")
            # to be implemented

    def convertTxtIntoDict(self, txtfile):
        # fo rnow assuming the format is: ieta(ix)  iphi(iy)  iz  value
        # with iz = 0 for EB
        # other columnsare possible, but not considered for now
        zToDet = {0 : "EB", 1 : "EEp", -1 : "EEm"}
        nProcessedLines = 0
        with open(txtfile) as f:
            for line in f:
                tokens = line.split()[:4]
                x,y,z = [int(t) for t in tokens[:3]]
                # for EB should put ieta on Y axis
                if zToDet[z] == "EB":
                    x,y = y,x
                    #tmp = y
                    #y = x
                    #x = tmp
                val = float(tokens[3])
                self.detPartValues[zToDet[z]][(x,y,z)] = val
                self.detPartMap[zToDet[z]].Fill(x,y,val)
                nProcessedLines += 1
        logging.info(f"Read {nProcessedLines} lines from file {txtfile}")

    def getHistograms(self, selectedPart=None):
        if selectedPart != None:
            return self.detPartMap[selectedPart]
        else:
            return self.detPartMap

    def getMapEB(self):
        return self.getHistograms(selectedPart="EB")
    def getMapEEp(self):
        return self.getHistograms(selectedPart="EEp")
    def getMapEEm(self):
        return self.getHistograms(selectedPart="EEm")

