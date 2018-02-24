import numpy as np
import matplotlib.pyplot as plt
import sys

colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
markers=['.',',','o','v','^','<','>','1','2','3','4','8','s','p','*','h','H','+','x','D','d','|','_']

# Returns a mean of a list of ints
def mean(list): #list of ints
    if len(list) == 0:
        return 0
    else:
        sum = 0
        for p in list:
            sum = sum + int(p)
        return sum / len(list)

# returns the metada contained in the file name
def getMetadata(file):
    name = str(file).split(".")[len(str(file).split(".")) - 2]
    type = str(name).split("_")[0]
    suffix = name.split("_")[len(name.split("_"))-1]
    return type,suffix

# opt: 0 => dag name, 1 => perc, 3 => critical path (cp)
def getDataDF(file): #Dicho format
    data = []
    f = open(str(file),'r')
    for line in f.readlines():
        if len(line.split(";")) > 1:
            data.append(line.split(";"))
    f.close()
    return data

# Reads data from a file created by run_full_range method
def getDataFR(file): #Full range format
    dico_time = {str(x): float(x*0) for x in xrange(1, 101)}
    dico_succ = {str(x): x*0 for x in xrange(1, 101)}
    f = open(str(file),'r')
    nb_dags = 0
    dag = ''
    for line in f.readlines():
        olddag = dag
        datum = line.split(";")
        if len(datum) > 1: #we have a data line
            dag = str(datum[0])
            key = str(datum[1]) #the key is the percentage (x axis value)

            #new DAG data
            if olddag != dag:
                nb_dags += 1

            if int(datum[2]) == -1:
                s = 0
            else:
                s = 1
            dico_succ[key] += int(s)
            dico_time[key] += float(datum[4])  # sum of times

    for key in dico_time.keys():
            dico_succ[key] = float(dico_succ[key])/nb_dags
            dico_time[key] = dico_time[key]/nb_dags
    f.close()
    return dico_time,dico_succ

# Returns a list of the tested dags from an outputfile.
# /!\ May return duplicate DAGs for the run_full_range method.
def getDagInputSet(file):
    data = []
    f = open(str(file),"r")
    for line in f.readlines():
        if len(line) > 0:
            data.append(line.split(";")[0])
    f.close()
    return data

# Verifies if the dataset is the same for all tested algorithms.
def verifyInputs(files):
    input_set = getDagInputSet(files[0])
    type,suffix = getMetadata(files[0])
    # verify initial input set
    if len(files) > 1:
        for f in files[1:]:
            if getDagInputSet(f) != input_set:
                # input sets differ => irrelevent comparaison
                print "input sets differ => irrelevent comparaison"
                return -1
            if type != getMetadata(f)[0]:
                # types of dag differ => irrelevent comparaison (?)
                print "types of dag differ => irrelevent comparaison (?)"
                return -1
    print "input data verified"
    return 0


# plot for experiment 1
def plot1(files):

    valid = verifyInputs(files)

    nb_algos = len(files)

    # data to plot
    n_groups = nb_algos

    #create data_structure for plotting
    #files_data = [(file,data_struct),...]
    files_data = []
    for file in files:
        type,suffix = getMetadata(file)
        data_struct= [] #[(nb_nodes,[list of perc values]),...]

        for datum in getDataDF(file):
            dag = datum[0]
            perc = datum[1]
            nb_nodes = str(dag).split(".")[1]
            added = 0
            for d in data_struct:
                if d[0] == nb_nodes:
                    d[1].append(perc)
                    added = 1
            if added == 0:
                data_struct.append((nb_nodes,[perc]))
        files_data.append([suffix,data_struct])

    print "files_data="+ str(files_data)

    print "output data structured"

    # create plot
    fig, ax = plt.subplots()
    ax.plot()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    list_means = [ None ] * len(files_data[0][1])
    # for i in number of different "number of nodes"
    for i in xrange(0,len(files_data[0][1])):  # len of the first data_struct
        list_means[i] = []
        nb_nodes = files_data[0][1][i][0]
        print "nb_nodes=" + str(nb_nodes)
        for file in files_data:
            # append in a list all means for "n node" for all algo
            print "file= " + str(file)
            print "                     " + str(file[1][i][1])
            list_means[i].append(mean(file[1][i][1]))
        print "list_means=" + str(list_means)
        if i == 0:
            plt.bar(index + bar_width, tuple(list_means[i]), bar_width,
                alpha=opacity,
                color=colors[i],
                label=str(nb_nodes) + " nodes")
        else:
            plt.bar(index, tuple(list_means[i]), bar_width,
                    alpha=opacity,
                    color=colors[i],
                    label=str(nb_nodes) + " nodes")



    xticks_labels = []
    for algo in files_data:
        xticks_labels.append(str(algo[0]))

    plt.xlabel('Algorithm')
    plt.ylabel('Average highest percentage')
    plt.title(getMetadata(files[0])[0])

    plt.xticks(index + bar_width, xticks_labels)
    plt.legend()

    try:
        plt.show()
        plt.draw()
        plt.pause(0.001)
        input("Press [enter] to continue.")
    except:
        print "plot issue"

# plot for experiment 2
def plot2(files):
    valid = verifyInputs(files)

    nb_algos = len(files)

    # create data_structure for plotting
    # files_data = [(file,data_struct),...]
    files_data = []
    x_axis = xrange(1,101)
    times = []
    succs = []
    for file in files:
        #type, suffix = getMetadata(file)
        dico_time, dico_succ = getDataFR(file)
        t = []
        s = []
        for k in xrange(1,101):
            t.append(dico_time[str(k)])
            s.append(dico_succ[str(k)])
        times.append(t)
        succs.append(s)
    print succs
    print times

    # Two subplots, the axes array is 1-d
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(x_axis, succs[0],colors[0],succs[1],colors[1],succs[2],colors[2])
    axarr[0].set_title('Success Rate')
    axarr[0].legend()
    axarr[1].plot(x_axis, times[0], colors[0], times[1], colors[1], times[2], colors[2])
    axarr[1].set_title('Average Time [sec]')
    plt.legend(["v2","v0","v1"])

    plt.xlabel('Percentage p')

    plt.show()

    print "files_data=" + str(files_data)

    print "output data structured"


def main(argv):
    plot1(argv)
    #plot2(argv)


if __name__ == '__main__':

    #sys.argv = ['epigenomics_v2a.txt','epigenomics_v0a.txt','epigenomics_v1a.txt']
    #sys.argv = ['cybershake_v2a.txt', 'cybershake_v0a.txt', 'cybershake_v1a.txt']
    #sys.argv = ['inspiral_v2a.txt' ,'inspiral_v0a.txt','inspiral_v1a.txt']
    #sys.argv = ['montage_v2a.txt','montage_v0a.txt', 'montage_v1a.txt']
    #sys.argv = ['sipht_v2a.txt','sipht_v0a.txt','sipht_v1a.txt']

    #sys.argv = ['inspiral_v2.txt', 'inspiral_v0.txt', 'inspiral_v1.txt']
    #sys.argv = ['montage_v2.txt','montage_v0.txt', 'montage_v1.txt']
    #sys.argv = ['cybershake_v2.txt', 'cybershake_v0.txt', 'cybershake_v1.txt']
    #sys.argv = ['sipht_v2.txt', 'sipht_v0.txt', 'sipht_v1.txt']
    #sys.argv = ['epigenomics_v2.txt', 'epigenomics_v0.txt', 'epigenomics_v1.txt']

    main(sys.argv)
