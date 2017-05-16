__author__ = 'Jonathan Rubin'

import matplotlib
matplotlib.use('Agg')
import pybedtools
from pybedtools import BedTool
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import os
from numpy import random as rn
import load

def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

def find_nearest(array):
    l = len(array)
    result = list()
    for i in range(l):
        if i == 0:
            result.append(math.fabs(array[1][0] - array[i][1]))
        elif i == l-1:
            result.append(math.fabs(array[i][0] - array[i-1][0]))
        else:
            result.append(min(math.fabs(array[i][1] - array[i+1][0]),math.fabs(array[i][0] - array[i-1][1])))

    return result

def run(DMSO,Nutlin1,Nutlin3,P53,figuredir):
    D = BedTool(DMSO)
    N1 = BedTool(Nutlin1)
    N3 = BedTool(Nutlin3)
    P = BedTool(P53).cut([0,1,2])


    w1 = D
    w1rand = BedTool([P[i] for i in rn.randint(0,len(P),len(w1))]).sort()
    w2 = N1-D
    w2rand = BedTool([P[i] for i in rn.randint(0,len(P),len(w2))]).sort()
    w3 = N3-N1-D
    w3rand = BedTool([P[i] for i in rn.randint(0,len(P),len(w3))]).sort()

    a = w2.closest(w1, d=True)
    b = w2rand.closest(w1rand, d=True)
    c = w3.closest(w2, d=True)
    d = w3rand.closest(w2rand, d=True)

    F = plt.figure()
    ax1 = F.add_subplot(221)
    ax1.set_title('Wave2 to Wave1')
    ax1.set_ylabel('Count')
    ax1.set_xlabel('Distance (bp)')
    ax1.set_xlim([0,35000000])
    ax1.hist([float(x[-1]) for x in a],bins=100)

    ax2 = F.add_subplot(222)
    ax2.set_title('Wave2rand to Wave1rand')
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Distance (bp)')
    ax2.set_xlim([0,35000000])
    ax2.hist([float(x[-1]) for x in b],bins=100)

    ax3 = F.add_subplot(223)
    ax3.set_title('Wave3 to Wave2')
    ax3.set_ylabel('Count')
    ax3.set_xlabel('Distance (bp)')
    ax3.set_xlim([0,35000000])
    ax3.hist([float(x[-1]) for x in c],bins=100)

    ax4 = F.add_subplot(224)
    ax4.set_title('Wave3rand to Wave2rand')
    ax4.set_ylabel('Count')
    ax4.set_xlabel('Distance (bp)')
    ax4.set_xlim([0,35000000])
    ax4.hist([float(x[-1]) for x in d],bins=100)



    plt.savefig(figuredir + 'Cluster_analysis.png', dpi=1200)

def nearest_neighbor(DMSO,Nutlin1,Nutlin3,P53):
    a = load.load_bed_points(DMSO)
    b = load.load_bed_points(Nutlin1)
    c = load.load_bed_points(Nutlin3)
    P = load.load_bed_points(P53)

    arand = set()
    while len(arand) < len(a):
        arand.add(rn.randint(0,len(P)))
    arand = list(arand)

    brand = set()
    while len(arand) < len(b):
        brand.add(rn.randint(0,len(P)))
    brand = list(brand)

    crand = set()
    while len(arand) < len(c):
        crand.add(rn.randint(0,len(P)))
    crand = list(crand)

    print len(arand),len(brand),len(crand)

    # F = plt.figure()
    # ax1 = F.add_subplot(221)
    # plt.hist([l for l in find_nearest(a)],bins=100)
    # # ax1.set_xlim([0,500])
    # ax1.set_title('DMSO')
    # ax1.set_ylabel('Count')
    # ax1.set_xlabel('Peak Distance')
    # ax2 = F.add_subplot(222)
    # plt.hist([m for m in find_nearest(b)],bins=100)
    # # ax2.set_xlim([0,500])
    # ax2.set_title('Nutlin 1hr')
    # ax2.set_ylabel('Count')
    # ax2.set_xlabel('Peak Distance')
    # ax3 = F.add_subplot(223)
    # plt.hist([n for n in find_nearest(c)],bins=100)
    # # ax3.set_xlim([0,500]) 
    # ax3.set_title('Nutlin 3hr')
    # ax3.set_ylabel('Count')
    # ax3.set_xlabel('Peak Distance')
    # # plt.savefig(figuredir + 'nearest_neighbor.png', dpi=1200)
    # plt.show()
    


if __name__ == "__main__":
    #Home directory
    homedir = os.path.dirname(os.path.realpath(__file__))

    #File directory
    filedir = parent_dir(homedir) + '/files/'
    file2dir = parent_dir(homedir) + '/files2/'
    figuredir = parent_dir(homedir) + '/figures/'

    DMSO = file2dir + 'DMSO1Hr_peaks.merge_200.bed'
    Nutlin1 = file2dir + 'Nutlin1Hr_peaks.merge_200.bed'
    Nutlin3 = file2dir + 'Nutlin3Hr_peaks.merge_200.bed'
    P53 = file2dir + 'HO_P53_HUMAN.H10MO.B.pval-6.bed'
    P53 = '/Users/jonathanrubin/Google Drive/Colorado University/Jonathan/P53_fimo.bed'
    # run(DMSO,Nutlin1,Nutlin3,P53,figuredir)

    P53 = '/Users/jonathanrubin/Google Drive/Colorado University/Jonathan/P53_fimo.no_header.bed'
    nearest_neighbor(DMSO,Nutlin1,Nutlin3,P53)
