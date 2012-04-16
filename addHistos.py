#!/bin/python

from ROOT import *
from array import *
import os.path

def addHistos( label, histname, Samples, color, verbose) :
    histos = []
    for iSample in Samples :
        ifile = iSample[0]
        xs = iSample[1]
        nevt = iSample[2]
        lumi = iSample[3]
        #print 'hist', histname
        hist = ifile.Get( histname ).Clone()
        if verbose:
            print 'file: {0:<20}, histo:{1:<20}, integral:{2:<5.3f}, nEntries:{3:<5.0f}, weight:{4:<2.3f}'.format(
                ifile.GetName(),    
                histname,
                hist.Integral(), hist.GetEntries(), xs * lumi /nevt
                )
        hist.Sumw2()    
        hist.Scale( xs * lumi /nevt)
        histos.append( hist )
    histo = histos[0]
    for ihisto in range(0, len(histos) ):
        #print len(histos)
        histo.Add( histos[ihisto] )              
        histo.SetName( label+histname )
        histo.SetTitle( label+histname )
        histo.SetFillColor( color)
    if verbose:    
        print 'newName: {0:<5}, newIntegral: {1:5.2f}'.format(label+histname, histo.Integral() )   
    return histo

def addHistosMulti( label, histname, Samples, color, verbose, binnedExpected, minTag, maxTag, minJet, maxJet) :
    print "====Begin plotting %s" % label
    verbose = False
    histos = []
    globalEventsStored = 0
    globalEventsExpected = 0
    globalPreIntegral = 0
    globalPostIntegral = 0
    for currTag in range( int(minTag), int(maxTag) + 1 ):
        for currJet in range( int(minJet), int(maxJet) + 1 ):
            if currTag > currJet:
                continue
            binKey = "%sj_%st" % (currJet, currTag)
            print "current bin %s" % binKey
            sampleCount        = 0
            samplePreIntegral  = 0
            samplePostIntegral = 0
            sampleHistos = []
            for iSample in Samples :
                ifile = iSample[0]
                xs = iSample[1]
                nevt = iSample[2]
                lumi = iSample[3]
                targetHistogram = "%s_%s" % (histname, binKey)
                if True:
                    print 'file: {0:<20}, histo:{1:<20}'.format(
                        ifile.GetName(),    
                        targetHistogram )
                hist = ifile.Get( targetHistogram ).Clone()
                if verbose:
                    print 'file: {0:<20}, histo:{1:<20}, integral:{2:<5.3f}, nEntries:{3:<5.0f}, weight:{4:<2.3f}'.format(
                        ifile.GetName(),    
                        histname,
                        hist.Integral(), hist.GetEntries(), xs * lumi /nevt
                        )
                hist.Sumw2()    
                #hist.Scale( hist.Integral() / binnedExpected[binKey] )
                sampleCount        += hist.GetEntries()
                samplePreIntegral  += hist.Integral()
                globalPreIntegral  += hist.Integral()
                histos.append( hist )
                sampleHistos.append( hist )
                if binnedExpected != None:
                    print "      {0:<7}: {1:<20}, EventsStored: {2:<7.0f} EventsReqd: {3:<7.0f}".format( binKey, os.path.basename(ifile.GetName()), hist.GetEntries(), binnedExpected[binKey] )
                else:
                    print "      {0:<7}: {1:<20}, EventsStored: {2:<7.0f}".format( binKey, os.path.basename(ifile.GetName()), hist.GetEntries())

            # END -- for iSample in Samples:
            # rescale all the samples in a jettag bin
            globalEventsStored += sampleCount
            if binnedExpected != None and sampleCount != 0 and samplePreIntegral != 0:
                globalEventsExpected += binnedExpected[binKey]
                
                for oneHist in sampleHistos:
                    preIntegral = oneHist.Integral()
                    oneHist.Scale( binnedExpected[binKey] / samplePreIntegral )
                    postIntegral = oneHist.Integral()
                    samplePostIntegral += postIntegral
                    globalPostIntegral += postIntegral
                    print "          Scaling %s - integral from %s to %s" % (os.path.basename(oneHist.GetName()), preIntegral, postIntegral)

                print "      {0:<20}: Scaled by {1:5.3f} ({2:5.3f}/{3:7.3f}) Integral: {4:6.3f} to {5:6.3f}".format( binKey, binnedExpected[binKey] / sampleCount, binnedExpected[binKey], sampleCount, samplePreIntegral, samplePostIntegral )
            else:
                print "      {0:<20}: Total Samples {1:7.3f}".format( binKey, sampleCount )


    # end forTag, forJet
    print "====END plotting %s - eventsStored %s - eventsRequested %s - Integral %s to %s" % (label, globalEventsStored, globalEventsExpected,globalPreIntegral, globalPostIntegral)
    histo = histos[0]
    histo.SetName( label+histname )
    histo.SetTitle( label+histname )
    histo.SetFillColor( color)
    for ihisto in range(1, len(histos) ):
        histo.Add( histos[ihisto] )              

    if verbose:    
        print 'newName: {0:<5}, newIntegral: {1:5.2f}'.format(label+histname, histo.Integral() ) 
    return histo
