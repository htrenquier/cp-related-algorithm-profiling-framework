# cp-related-algorithm-profiling-framework
Framework for profiling critical path related algorithms

This project is the result of my Research project.

Reading the paper should help understanding this framework, its features and its goals.

The paper of this project should be released soon.

I was unfortunately not allowed to share the algorithm implementations. I will link them on this project once they get published.

## main.py
Usage: `python main.py input-dags`

The algorithms have to be imported in the script and appended to the list 'algos'.
The list 'types' indicates the input datasets.
It is possible to chose any of the 5 topologies: Montage, Sipht, CyberShake, Inspiral and Epigenomics.

Requirements on the algorithm to test:
	- Input parameters:
		- DAG in the right format ('.propfile') with performance file etc. as stated in the paper
		- The walking-directory to read the DAGs from
		- The percentage p
	- Output parameters:
		- Success of the algorithm ('-1' is failure, '0' if success)
		- Critical path (has to be removed in the next version)

Limitations:
	- The algorithm developper has to parse the DAG himself
	- The algorithm developper has to verify the validity of the final configuration himself

## plot.py
Usage: `python plot.py outputFileName1 outputFileName1 outputFileName3 ...`

outputFileNameN should be named as follows:
'\<dataset\>_\<algorithmName\>.txt'

The file can be read as '.csv' format.


## input-dags
These datasets have been generated from templates available on the Pegasus' project website:
https://confluence.pegasus.isi.edu/display/pegasus/WorkflowGenerator
