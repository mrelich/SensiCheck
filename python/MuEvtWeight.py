
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# Simple tool to hack the event weight for this quick #
# sensitivity study. Will only have muons for now but #
# will add electrons later.                           #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

import pickle
from math import log10, pi
import Constants as C
import numpy as np

class MuEvtWeightTool:

    # Constructor
    def __init__(self, f_mu_path):
        self.loadMu(f_mu_path)

    # Get Muon event Weight
    def getMuW(self, E_nu, OneWeight, fnorm, addinc=False, inclevel=1):
        
        Aeff = self.getMuEffArea(E_nu) * 1e4 # m^2 --> cm^2
        flux = C.astronorm / (fnorm * pow(E_nu,1))
        
        # Add a scale factor if we want to see impact of increasing
        # in the PeV region.
        sf = self.getSF(E_nu, addinc, inclevel)

        # Calculate weight
        w = flux * AEff * 4 * pi * C.livetime * sf
        
        # Fudge factor -- the shape seems to be right, but the normalization
        # is off.. I don't know where this is coming from yet, but add the ad-hoc
        # factor to get things to match reasonably well now.
        w *= 10

        # Return the weight
        return w

    # Get Effective Area 
    def getMuEffArea(self, E_nu):
        logE = log10(E_nu)
        for i in range(len(self.mubins)):
            if self.mubins[i] <= logE and logE <= self.mubins[i+1]:
                return self.mueffa[i]
        return 0.


    def getSF(self, E_nu, addinc,incfactor):
        if not addinc: return 1.
        logE = log10(E_nu)
        if 6 <= logE:
            return incfactor
        else:
            return 1

    # Load Muon Data
    def loadMu(self, pathToFile):
        mudata = pickle.load(open(pathToFile,'r'))
        self.mubins = mudata['logebins']
        self.mueffa = mudata['effa']
        self.mudE = self.mubins[1] - self.mubins[0]

