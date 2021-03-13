#!/usr/bin/env python3
 
from commonImport import *
from tagClasses import TagManager

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
    if outdir and not os.path.exists(outdir):
        logging.info(f"Creating output folder {outdir}")
        os.makedirs(outdir)
        htmlpath = "./plotUtils/index.php"
        shutil.copy(htmlpath, outdir)

    tgVal = TagManager(args)

    mapEB = tgVal.getMapEB()
    mapEEp = tgVal.getMapEEp()
    mapEEm = tgVal.getMapEEp()
    if args.setSpecial:        
        oldval = args.setSpecial[0]
        newval = args.setSpecial[1]
        logging.info(f"setting map values from {oldval} to {newval}")
        updateMapValue(mapEB, oldval, newval)
        updateMapValue(mapEEp, oldval, newval)
        updateMapValue(mapEEm, oldval, newval)

    adjustSettings_CMS_lumi() # just a dummy function to fix some settings in canvas later on
    xsizeCanvas_EB = int(1200)
    ysizeCanvas_EB = int(xsizeCanvas_EB * 171. / 360. + 0.1 * xsizeCanvas_EB)
    cEB = ROOT.TCanvas("cEB", "", xsizeCanvas_EB, ysizeCanvas_EB) 
    xsizeCanvas_EE = int(900)
    ysizeCanvas_EE = int(800)
    cEE = ROOT.TCanvas("cEE", "", xsizeCanvas_EE, ysizeCanvas_EE) 

    cEB.cd()
    minz,maxz = getMinMaxHisto(mapEB, excludeEmpty=True, sumError=False, excludeVal=args.setSpecial[1] if args.setSpecial else None)
    drawTH2(mapEB, "iphi", "ieta", "value in tag::%s,%s" % (minz,maxz),
            canvasName="mapEB", outdir=outdir,
            leftMargin=0.08, rightMargin=0.16,
            nContours=101, palette=args.palette, passCanvas=cEB, drawOption="COLZ0")

    cEE.cd()
    minz,maxz = getMinMaxHisto(mapEEp, excludeEmpty=True, sumError=False, excludeVal=args.setSpecial[1] if args.setSpecial else None)
    drawTH2(mapEEp, "iX", "iY", "value in tag::%s,%s" % (minz,maxz),
            canvasName="mapEEp", outdir=outdir,
            leftMargin=0.12, rightMargin=0.18,
            nContours=101, palette=args.palette, passCanvas=cEE, drawOption="COLZ0")
    minz,maxz = getMinMaxHisto(mapEEm, excludeEmpty=True, sumError=False, excludeVal=args.setSpecial[1] if args.setSpecial else None)
    drawTH2(mapEEm, "iX", "iY", "value in tag::%s,%s" % (minz,maxz),
            canvasName="mapEEm", outdir=outdir,
            leftMargin=0.12, rightMargin=0.18,
            nContours=101, palette=args.palette, passCanvas=cEE, drawOption="COLZ0")
