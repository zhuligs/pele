import numpy as np
from numpy import log, exp



def logSum1(a, b):
    """
    return log( exp(a) + exp(b) )
    """
    if a > b:
        return a + log(1.0 + exp(-a + b) )
    else:
        return b + log(1.0 + exp(a - b) )


def logSum(log_terms):
    """
    Compute the log of a sum of terms whose logarithms are provided.

    REQUIRED ARGUMENTS  
      log_terms is the array (possibly multidimensional) containing the logs of the terms to be summed.

    RETURN VALUES
      log_sum is the log of the sum of the terms.
    """
    log_sum = log_terms[0] 
    for lt in log_terms[1:]:
        if log_sum > lt:
            log_sum = log_sum + log(1.0 + exp(-log_sum + lt) )
        else:
            log_sum = lt + log(1.0 + exp(log_sum - lt) )
    # return the log sum
    return log_sum



def calc_Cv(logn_E, visits1d, binenergy, NDOF, Treplica, k_B, TRANGE=None, NTEMP=100):
    
    #put some variables in this namespace
    nrep, nebins = np.shape(visits1d)
    print "nreps, nebins", nrep, nebins

    nz = np.where( visits1d.sum(0) != 0)[0]

    #find the ocupied bin with the minimum energy
    EREF = np.min(binenergy[nz])

    #now calculate partition functions, energy expectation values, and Cv
    if TRANGE == None:
        #NTEMP = 100 # number of temperatures to calculate expectation values
        TMAX = Treplica[-1]
        TMIN = Treplica[0]
        TINT=(TMAX-TMIN)/(NTEMP-1)
        TRANGE = [ TMIN + i*TINT for i in range(NTEMP) ]

    dataout = np.zeros( [NTEMP, 6] )
    for count,T in enumerate(TRANGE):
        kBT = k_B*T
        #find expoffset so the exponentials don't blow up
        dummy = logn_E[nz] - (binenergy[nz] - EREF)/kBT
        expoffset = np.max(dummy)
        dummy = np.exp(dummy)
        Z0 = np.sum(dummy)
        Z1 = np.sum( dummy *  (binenergy[nz] - EREF) )
        Z2 = np.sum( dummy *  (binenergy[nz] - EREF)**2 )

        

        if i == nebins-1:
            dE = binenergy[i]-binenergy[i-1]
        else:
            dE = binenergy[i+1]-binenergy[i]
            
        if dE/kBT < 1.0E-7:
            ONEMEXP=-dE/kBT
        else:
            ONEMEXP= 1.0-np.exp(dE/kBT)

        Eavg = NDOF*kBT/2.0 + 1.0*(kBT + dE/ONEMEXP) + Z1/Z0 + EREF
        
        Cv = NDOF/2. + 1.0*(1.0 - dE**2 * np.exp(dE/kBT)/(ONEMEXP**2*kBT**2)) - (Z1/(Z0*kBT))**2 + Z2/(Z0*kBT**2)
        
        dataout[count,0] = T
        dataout[count,1] = np.log(Z0)+expoffset
        dataout[count,2] = np.log(Z1)+expoffset
        dataout[count,3] = np.log(Z2)+expoffset
        dataout[count,4] = Eavg
        dataout[count,5] = Cv

        
        #np.array([kBT, Z0*np.exp(expoffset), Z1*np.exp(expoffset), Z2*np.exp(expoffset), Eavg, Cv, np.log(Z0)+expoffset, np.log(Z1)+expoffset, np.log(Z2)+expoffset]).tofile(fout," ")
        
        #fout.write("\n")

    return dataout
