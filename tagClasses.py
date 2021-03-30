#!/usr/bin/env python3

from commonImport import *

class TagManager:
    def __init__(self, inputfile, options):
        self.options = options
        self.tagname = self.options.tagName
        self.recordname = self.options.recordName
        self.filename   = inputfile 
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
        # other columns are possible, but not considered for now
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

class PlotManager:
    def __init__(self, h2, det, options, outdir=None):
        self.options = options
        self.det = det
        if self.det not in ['EB', 'EEp', 'EEm']:
            logging.error(" in initializeCanvas(): have to specify detPart in ['EB', 'EEp', 'EEm']")
            quit()
        self.map2D = h2
        self.canvas = None
        self.map1D = None
        self.canvas_1D = None
        self.initializeCanvas()
        self.minval = None
        self.maxval = None
        self.setMinMax()
        #self.setDistribution1D() # already called inside self.setMinMax if self.map1D == None
        self.outdir = outdir if outdir != None else "./plots_%s/" % self.det 

    def initializeCanvas(self):        
        if self.det == "EB":
            xsizeCanvas = int(1200)
            ysizeCanvas = int(xsizeCanvas * 171. / 360. + 0.1 * xsizeCanvas)
        else:
            xsizeCanvas = int(900)
            ysizeCanvas = int(800)
        self.canvas = ROOT.TCanvas("c%s" % self.det, "", xsizeCanvas, ysizeCanvas)
        self.canvas_1D = ROOT.TCanvas("c%s_1D" % self.det, "", 800, 800)

    def getDet(self):
        return self.det
    def getMap(self):
        return self.map2D
    def getMap1D(self):
        return self.map1D
    def getMax(self):
        return self.maxval
    def getMin(self):
        return self.minval
    def getMinMax(self):
        return (self.minval, self.maxval)
    def getOutdir(self):
        return self.outdir

    def setOutdir(self, outdir):
        self.outdir = outdir
        
    def centerZaxisAround1(self):
        # generally useful only for ratios, to have 1 in the middle of the axis
        # which might show as white depending on the palette
        if self.minval == None or self.maxval == None:
            self.setMinMax(mymin=self.minval, mymax=self.maxval)
        maxdiff = max(abs(self.maxval)-1.0, abs(self.minval)-1.0)
        self.minval = 1.0 - maxdiff
        self.maxval = 1.0 + maxdiff
        # the drawing function in self.makePlots() already uses self.minval and self.maxval to set the axis
        # but let's set it here as well in case one doesn't use that one for plots
        self.map2D.GetZaxis().SetRangeUser(self.minval, self.maxval)

    def setMinMax(self, mymin=None, mymax=None, reset1D=False):
        if mymin != None and mymax != None:
            self.minval = mymin
            self.maxval = mymax
        else:
            # for EB might also use skipYbin=[86] to skip ieta=0, which is bin 86, but skipSpecialVal 
            # also allows to remove dead crystals, assuming they had a special value in the input txt file 
            minz,maxz = getMinMaxHisto(self.map2D, excludeEmpty=True, sumError=False, excludeVal=self.options.setSpecial[1] if self.options.setSpecial else None) 
            self.minval = minz if mymin == None else mymin
            self.maxval = maxz if mymax == None else mymax
        if self.map1D == None or reset1D:
            self.setDistribution1D() 

    def setDistribution1D(self, nbins=101, minValOffset=1.0, maxValOffset=1.01):
        # 1.01* maxz because otherwise the upper edge value would be associated to overflow bin and not shown in the plot
        self.map1D = getTH1fromTH2(self.map2D, "map%s_distribution" % self.det, 
                                   nbins, minValOffset*self.minval, maxValOffset*self.maxval, 
                                   skipSpecialVal=self.options.setSpecial[1] if self.options.setSpecial else None)

    def makePlots(self, centerZaxisAt1=False, palette=None):
        createPlotDirAndCopyPhp(self.outdir)
        self.canvas.cd()
        if self.det == "EB":
            xaxisName = "iphi"
            yaxisName = "ieta"
        else:
            xaxisName = "iX"
            yaxisName = "iY"
        if centerZaxisAt1:
            self.centerZaxisAround1()
        drawTH2(self.map2D, xaxisName, yaxisName, "value in tag::%s,%s" % (self.minval, self.maxval),
                canvasName=self.map2D.GetName(), outdir=self.outdir,
                leftMargin=0.08, rightMargin=0.16,
                nContours=101, palette=palette if palette != None else self.options.palette, 
                passCanvas=self.canvas, drawOption="COLZ0")

        self.canvas_1D.cd()
        drawTH1(self.map1D, "value in tag", "Number of elements", outdir=self.outdir, 
                canvasName=self.map1D.GetName(),
                passCanvas=self.canvas_1D, drawStatBox=True, draw_both0_noLog1_onlyLog2=0)


    def printSummary(self, text=None):
            print("-"*30)
            print("%s summary" % self.det)
            if text:
                print("%s" % text)
            print("-"*30)
            print("entries  : {: <20} ".format(self.map1D.GetEntries()))
            print("min      : {: <20} ".format(self.minval))
            print("max      : {: <20} ".format(self.maxval))
            print("average  : {: <20} ".format(self.map1D.GetMean(1)))
            print("std.dev. : {: <20} ".format(self.map1D.GetStdDev(1)))
            print("-"*30)

