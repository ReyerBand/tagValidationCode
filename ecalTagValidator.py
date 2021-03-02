
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
