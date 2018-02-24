import os
import sys
import PCP_org_v0a
import PCP_org_v1a
import ICPCP_v2
import run


source = sys.argv[1]

algos=[ICPCP_v2,PCP_org_v0a,PCP_org_v1a]

types=['montage','cybershake','epigenomics','inspiral','sipht']
#types=['sipht']

for type in types:

    walk_dir = source +"/"+type
    print('walk_dir = ' + walk_dir)
    #print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

    dag_list = []
    for root, subdirs, files in os.walk(walk_dir):
        for subdir in subdirs:
            if os.path.isdir(root+"/"+subdir):
                dag_list.append(subdir)

    print "dag list: " + str(dag_list)
    print "in dir: " + walk_dir

    files = []
    for algo in algos:
        name_split = str(algo).split(".")[len(str(algo).split("."))-2].split("_")
        suffix = name_split[len(name_split)-1]

        #filename will end with the algo s suffix
        current_file = open(str(type + "_" + suffix + ".txt"),"w")
        files.append(str(type + "_" + suffix + ".txt"))

        run.run_dichotomy(algo, dag_list, walk_dir, current_file)
        #runner.algo_full_range(algo, dag_list, walk_dir, current_file)

        current_file.close()
        print "file closed"