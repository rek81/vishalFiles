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

class PHOTON:
	def __init__(self, V):
		self.V = V
		self.nM = 0
		self.Pho = []
		self.RECOV = TLorentzVector()
	def AddMatch(self, P):
		Ph = TLorentzVector()
		Ph.SetPtEtaPhiM(P.pt(), P.eta(), P.phi(), P.mass())
		if Ph.DeltaR(self.V) < 0.05:
			self.nM += 1
			self.Pho.append(P)
			self.RECOV = self.RECOV + Ph
			return True
		else: return False
class ETA:
	def __init__(self, V, D0V, D1V, ID):
		self.ID = ID
		self.V  = V
		self.D0V = D0V
		self.D1V = D1V
		self.DR = D0V.DeltaR(D1V)
		self.nM = 0
		self.Pho = []
		self.RECOV = TLorentzVector()
	def AddMatch(self, P):
		Ph = TLorentzVector()
		Ph.SetPtEtaPhiM(P.pt(), P.eta(), P.phi(), P.mass())
		if Ph.DeltaR(self.V) < 0.05:
			self.nM += 1
			self.Pho.append(P)
			self.RECOV = self.RECOV + Ph
			return True
		else: return False

def HardGet(e, L, H):
	e.getByLabel(L, H)
	if H.isValid() and len(H.product()) > 0: 
		return H.product()
	return False

parser = OptionParser()
parser.add_option('--file', metavar='F', type='string', action='store', 
		default = '/cms/xaastorage/MINIAOD/2016/GJets/HT_100to200',
		dest='dire',
		help='') ## Sets which files to run on
(options, args) = parser.parse_args()

files = glob.glob( options.dire + "/*4.root" )
print 'Getting these files : '
print files

events = Events (files)
GH = Handle("vector<reco::GenParticle>")
GL = ("prunedGenParticles", "")

PH = Handle("vector<pat::Photon>")
PL = ("slimmedPhotons", "", "PAT")

sigmaIetaIeta = TH1F("sigmaIetaIeta", ";#sigmaietaieta", 200, 0, 200)

EtaPT = TH1F("EtaPT", ";#eta p_{T} (GeV)", 100, 0, 200)
EtaRAD = TH1F("EtaRAD", ";#Delta R(#gamma , #gamma)", 50, 0., 0.1)

NRecoPho = TH1F("NRecoPho", ";# of RECO #gamma", 5, 0, 5)
NRecoPhoP = TH1F("NRecoPhoP", ";# of RECO #gamma", 5, 0, 5)

PhoRecoPhoPT = TH2F("PhoRecoPhoPT", ";#eta p_{T} (GeV); RECO #gamma p_{T} (GeV)", 100, 0, 200, 100, 0, 200)
PhoRecoPhoPT.SetStats(0)

PhoRecoPTFrac = TH1F("PhoRecoPTFrac", ";fraction of #eta p_{T} reconstructed", 50, 0, 5)
PhoRecoPTFrac.SetStats(0)

n = 0
np = 0
en = 0 
ETAS = []
PHOTONS = []
for event in events:
	en += 1
	nBs = 0
	X = TLorentzVector()
	GP = HardGet(event, GL, GH)
	Ph = HardGet(event, PL, PH)
	if Ph == False: continue
	print dir(Ph[0])
	etas = []
	photons = []
	for ig in GP:
		if math.fabs(ig.pdgId()) in [22] and ig.mother().pdgId() not in [221, 331, 441]:	
			G = TLorentzVector()
			G.SetPtEtaPhiM(ig.pt(), ig.eta(), ig.phi(), ig.mass())
			photons.append(PHOTON(G))
			np += 1
		if math.fabs(ig.pdgId()) in [221, 331, 441]:
			if ig.numberOfDaughters() == 2:
				D0 = ig.daughter(0)
				D1 = ig.daughter(1)
				if D0.pdgId() == 22 and D1.pdgId() == 22:
					G = TLorentzVector()
					G.SetPtEtaPhiM(ig.pt(), ig.eta(), ig.phi(), ig.mass())
					print str(n) + ", " + str(np)
					n += 1
					EtaPT.Fill(ig.pt())
					d0V = TLorentzVector()
					d1V = TLorentzVector()
					d0V.SetPtEtaPhiM(D0.pt(), D0.eta(), D0.phi(), D0.mass())
					d1V.SetPtEtaPhiM(D1.pt(), D1.eta(), D1.phi(), D1.mass())
					EtaRAD.Fill(d1V.DeltaR(d0V))
					etas.append(ETA(G, d0V, d1V, ig.pdgId()))
	for p in Ph:
		dir(p)
		for e in etas:
			e.AddMatch(p)
		for i in photons:
			i.AddMatch(p)
	if len(etas) > 0: ETAS.append(etas)
	if len(photons) > 0: PHOTONS.append(photons)

for J in PHOTONS:
	for j in J:
		NRecoPhoP.Fill(j.nM)
for E in ETAS:
	for e in E:
		NRecoPho.Fill(e.nM)
		for p in e.Pho:
			PhoRecoPhoPT.Fill(e.V.Pt(), e.RECOV.Pt())
			PhoRecoPTFrac.Fill(e.RECOV.Pt()/e.V.Pt())




F = TFile("EtasPhoPho.root", "recreate")
F.cd()
EtaPT.Write()
EtaRAD.Write()
NRecoPho.Write()
NRecoPhoP.Write()
PhoRecoPhoPT.Write()
PhoRecoPTFrac.Write()
F.Write()
F.Save()
F.Close
			
			








