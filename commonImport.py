#!/usr/bin/env python3 

import re
import os, os.path
import logging
import argparse
import shutil

## safe batch mode 
import sys
args = sys.argv[:]
sys.argv = ['-b']
import ROOT
sys.argv = args
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from copy import *

sys.path.append(os.getcwd() + "/plotUtils/")
from utility import *
