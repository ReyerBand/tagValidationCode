#!/usr/bin/env python3
 
from commonImport import *
from tagClasses import TagManager, PlotManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str, nargs=1)
    parser.add_argument("outdir",   type=str, nargs=1)
    parser.add_argument("-r", "--recordName", type=str, default="", help="Record name")
    parser.add_argument("-t", "--tagName",    type=str, default="", help="Tag name")
    parser.add_argument("-g", "--idGranularity", type=str, choices=["crystal", "tower"], default="crystal", help="Granularity for the content of the tag object")
    parser.add_argument("-v", "--verbose", type=int, choices=[0,1,2,3,4], default=3, help="Verbose mode")
    parser.add_argument("--setSpecial", type=float, nargs=2, default=None, help="Set the values for special bins to this value. First argument is used to specify which value corresponds to a spacial bin (e.g. it could be an empty one), second one is the new thresholds)")
    parser.add_argument("--setMapRangeEB", type=float, nargs=2, default=(0, -1), help="Range for 2D map in EB (if min > max, the default range is used)")
    parser.add_argument("--setMapRangeEE", type=float, nargs=2, default=(0, -1), help="Range for 2D map in EE (if min > max, the default range is used)")
    parser.add_argument("-p", "--palette", type=int, default=55, help="Palette for 2D maps")
    parser.add_argument("--ref", "--reference", dest="reference", type=str, default="", help="Pass another file that will be used as a reference to make ratios and other comparisons")
    # add other actions
    args = parser.parse_args()

    verboseLevel = {0 : logging.CRITICAL,
                    1 : logging.ERROR,
                    2 : logging.WARNING,
                    3 : logging.INFO,
                    4 : logging.DEBUG}

    logging.basicConfig(level=verboseLevel[args.verbose])

    fname = args.inputfile[0]
    outdir = args.outdir[0] + "/"
    createPlotDirAndCopyPhp(outdir)

    tgVal = TagManager(args.inputfile[0], args)

    mapEB  = tgVal.getMapEB()
    mapEEp = tgVal.getMapEEp()
    mapEEm = tgVal.getMapEEm()
    if args.setSpecial:        
        oldval = args.setSpecial[0]
        newval = args.setSpecial[1]
        logging.info(f"setting map values from {oldval} to {newval}")
        updateMapValue(mapEB, oldval, newval)
        updateMapValue(mapEEp, oldval, newval)
        updateMapValue(mapEEm, oldval, newval)

    adjustSettings_CMS_lumi() # just a dummy function to fix some settings in canvas later on

    plotEB  = PlotManager(mapEB,   "EB",  args, outdir=outdir)
    if args.setMapRangeEB[0] < args.setMapRangeEB[1]:
        plotEB.setMinMax(args.setMapRangeEB[0], args.setMapRangeEB[1])
    plotEB.makePlots()
    plotEB.printSummary()

    plotEEp = PlotManager(mapEEp,  "EEp", args, outdir=outdir)
    if args.setMapRangeEE[0] < args.setMapRangeEE[1]:
        plotEB.setMinMax(args.setMapRangeEE[0], args.setMapRangeEE[1])
    plotEEp.makePlots()
    plotEEp.printSummary()

    plotEEm = PlotManager(mapEEm, "EEm", args, outdir=outdir)
    if args.setMapRangeEE[0] < args.setMapRangeEE[1]:
        plotEB.setMinMax(args.setMapRangeEE[0], args.setMapRangeEE[1])
    plotEEm.makePlots()
    plotEEm.printSummary()

    if args.reference != "":

        tgValRef = TagManager(args.reference, args)
        refMapEB  = tgValRef.getMapEB()
        refMapEEp = tgValRef.getMapEEp()
        refMapEEm = tgValRef.getMapEEm()
        if args.setSpecial:        
            oldval = args.setSpecial[0]
            newval = args.setSpecial[1]
            logging.info(f"setting reference map values from {oldval} to {newval}")
            updateMapValue(refMapEB, oldval, newval)
            updateMapValue(refMapEEp, oldval, newval)
            updateMapValue(refMapEEm, oldval, newval)
        ratioMapEB = makeHistogramRatio(mapEB, refMapEB, "ratioEB_overRef", 
                                        valForNullDen=1, valToKeepFromDen=None)
        ratioMapEEp = makeHistogramRatio(mapEEp, refMapEEp, "ratioEEp_overRef", 
                                         valForNullDen=1, valToKeepFromDen=None)
        ratioMapEEm = makeHistogramRatio(mapEEm, refMapEEm, "ratioEEm_overRef", 
                                         valForNullDen=1, valToKeepFromDen=None)

        outdirRatio = outdir + "ratioWithRef/"
        createPlotDirAndCopyPhp(outdirRatio)

        plotEB  = PlotManager(ratioMapEB,   "EB",  args, outdir=outdirRatio)
        plotEB.makePlots(centerZaxisAt1=True, palette=-1)
        plotEB.printSummary(text="ratio with reference map")

        plotEEp = PlotManager(ratioMapEEp,  "EEp", args, outdir=outdirRatio)
        plotEEp.makePlots()
        plotEEp.printSummary(text="ratio with reference map")

        plotEEm = PlotManager(ratioMapEEm, "EEm", args, outdir=outdirRatio)
        plotEEm.makePlots()
        plotEEm.printSummary(text="ratio with reference map")
