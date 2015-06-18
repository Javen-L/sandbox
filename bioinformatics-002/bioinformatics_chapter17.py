# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 20:11:54 2015

@author: ngaude
"""

import numpy as np

amino_acid_mass = {'G' : 57, 'A' : 71, 'S' : 87, 'P' : 97, 'V' : 99, 'T' : 101, 'C' : 103,
    'I' : 113, 'L' : 113, 'N' : 114, 'D' : 115, 'K' : 128, 'Q' : 128, 'E' : 129,'M' : 131,
    'H' : 137, 'F' : 147, 'R' : 156, 'Y' : 163, 'W' : 186}
    
toy_mass = {'X':4, 'Z':5}

def spectrum_graph(spectrum, ref_mass = amino_acid_mass):
    """
    CODE CHALLENGE: Construct the graph of a spectrum.
    Given: A space-delimited list of integers Spectrum.
    Return: Graph(Spectrum).
    """
    spectrum.append(0)
    spectrum.sort()
    raa = {v:k for k,v in ref_mass.iteritems()}
    aav = ref_mass.values()
    aamax = max(aav)
    adj = []
    for i,si in enumerate(spectrum):
        for j,sj in enumerate(spectrum[i+1:]):
            if sj-si > aamax:
                break
            if (sj-si) in raa:
                adj.append((si,sj,raa[sj-si]))
    return adj

def ideal_spectrum(peptide, ref_mass = amino_acid_mass):
    """
    return an ideal spectrum from peptide
    """
    li = [ ref_mass[aa] for aa in peptide]
    n = len(li)
    spectrum = []
    for i in range(0,n+1):
            spectrum.append(sum(li[0:i]))
            spectrum.append(sum(li[i:]))
    return spectrum


def spectrum_decoding(spectrum, ref_mass = amino_acid_mass):
    """
    CODE CHALLENGE: Solve the Decoding an Ideal Spectrum Problem.
    Given: A space-delimited list of integers Spectrum.
    Return: An amino acid string that explains Spectrum.
    """
    adj = spectrum_graph(spectrum, ref_mass)
    g = {}
    for a,b,c in adj:
        g.setdefault(a,[]).append((b,c))
    source = 0
    sink = max(spectrum)
    paths = [[(source,''),],]
    while len(paths)>0:
        npaths= []
        for p in paths:
            e = p[-1]
            if e[0] in g:
                for ne in g[e[0]]:
                    np = p[:]
                    np.append(ne)
                    if ne[0] == sink:
                        # check if solution found ....
                        peptide = [e[1] for e in np][1:]
                        ispectrum = ideal_spectrum(peptide,ref_mass)
                        ispectrum.sort()
                        if set(ispectrum) == set(spectrum):
                            return peptide
                    else:
                        npaths.append(np)
        paths = npaths
    return None
    
text = '57 71 154 185 301 332 415 429 486'
spectrum = map(int,text.split(' '))
peptide = spectrum_decoding(spectrum)
assert ''.join(peptide) == 'GPFNA'

text = '103 131 259 287 387 390 489 490 577 636 690 693 761 840 892 941 1020 1070 1176 1198 1247 1295 1334 1462 1481 1580 1599 1743 1762 1842 1861 2005 2024 2123 2142 2270 2309 2357 2406 2428 2534 2584 2663 2712 2764 2843 2911 2914 2968 3027 3114 3115 3214 3217 3317 3345 3473 3501 3604'
spectrum = map(int,text.split(' '))
peptide = spectrum_decoding(spectrum)
assert ''.join(peptide) == 'CRQCSLAMQRASQHYVYVWPQETFGFVCRM'

def peptide_vector(peptide, ref_mass = amino_acid_mass):
    """
    CODE CHALLENGE: Solve the Converting a Peptide into a Peptide Vector Problem.
    Given: An amino acid string P.
    Return: The peptide vector of P (in the form of space-separated integers).
    """
    li = [ ref_mass[aa] for aa in peptide]
    n = len(li)
    pm = [sum(li[:i]) for i in range(1,n+1)]
    P = np.zeros(max(pm),dtype = int)
    for e in pm:
        P[e-1]=1
    return P

   
peptide = 'XZZXX'
P = peptide_vector(peptide,toy_mass)
assert ' '.join(map(str,P)) == '0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 1'

def vector_peptide(P, ref_mass = amino_acid_mass):
    """
    CODE CHALLENGE: Solve the Converting a Peptide Vector into a Peptide Problem.
    Given: A space-delimited binary vector P
    Return: An amino acid string whose binary peptide vector matches P. For masses
    with more than one amino acid, any choice may be used.
    """
    pm = [i+1 for i,v in enumerate(P) if v==1]
    pm_max = max(pm)
    sm = [pm_max - e for e in pm[:-1]]
    peptide = spectrum_decoding(pm+sm,ref_mass)
    return peptide[::-1]
    
text = '0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 1'
P = map(int,text.split(' '))
assert ''.join(vector_peptide(P,toy_mass)) == 'XZZXX'

############################################################
fpath = 'C:/Users/ngaude/Downloads/'
#fpath = '/home/ngaude/Downloads/'
#fpath = 'C:/Users/Utilisateur/Downloads/'
############################################################



#fname = fpath + 'dataset_11813_2.txt'
#with open(fname, 'r') as f:
#    text = f.read()
#    lines = text.split('\n')
#    spectrum = map(int,lines[0].split(' '))
#    adj = spectrum_graph(spectrum)
#with open(fname+'.out','w') as f:
#    for a,b,c in adj:
#        f.write(str(a)+'->'+str(b)+':'+c+'\n')

#fname = fpath + 'dataset_11813_4.txt'
#with open(fname, 'r') as f:
#    text = f.read()
#    lines = text.split('\n')
#    spectrum = map(int,lines[0].split(' '))
#    peptide = spectrum_decoding(spectrum)
#    print ''.join(peptide)

#fname = fpath + 'dataset_11813_6.txt'
#with open(fname, 'r') as f:
#    text = f.read()
#    lines = text.split('\n')
#    peptide = lines[0]
#    P = peptide_vector(peptide)
#with open(fname+'.out','w') as f:
#    f.write(' '.join(map(str,P)))


fname = fpath + 'dataset_11813_8.txt'
#fname = fpath + 'peptide_vector_to_peptide.txt'
with open(fname, 'r') as f:
    text = f.read()
    lines = text.split('\n')
    P = map(int,lines[0].split(' '))
    peptide = vector_peptide(P)
    print ''.join(peptide)
