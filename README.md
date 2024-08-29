# VCF statistics - psarema 0.4
[![uses-bash](https://img.shields.io/badge/Uses%20-Bash-blue.svg)](https://www.gnu.org/software/bash/)
[![Python 2.7](https://img.shields.io/badge/Python-2.7-green.svg)](https://www.python.org/)
[![R 3.6.0](https://img.shields.io/badge/R-3.6.0-green.svg)](https://www.r-project.org/)

## Table of contents
1. [Step 1 - Analysis](#step1)
2. [Step 2 - Visualization](#step2)
3. [About VCF statistics](#about)
4. [Version Changelog](#version)
5. [Contact](#contact)


#### Step 1 - Analysis <a name="step1"></a>
The first step for this analysis is to run <code>psarema.py</code>.

```console
$ python psarema.py --help
Usage: python psarema.py [options]
Options:
  -v FILE, --vcf=FILE  VCF for statistics
  -p FILE, --pop=FILE  File with information about populations
```
This script needs 2 arguments
1. -v | a file to be analysed in VCF format
2. -p | a tab-delimited file with some essential information about which samples belong to each population


This tab-delimited file contains 2 fixed fields per line. All data lines are tab-delimited. Fixed fields are:
1. sample - an identifier to a sample
2. population - the population this sample belongs to

In SupportData directory, you can find <code>1KGP.sample.pop.tab</code> which is a sample file, we are going to use in this tutorial.

This file is suitable to be used for analysis, in samples contained in 1000 genome project. So if your vcf file's samples belong to 1000 genome project, you will probably use <code>1KGP.sample.pop.tab</code> file.
Or else try to keep the same format and the output will be ok.

In conclusion, your command line will like this: 
```console
$ python psarema.py -p 1KGP.sample.pop.tab -v yourfile.vcf 
```

If lets say you have a vcf file named as <code>yourfile.vcf</code> and you have executed the command above, now you have 3 files:
1. yourfile.summaryStats.1.tab
2. yourfile.summaryStats.2.tab
3. yourfile.summaryStats.3.tab

The first one contains information about each line of your vcf file. Information about the number of samples that have 0/0, 1/1 or 0/1 in each population. This information will help us later to visualize the information from the vcf file.

The 2nd file contains the number of and which populations does have the SNP or whatever a line explains in your vcf file.

The 3rd  file contains information per sample. This file will inform us on how many insertions/SNPs a sample has and in which population this sample belongs.

As you may have noticed, that the name of the vcf file, we used in this step, is this pipeline's ID. All products start with this ID.

#### Step 2 - Visualization <a name="step2"></a>
For Step2, we will need  <code>Rscript</code> and <code>tidyverse</code> package. If you dont have it, follow the commands below.
```console
$ R
> install.packages("tidyverse")
> q()
Save workspace image? [y/n/c]: n
```

In order to run this script, we only need one argument and this is the ID of this project and the file <code>popSUPERpop.tab</code>, in the same directory as <code>psarema.plots.R</code> script is.

The file <code>popSUPERpop.tab</code>, that is providen in the <code>SupportData</code> directory has information about the populations from 1000 genome project.

In our example the ID was <code>yourfile</code>, because the vcf file was named <code>yourfile.vcf</code>.

**Does it make sense? __No!__ But we assumed, that was your file's name.**


```console
$ Rscript psarema.plots.R yourfile 
```
The command above, will output 2 pdf files, 5 files (5 super families) with tables, with statistics about each super population and 1 <code>.tab</code> file that contain some extra information, that is needed for the visualization.

The plot1 is showing us in how many populations, a SNP/insertion exists.

The plot2 is showing us, in each population how many samples do have 0,1,2,... insertions/SNPs depending again on the information each line explains in the vcf file and the number of lines.


## ABOUT VCF statistics <a name="about"></a>
This toolset was created when we needed to visualize some of our data and also to make some basic statistical analysis.

Ψάρεμα-Psarema means fishing (in Greek), and this toolkit was named after this, because we try to fish information out of a vcf file...


## VERSION CHANGELOG <a name="version"></a>
<pre>
-0.1 
   + Support files included
   + Files added as arguments and not as hardcoded paths
-0.2 
   + A more informative and well-formated README file
   + Phased data are also supported
-0.3
   + Bug fixed on psarema.plots.R
-0.4 - CURRENT-
   + Updated README file
   + Step 2 and Step 3 are concatenated
-0.5 
   + Python 3 update for the python script
</pre>

## Contact <a name="contact"></a>
Contact me at <code>ioannis.kutsukos@gmail.com</code> for reporting bugs or anything else! :)
