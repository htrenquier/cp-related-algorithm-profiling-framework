import sys
import os
import math
import traceback
import time

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__

# This function only tests the algorithm for specific values of p.
# It aims at finding the shortest deadline that the algorithm is able to vali- date.
# In order to lower the number of runs for time complexity issues,
# run_dichotomy looks for the shortest deadline that the algorithm is capable of reaching.
# This is done by trying several deadlines based on a dichotomy pattern.
def run_dichotomy(algo, list, walk_dir, file):
    print str(algo) + " with dichotomy"
    for dag in list:
        print dag
        file.write("\n"+ dag + "; ")
        p = 1
        min = 1
        max = 101
        redo = 1
        lastp = -1
        while (redo == 1):
            sys.argv = ['','-d', walk_dir, '-i', dag, '-p',str(p)]
            try:
                blockPrint()
                start=time.time()
                ret,pcp = algo.main(sys.argv)
                end=time.time()
                enablePrint()
                if ret == -1:
                    if p == 1:
                        redo = 0
                    else:
                        t = p
                        p=int(math.floor((p + min)/2))
                        max = t
                else:
                    t = p
                    p = int(math.floor((max + p) / 2))
                    min = t

                if p==lastp:
                    redo = 0
                lastp=p
            except Exception, e:
                enablePrint()
                print dag+" failed: " + str(e)
                print sys.exc_info()
                traceback.print_exc()
                time.sleep(2)
        file.write(str(p) + ";" + str(ret) + ";" + str(pcp) + ";" + str(end - start))


#For all integer values of p between 1 and 100, the algorithm A is ran on the DAG D with the deadline computed from p.
# The success (or validity of the configuration given by the algorithm), the time to com- pute the configuration,
# the DAG s name and the percentage for the configuration are saved in a file.
def run_full_range(algo,list,walk_dir,file):
    print str(algo) + " on full range"
    for dag in list:
        print dag
        for p in xrange(1,101):
            sys.argv = ['','-d', walk_dir, '-i', dag, '-p',str(p)]
            try:
                blockPrint()
                start = time.time()
                ret,pcp = algo.main(sys.argv)
                end = time.time()
                enablePrint()
                file.write("\n"+dag +";"+str(p) + ";" + str(ret) + ";" + str(pcp) + ";" + str(end - start))
            except Exception, e:
                enablePrint()
                print dag+" failed: " + str(e)