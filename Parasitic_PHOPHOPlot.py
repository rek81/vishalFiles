#
import os
import array
from array import *
import glob
import math
import ROOT
from ROOT import *
import sys
import itertools
from itertools import *
from DataFormats.FWLite import *
from HLTrigger import *
from optparse import OptionParser

L = TLine(0.025,0.,0.025,0.15)
L.SetLineColor(kRed)

L2 = TLine(0,0,200,200)
L2.SetLineColor(kRed)


F = TFile("EtasPhoPho.root")
F.cd()
PP = F.Get("PhoRecoPhoPT")
Frac = F.Get("PhoRecoPTFrac")
Frac.Scale(1/Frac.Integral())
N = F.Get("NRecoPho")
N.Scale(1/N.Integral())
Np = F.Get("NRecoPhoP")
Np.Scale(1/Np.Integral())
Np.SetLineColor(kRed)
A = F.Get("EtaRAD")
A.Scale(1/A.Integral())
P = F.Get("EtaPT")
P.Scale(1/P.Integral())
P.GetYaxis().SetRangeUser(0.,0.075)
A.GetYaxis().SetRangeUser(0.,0.15)
C = TCanvas("C", "",1203, 803)
C.Divide(2,2)
C.cd(1)
P.Draw("e")
C.cd(2)
A.Draw("e")
L.Draw("same")
C.cd(3)
N.Draw("e")
Np.Draw("histsame")
C.cd(4)
PP.Draw("colz")
L2.Draw("same")

C2 = TCanvas("C2", "", 500, 500)
C2.cd()
Frac.Draw("e")
