### Set of functions to analyse empirical distributions
import numpy as np



def sampleFromDist(yRange, cdf):
    ## For a given cdf inverts the CDF. 
    ## Currently returns a piecewise linear function in the following form
    ##
    ## yRange runs from yMin to yMax
    ## cdf must run from 0 to 1 and must be ordered 0 -> 1

    if len(yRange) != len(cdf):
        print('Error in sampleFromDist: range and cdf of incompatable lengths')
        return none
    
    value = np.random.uniform()
    i = next(p[0] for p in enumerate(cdf) if p[1] >value)-1
    if i < len(cdf):
        #linear interpolation
        s = yRange[i]+ ((value - cdf[i])/(cdf[i+1]-cdf[i])) * (yRange[i+1] - yRange[i])    #Standard linear interpolation between points
    elif cdf_i == len(cdf):
        s = yRange[i]
    
    return s
    
        
    
    