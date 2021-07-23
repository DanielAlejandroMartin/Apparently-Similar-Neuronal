# Apparently-Similar-Neuronal

We include the codes required to reproduce the results of the article

"Apparently similar neuronal dynamics may lead to different collective repertoire" by Margarita M. Sánchez Díaz, Eyisto J. Aguilar Trejo, Daniel A.
Martin, Sergio A. Cannas, Tomás S. Grigera, and  Dante R. Chialvo.

The codes have been written in Fortran 90 and Python 3.

Required Packages:
-------------------


 In Python 3, the following packages are required:
numpy (https://numpy.org/)
matplotlib (https://matplotlib.org/)
networkx  (https://networkx.org/)
random (https://docs.python.org/3/library/random.html)
and
datatime (https://docs.python.org/3/library/datetime.html),

which can be installed on the command line terminal as:

sudo apt-get install python3-numpy
sudo apt-get install python3-matplotlib
sudo pip install networkx
sudo apt-get install python3-datatime
and,
sudo apt-get install python3-random

Documentation for those packages can be found at their respective webpages. matplotlib and datatime are for ploting and time measuring, and can be omitted. In that case, you should comment the lines where respective routines are called.


Program Execution:
------------------

Fortran codes can be compiled and run on a linux or Mac terminal typing gfortran -O3 <program-name>.f90 -o <desired_output_code>
  and then ./<desired_output_code>
  
Python 3 Codes can be run from a terminal typing python3 <desired_code>.py
Be sure to have all required packages.  
  
Python 3 Program Description:  
-----------------------------
  The following codes have been uploaded. I all cases, the mames of the parameters are described in the code, and follow the maiming used on the main text.
 
 GH.py: runs the Greenberg & Hastings implementation on a Watts-Strogatz undirected network. 
 
 KC_m/b/l: runs the Kinouchi & Copelli main/backwards/local implementation on a Watts-Strogatz undirected network.
 
 
  Fortran 90 Program Description:  
---------------------------------
 
  
  
  

