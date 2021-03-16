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
    parser.add_argument("--setSpecial", type=float, nargs=2, default=None, help="Set the values for special bins to this value. Ffirst argument is used to specify which value corresponds to a spacial bin (e.g. it could be an empty one), second one is the new thresholds)")
    parser.add_argument("-p", "--palette", type=int, default=55, help="Palette for 2D maps")
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

    tgVal = TagManager(args)

    # all the following might go into another function or class, which should receive tgVal and args
    mapEB = tgVal.getMapEB()
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
    plotEB.makePlots()
    plotEB.printSummary()

    plotEEp = PlotManager(mapEEp,  "EEp", args, outdir=outdir)
    plotEEp.makePlots()
    plotEEp.printSummary()

    plotEEm = PlotManager(mapEEm, "EEm", args, outdir=outdir)
    plotEEm.makePlots()
    plotEEm.printSummary()

