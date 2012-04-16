#!/bin/python

from ROOT import *
from array import *

def weightHisto( label, histname, sample, color, verbose) :
    ifile = sample[0]
    xs    = sample[1]
    nevt  = sample[2]
    lumi  = sample[3]
    if len(sample) >= 5:
        eventsExpected = sample[4]
    hist  = ifile.Get( histname ).Clone()
    if verbose:
        print 'file: {0:<20}, histo:{1:<20}, integral:{2:<5.3f}, xs:{3:<5.2f}, lumi:{4:<5.2f}, nevt:{5:<5.2f}, weight:{6:<2.3f}'.format(
            ifile.GetName(),    
            histname,
            hist.Integral(), xs, lumi, nevt, xs * lumi /nevt
            )
    hist.Sumw2()

    # either scale according to the lumi, xsec, nevents or from the fitted value
    if len(sample) >= 5:
        hist.Scale( eventsExpected / hist.Integral() )
    else:
        hist.Scale( xs * lumi /nevt)

    hist.SetName( label+histname )
    hist.SetTitle( label+histname )
    if histname != 'Data_':
        hist.SetFillColor(color)
    if verbose:    
        print 'newName: {0:<5}, newIntegral: {1:5.2f}'.format(label+histname, hist.Integral() )  
    return hist

def weightHistoMulti( label, histname, sample, color, verbose, binnedExpected, minTag, maxTag, minJet, maxJet):
    totalEntries = 0
    histos = []
    for currTag in range( int(minTag), int(maxTag) + 1 ):
        for currJet in range( int(minJet), int(maxJet) + 1 ):
            binKey = "%sj_%st" % (currJet, currTag)

            ifile = sample[0]
            xs    = sample[1]
            nevt  = sample[2]
            lumi  = sample[3]
            hist  = ifile.Get( "%s_%s" % (histname, binKey) ).Clone()
            if verbose:
                print 'file: {0:<20}, histo:{1:<20}, integral:{2:<5.3f}, xs:{3:<5.2f}, lumi:{4:<5.2f}, nevt:{5:<5.2f}, weight:{6:<2.3f}'.format(
                    ifile.GetName(),    
                    ("%s_%s") % (histname, binKey),
                    hist.Integral(), xs, lumi, nevt, xs * lumi /nevt
                    )
            hist.Sumw2()
            
            # either scale according to the lumi, xsec, nevents or from the fitted value
            if binnedExpected != None:
                hist.Scale( binnedExpected[binKey] / hist.GetEntries() )
                totalEntries += binnedExpected[binKey]
            else:
                totalEntries += hist.GetEntries()
            histos.append( hist )

    histo = histos[0]
    for ihisto in range(1, len(histos) ):
        #print len(histos)
        histo.Add( histos[ihisto] )              
        histo.SetName( label+histname )
        histo.SetTitle( label+histname )
        if histname != 'Data_':
            histo.SetFillColor(color)

    if verbose:    
        print 'newName: {0:<5}, newIntegral: {1:5.2f}, newEntries: {1:f}'.format(label+histname, histo.Integral(), totalEntries )  
    return histo
