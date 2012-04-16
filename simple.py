#!/usr/bin/env python2.6
# ROOT is the worst worst worst worst worst
# At least the pyRoot stuff should try and behave nicely and not eat random arguments

import ROOT as ROOTMODULE
from ROOT import *
ROOTMODULE.PyConfig.IgnoreCommandLineOptions = True
gROOT.SetBatch()

from array import *
import json
#from sys import argv
#import sys
#import re
from addHistos import *
from weightHisto import *
from setTDRStyle import *
setTDRStyle()
#gROOT.Macro("~/rootlogon.C")
gStyle.SetTitleFillColor(10)
gStyle.SetTitleBorderSize(0)
gStyle.SetOptStat(000000)


# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--Lumi', metavar='D', type='float', action='store',
                  default=880.241, ##Single Ele
                  #default= 1292.65,##EleHad
                  #default=2172.891, ## Combine
                  dest='Lumi',
                  help='Data Luminosity')

parser.add_option('--globalSF', metavar='SF', type='float',
                  default=0.9485,
                  dest='globalSF',
                  help='Global lepton SF (%default default)')

parser.add_option('--rebin', metavar='T', type='int', action='store',
                  default=1,
                  dest='rebin',
                  help='rebin x axes to this')

parser.add_option('--outputDir', metavar='MTD', type='string',
                  default='../plots',
                  dest='outputDir',
                  help='Directory to store plots')

parser.add_option('--filePath', metavar='MTD', type='string',
                  default='../inputFiles/CombinedEle',
                  dest='filePath',
                  help='Path to the root histograms')

parser.add_option('--fileSuffix', metavar='MTD', type='string',
                  default='',
                  dest='fileSuffix',
                  help='arbitrarty text to place directly before the output extension')

parser.add_option('--var', metavar='MTD', type='string',
                  default='Top_secvtxMass',
                  dest='var',
                  help='variable of interest')

parser.add_option('--nBin', metavar='D', type='int', action='store',
                  default=40,
                  dest='nBin',
                  help='Number of x-axis bin to display')

parser.add_option('--verbose',action='store_true',
                  default=True,
                  dest='verbose',
                  help='verbose switch')

parser.add_option('--useFitter',action='store_true',
                  default=True,
                  dest='useFitter',
                  help='Use results from fitter?')

parser.add_option('--fitJSON', action='store',
                  dest='fitJSON',
                  help="Location to read fit values from" )

parser.add_option('--minJets', metavar='D', type='int', action='store',
                  default=3,
                  dest='minJets',
                  help='Minimum number of jets for plots')
parser.add_option('--maxJets', metavar='D', type='int', action='store',
                  default=5,
                  dest='maxJets',
                  help='Minimum number of jets for plots')
parser.add_option('--minTags', metavar='D', type='int', action='store',
                  default=1,
                  dest='minTags',
                  help='Minimum number of tags for plots')
parser.add_option('--maxTags', metavar='D', type='int', action='store',
                  default=2,
                  dest='maxTags',
                  help='Minimum number of tags for plots')

parser.add_option('--PVSelector', type="string", action="store",
                  default="nominal",
                  dest="pvSelector",
                  help="Selects between (nominal/PVup/PVdown)")

parser.add_option('--useLooseQCD', action='store_true',
                 default=False,
                 dest = 'useLooseQCD', help="Should we use a loose QCD shape for plotting?")

parser.add_option('--inputMCFilenameSuffix', action='store',
                  default='_ttbsm_v9_nominal.root',
                  dest='inputMCFilenameSuffix',
                  help='Suffix for our input filenames (Not MC or Data)' )

parser.add_option('--inputFilenameSuffix', action='store',
                  default='_ttbsm_v9_nominal.root',
                  dest='inputFilenameSuffix',
                  help='Suffix for our input filenames (QCD and Data)' )


(options,args) = parser.parse_args()

# ==========end: options =============
   
Path          = options.filePath
outputDir     = options.outputDir
var           = options.var
verbose       = options.verbose
useFitter     = options.useFitter
fileSuffix    = options.fileSuffix
useLooseQCD   = options.useLooseQCD
inputFilenameSuffix = options.inputFilenameSuffix
inputMCFilenameSuffix = options.inputMCFilenameSuffix
lum           = '{0:1.0f}'.format( options.Lumi)
minJet = '{0:1.0f}'.format( options.minJets)
maxJet = '{0:1.0f}'.format( options.maxJets)
minTag = '{0:1.0f}'.format( options.minTags)
maxTag = '{0:1.0f}'.format( options.maxTags)


f_data        = TFile(Path+'/SingleElectron%s' % inputFilenameSuffix)
#f_data        = TFile(Path+'/ElectronHad%s' % inputFilenameSuffix)
#f_data        = TFile(Path+'/CombinedElectron%s' % inputFilenameSuffix)
f_ttbar       = TFile(Path+'/TTJets_TuneZ2_7TeV-madgraph-tauola%s' % inputMCFilenameSuffix)
f_wjets       = TFile(Path+'/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola%s' % inputMCFilenameSuffix)
f_zjets       = TFile(Path+'/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola%s' % inputMCFilenameSuffix)
f_sToptW      = TFile(Path+'/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola%s' % inputMCFilenameSuffix)
f_sTopt       = TFile(Path+'/T_TuneZ2_t-channel_7TeV-powheg-tauola%s' % inputMCFilenameSuffix)
f_sTops       = TFile(Path+'/T_TuneZ2_s-channel_7TeV-powheg-tauola%s' % inputMCFilenameSuffix)
f_sTopbartW   = TFile(Path+'/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola%s' % inputMCFilenameSuffix)
f_sTopbart    = TFile(Path+'/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola%s' % inputMCFilenameSuffix)
f_sTopbars    = TFile(Path+'/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola%s' % inputMCFilenameSuffix)
f_emen2030    = TFile(Path+'/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6%s' % inputFilenameSuffix)
f_emen3080    = TFile(Path+'/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia%s' % inputFilenameSuffix)
f_emen80170   = TFile(Path+'/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6%s' % inputFilenameSuffix)
f_bc2e2030    = TFile(Path+'/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6%s' % inputFilenameSuffix)
f_bc2e3080    = TFile(Path+'/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6%s' % inputFilenameSuffix)
f_bc2e80170   = TFile(Path+'/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia%s' % inputFilenameSuffix)
f_gjet40100   = TFile(Path+'/GJets_TuneZ2_40_HT_100_7TeV-madgraph%s' % inputFilenameSuffix)
f_gjet100200  = TFile(Path+'/GJets_TuneZ2_100_HT_200_7TeV-madgraph%s' % inputFilenameSuffix)
f_gjet200Inf  = TFile(Path+'/GJets_TuneZ2_200_HT_inf_7TeV-madgraph%s' % inputFilenameSuffix)

##to get the shape of QCD
f_emen2030_l    = TFile(Path+'/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_v9_Loose.root')
f_emen3080_l    = TFile(Path+'/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia_ttbsm_v9_Loose.root')
f_emen80170_l   = TFile(Path+'/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_v9_Loose.root')
f_bc2e2030_l    = TFile(Path+'/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_v9_Loose.root')
f_bc2e3080_l    = TFile(Path+'/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_v9_Loose.root')
f_bc2e80170_l   = TFile(Path+'/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia_ttbsm_v9_Loose.root')
f_gjet40100_l   = TFile(Path+'/GJets_TuneZ2_40_HT_100_7TeV-madgraph_ttbsm_v9_Loose.root')
f_gjet100200_l  = TFile(Path+'/GJets_TuneZ2_100_HT_200_7TeV-madgraph_ttbsm_v9_Loose.root')
f_gjet200Inf_l  = TFile(Path+'/GJets_TuneZ2_200_HT_inf_7TeV-madgraph_ttbsm_v9_Loose.root')

#==== Assumed luminosity (pb-1)=====
lumi = options.Lumi
gSF = options.globalSF


#===== cross sections (pb)==========
Top_xs            = 157.5    *gSF
WJets_xs          = 31314.0  *gSF 
ZJets_xs          = 3048.0   *gSF
SingleToptW_xs    = 7.87     *gSF
SingleTopT_xs     = 41.92    *gSF
SingleTopS_xs     = 3.19     *gSF
SingleTopbartW_xs = 7.87     *gSF
SingleTopbarT_xs  = 22.65    *gSF
SingleTopbarS_xs  = 1.44     *gSF
GJets40100_xs     = 25690.0  *gSF
GJets100200_xs    = 5213.0   *gSF
GJets200Inf_xs    = 798.3    *gSF
BCtoE2030_xs      = 139299.0 *gSF
BCtoE3080_xs      = 143844.8 *gSF
BCtoE80170_xs     = 9431.1   *gSF
EMEn2030_xs       = 2502660.0*gSF
EMEn3080_xs       = 3625840.0*gSF
EMEn80170_xs      = 142813.8 *gSF

#===== Number of generated events ======
top_num            = 3701947
wjets_num          = 77105816
zjets_num          = 36277961
singleTopT_num     = 3900171
singleTopS_num     = 259971
singleToptW_num    = 814390
singleTopbarT_num  = 1944826
singleTopbarS_num  = 137980
singleTopbartW_num = 809984
GJets40100_num     = 12730972
GJets100200_num    = 1536287
GJets200Inf_num    = 9377170
BCtoE2030_num      = 2081560
BCtoE3080_num      = 2030033
BCtoE80170_num     = 1082691
EMEn2030_num       = 35729669
EMEn3080_num       = 70392060
EMEn80170_num      = 8150672

# ====variables of interest======
names = [
    var,
    ]

# === prepare the inputs ===========
dataLabel     = 'Data_'
topLabel      = 'Top_'
wjetsLabel    = 'Wjets_'
zjetsLabel    = 'Zjets_'
sTopLabel     = 'STop_'
qcdLabel      = 'QCD_'
qcdLabelLoose = 'QCD_Loose_'

allHists     = []

dataSample   = [[f_data,      1.0 ,         1.0,         1.0 ]]
topSample    = [[f_ttbar,     Top_xs,       top_num,     lumi]]
wjetSample   = [[f_wjets,     WJets_xs,     wjets_num,     lumi]]
zjetSample   = [[f_zjets,     ZJets_xs,     zjets_num,     lumi]]

singleTopSamples = [
    [f_sToptW,      SingleToptW_xs,      singleToptW_num,    lumi],
    [f_sTopt,       SingleTopT_xs,       singleTopT_num,     lumi],
    [f_sTops,       SingleTopS_xs,       singleTopS_num,     lumi],
    [f_sTopbartW,   SingleTopbartW_xs,   singleTopbartW_num, lumi],
    [f_sTopbart,    SingleTopbarT_xs,    singleTopbarT_num,  lumi],
    [f_sTopbars,    SingleTopbarS_xs,    singleTopbarS_num,  lumi],
    ]

qcdSamples = [
    [f_emen2030,   EMEn2030_xs,    EMEn2030_num,   lumi],
    [f_emen3080,   EMEn3080_xs,    EMEn3080_num,   lumi],
    [f_emen80170,  EMEn80170_xs,   EMEn80170_num,  lumi],
    [f_bc2e2030,   BCtoE2030_xs,   BCtoE2030_num,  lumi],
    [f_bc2e3080,   BCtoE3080_xs,   BCtoE3080_num,  lumi],
    [f_bc2e80170,  BCtoE80170_xs,  BCtoE80170_num, lumi],
    [f_gjet40100,  GJets40100_xs,  GJets40100_num, lumi],
    [f_gjet100200, GJets100200_xs, GJets100200_num,lumi],
    [f_gjet200Inf, GJets200Inf_xs, GJets200Inf_num,lumi],
    ]
qcdSamplesLoose = [
    [f_gjet200Inf_l, GJets200Inf_xs, GJets200Inf_num,lumi],
    [f_gjet40100_l,  GJets40100_xs,  GJets40100_num, lumi],
    [f_gjet100200_l, GJets100200_xs, GJets100200_num,lumi],
    [f_emen2030_l,   EMEn2030_xs,    EMEn2030_num,   lumi],
    [f_emen3080_l,   EMEn3080_xs,    EMEn3080_num,   lumi],
    [f_emen80170_l,  EMEn80170_xs,   EMEn80170_num,  lumi],
    [f_bc2e2030_l,   BCtoE2030_xs,   BCtoE2030_num,  lumi],
    [f_bc2e3080_l,   BCtoE3080_xs,   BCtoE3080_num,  lumi],
    [f_bc2e80170_l,  BCtoE80170_xs,  BCtoE80170_num, lumi],
    ]

#======= add scaling due to fit expectations =======
#     &       Data  & Total Fit  &        Top  &  SingleTop  &        Wbx  &        Wcx  &        Wqq  &      ZJets  &        QCD  \\
#               \hline           DATA   TOTALFIT    TOP      STOP      WBX      WCX       WQQ   ZJETS    QCD

#               &       Data  & Total Pred  &        Top  &  SingleTop  &        Wbx  &        Wcx  &        Wqq  &      ZJets  &        QCD  \\
#\hline             DATA     TOTAL       TOP        STOP     WBX          WCX       WQQ       ZJETS     QCD
#1 Jet  1 Tag   & 10487   & 10443.6   &  276.2   & 706.8   & 1023.2   & 6321.7   & 1050.3   & 320.5   & 744.8  
#2 Jets 1 Tag   &  5869   &  5932.7   & 1054.6   & 750.0   & 1348.4   & 2047.8   &  415.0   & 242.9   &  74.0  
#3 Jets 1 Tag   &  4959   &  4977.2   & 2618.1   & 457.0   &  613.6   &  693.8   &  177.2   & 136.0   & 281.5  
#4 Jets 1 Tag   &  1825   &  1770.7   & 1214.7   & 114.0   &  160.1   &  142.3   &   45.0   &  32.5   &  62.1  
#5 Jets 1 Tag   &   622   &   630.0   &  509.3   &  28.7   &   42.5   &   43.0   &    7.8   &   8.7   &  -9.9  
#2 Jets 2 Tags  &   638   &   639.7   &  299.2   & 127.7   &  141.6   &   49.1   &    3.4   &  13.8   &   4.9  
#3 Jets 2 Tags  &  1835   &  1855.0   & 1427.6   & 175.7   &  155.3   &   36.3   &    4.3   &  16.2   &  39.6  
#4 Jets 2 Tags  &  1046   &  1022.7   &  888.7   &  63.5   &   46.4   &    9.0   &    1.2   &   4.5   &   9.2  
#5 Jets 2 Tags  &   469   &   468.3   &  434.0   &  18.1   &   23.6   &    0.5   &    0.7   &   2.0   & -10.7  
########################################NOT THE ONE BELOW
#               1 Jet  1 Tag   & 25506 & 25475.4 &  600.5 & 1702.1 &  830.0 & 16409.9 & 3254.8 & 653.0 & 2025.1   \\
#               2 Jets 1 Tag   & 15227 & 15298.8 & 2676.7 & 1919.1 & 1400.9 &  6450.2 & 1582.9 & 419.1 &  849.8   \\
#               3 Jets 1 Tag   &  8683 &  8607.1 & 4444.5 &  919.7 &  568.2 &  1799.4 &  492.6 & 168.6 &  214.2   \\
#               4 Jets 1 Tag   &  4500 &  4491.3 & 3263.0 &  296.7 &  152.1 &   413.0 &  132.1 &  48.9 &  185.6   \\
#               5 Jets 1 Tag   &  2155 &  2175.6 & 1823.0 &   96.8 &   43.3 &   115.9 &   28.4 &  18.8 &   49.4   \\
#               2 Jets 2 Tags  &  1411 &  1453.8 &  773.5 &  323.7 &  186.8 &   129.5 &   20.9 &  19.5 &    0.0   \\
#               3 Jets 2 Tags  &  2844 &  2797.1 & 2288.9 &  309.9 &  115.9 &    61.9 &    4.8 &  15.7 &    0.0   \\
#               4 Jets 2 Tags  &  2516 &  2523.3 & 2305.6 &  140.9 &   38.5 &    29.6 &    3.4 &   5.4 &    0.0   \\
#               5 Jets 2 Tags  &  1606 &  1615.1 & 1531.2 &   59.3 &   14.1 &     7.1 &    0.3 &   3.1 &    0.0   \\

if useFitter:
    fitInfo = json.load( open( options.fitJSON, 'r') )
    QCD_total = fitInfo['QCD_total']
    Top_total = fitInfo['Top_total']
    SingleTop_total = fitInfo['SingleTop_total']
    WJet_total = fitInfo['WJet_total']
    ZJet_total = fitInfo['ZJet_total']





#QCD_total = {'5j_2t' : -10.7,'2j_2t' : 4.9,'4j_2t' : 9.2,'3j_2t' : 39.6,'5j_1t' : -9.9,'4j_1t' : 62.1,'1j_1t' : 744.8,'3j_1t' : 281.5,'2j_1t' : 74.0}
#Top_total = {'5j_2t' : 434.0,'2j_2t' : 299.2,'4j_2t' : 888.7,'3j_2t' : 1427.6,'5j_1t' : 509.3,'4j_1t' : 1214.7,'1j_1t' : 276.2,'3j_1t' : 2618.1,'2j_1t' : 1054.6}
#SingleTop_total = {'5j_2t' : 18.1,'2j_2t' : 127.7,'4j_2t' : 63.5,'3j_2t' : 175.7,'5j_1t' : 28.7,'4j_1t' : 114.0,'1j_1t' : 706.8,'3j_1t' : 457.0,'2j_1t' : 750.0}
#WJet_total = {'5j_2t' : 24.8,'2j_2t' : 194.1,'4j_2t' : 56.6,'3j_2t' : 195.9,'5j_1t' : 93.3,'4j_1t' : 347.4,'1j_1t' : 8395.2,'3j_1t' : 1484.6,'2j_1t' : 3811.2}
#ZJet_total = {'5j_2t' : 2.0,'2j_2t' : 13.8,'4j_2t' : 4.5,'3j_2t' : 16.2,'5j_1t' : 8.7,'4j_1t' : 32.5,'1j_1t' : 320.5,'3j_1t' : 136.0,'2j_1t' : 242.9}
# FIXME fix this to make it configurable
leptonName = "Electron"
if var == 'nJets':
    xtitle = "number of jets"
elif var.find('Top_MET') != -1:
    xtitle = "MET"
elif var.find('Top_secvtxMass') != -1:
    xtitle = "svm"
elif var.find('Top_lepPt') != -1:
    xtitle = "%s Pt(GeV)" % leptonName
elif var.find('Top_centrality') != -1:
    xtitle = "Centrality"
elif var.find('Top_sumEt') != -1:
    xtitle = "Sum Eta"
elif var.find('Top_wMT') != -1:
    xtitle = "w Mt (GeV)"
elif var.find('Top_hT') != -1:
    xtitle = "hT"
elif var == 'nTags':
   xtitle = "number of b-tag jets"   
elif var == 'm3':
    xtitle = "M3"
elif var == 'elePt':
    xtitle = "electron Pt(GeV)"    
elif var == 'ptJet0':
    xtitle = "leading jet pt (GeV)"
elif var == 'ptJet1':
    xtitle = "second leading jet pt (GeV)"
elif var == 'ptJet2':
   xtitle = "third leading jet pt (GeV)"
elif var == 'ptJet3':
    xtitle = "fourth leading jet pt (GeV)"
elif var == 'ptEle' :
     xtitle = "electron pt (GeV)"
elif var == 'm3j1t':
    xtitle = "M3, #geq 3j, #geq 1t"
elif var == 'wMT3j1t':
    xtitle = "M_{T}^{W}(Gev), #geq 3j, #geq 1t"    
elif var == 'eleEta3j1t':
    xtitle = "electron |#eta|, #geq 3j, #geq 1t"
elif var == 'elePt3j1t':
    xtitle = "electron Pt(GeV), #geq 3j, #geq 1t"     
elif var == 'met3j1t':
    xtitle = "MET (GeV), #geq 3j, #geq 1t"    
elif var == 'hT3j1t':
    xtitle = "H_{T}, #geq 3j, #geq 1t"    
elif var == 'nVertices3j1t':
    xtitle = "Number of Primary vertices, #geq 3j, #geq 1t"
elif var == 'Top_nPV':
    xtitle = "Number of Primary vertices"
elif  var == 'nJets3':
   xtitle = "number of jets"     
else:
    xtitle = ""
 

#======= add the qcd and singleTop histos and apply weights to all ============
for ivar in range(0, len(names)) :
    name = names[ivar]
    if not useFitter:
        hist_data  = weightHisto( dataLabel,   name, dataSample,    kBlack, verbose)
        hist_top   = weightHisto( topLabel,    name, topSample,     206,    verbose)
        hist_wjets = weightHisto( wjetsLabel,  name, wjetSample,    210,    verbose)
        hist_zjets = weightHisto( zjetsLabel,  name, zjetSample,    215,    verbose)   
        hist_sTop  = addHistos( sTopLabel,     name, singleTopSamples,95,     verbose)
        hist_qcd   = addHistos( qcdLabel,      name, qcdSamples,      220,    verbose)
        if useLooseQCD:
            hist_qcdL  = addHistos( qcdLabelLoose, name, qcdSamplesLoose,      220,    verbose)
        
        if useLooseQCD and hist_qcdL.Integral()!= 0:
            hist_qcdL.Scale(hist_qcd.Integral()/hist_qcdL.Integral())
            
    else:
        hist_data  = addHistosMulti( dataLabel,   name, dataSample,    kBlack, verbose, None, minTag, maxTag, minJet, maxJet)
        hist_top   = addHistosMulti( topLabel,    name, topSample,     206,    verbose, Top_total, minTag, maxTag, minJet, maxJet)
        hist_wjets = addHistosMulti( wjetsLabel,  name, wjetSample,    210,    verbose, WJet_total, minTag, maxTag, minJet, maxJet)
        hist_zjets = addHistosMulti( zjetsLabel,  name, zjetSample,    215,    verbose, ZJet_total, minTag, maxTag, minJet, maxJet)
        hist_sTop  = addHistosMulti( sTopLabel,     name, singleTopSamples,95,     verbose, SingleTop_total, minTag, maxTag, minJet, maxJet)
        hist_qcd   = addHistosMulti( qcdLabel,      name, qcdSamples,      220,    verbose, QCD_total, minTag, maxTag, minJet, maxJet)
        if useLooseQCD:
            hist_qcdL  = addHistosMulti( qcdLabelLoose, name, qcdSamplesLoose,      220,    verbose, QCD_total, minTag, maxTag, minJet, maxJet)
        
    
    allHists.append(hist_data)
    if useLooseQCD:
        allHists.append(hist_qcdL)
    else:
        allHists.append(hist_qcd)
    allHists.append(hist_sTop)
    allHists.append(hist_zjets)
    allHists.append(hist_wjets)
    allHists.append(hist_top)
    
# ============= PRINT ==================
for ihist in range(0, len(allHists)):
    print "  ", allHists[ihist].GetName(),"     %5.2f" % allHists[ihist].Integral(),"      nEntries= %5.0f" % allHists[ihist].GetEntries()
    
# ============= PLOT ==================
stackEvents = 0
hs = THStack("nEvents","nEvents")
allHists[0].Rebin(options.rebin)
allHists[0].Print()
for ihist in allHists[1:]:
    ihist.Rebin(options.rebin)
    hs.Add(ihist)
    ihist.Print()
    
      
    
# draw
if allHists[0].GetMaximum() > hs.GetMaximum() :
    print "Setting maximum!"
    hs.SetMaximum(allHists[0].GetMaximum())

c1 = TCanvas('c1', 'c1')
allHists[0].SetMarkerStyle(8)
allHists[0].error = "e"
hs.Draw("HIST")
allHists[0].Draw("esame")

xs = hs.GetXaxis()
xs.SetTitle(xtitle)
#xs.SetRangeUser(0.,options.nBin)
#xs.SetRangeUser(0.,200)
gPad.RedrawAxis()

#legend		
leg = TLegend(0.65,0.8,0.99,0.95)
leg.AddEntry(allHists[0],"Data ("+lum+" fb^{-1})","pl")
leg.AddEntry(allHists[5],"t #bar{t}","f")
leg.AddEntry(allHists[4],"W+jets","f")
leg.AddEntry(allHists[3],"Z+jets","f")
leg.AddEntry(allHists[2],"SingleTop","f")
leg.AddEntry(allHists[1],"QCD","f")

Ysize = max(4, len(allHists))
leg.SetY1(1-0.05*Ysize)
leg.SetBorderSize(1)
leg.SetFillColor(10)
leg.Draw()

c1.SetLogy(1)
baseName = options.outputDir+"/"+options.var+"_"+lum+fileSuffix
c1.SaveAs(baseName + "_log.gif")
c1.SaveAs(baseName + "_log.eps")
gROOT.ProcessLine(".!epstopdf " + baseName + "_log.eps")

c1.SetLogy(0)
c1.SaveAs(baseName + ".gif")
c1.SaveAs(baseName + ".eps")
gROOT.ProcessLine(".!epstopdf " + baseName + ".eps")

print "bin      zjet  wjet  stop  ttop  qcd"
for k in sorted(ZJet_total.keys()):
    print "%s %s %s %s %s %s" % (k, ZJet_total[k], WJet_total[k], SingleTop_total[k], Top_total[k], QCD_total[k] )
