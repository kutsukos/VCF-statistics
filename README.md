# VCF statistics - psarema
[![uses-bash](https://img.shields.io/badge/Uses%20-Bash-blue.svg)](https://www.gnu.org/software/bash/)
[![Python 2.7](https://img.shields.io/badge/Python-3.9.2-green.svg)](https://www.python.org/)
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
python3 psarema.py
```
This script needs 2 files and generates 3 output files. Please check the global variables on psarema.py, to learn more about the requested input.

The tab-delimited file contains 2 fixed fields per line. All data lines are tab-delimited. Fixed fields are:
1. sample - an identifier to a sample
2. population - the population this sample belongs to

In SupportData directory, you can find <code>1KGP.sample.pop.tab</code> which is a sample file, we are going to use in this tutorial.

This file is suitable to be used for analysis, in samples contained in 1000 genome project. So if your vcf file's samples belong to 1000 genome project, you will probably use <code>1KGP.sample.pop.tab</code> file.
Or else try to keep the same format and the output will be ok.

Output of this script are 3 files:
1. result.1.tab
2. result.2.tab
3. result.2.tab

The first one contains information about each line of your vcf file. Information about the number of samples that have 0/0, 1/1 or 0/1 in each population. This information will help us later to visualize the information from the vcf file.

The 2nd file contains the number of and which populations does have the SNP or whatever a line explains in your vcf file.

The 3rd  file contains information per sample. This file will inform us on how many insertions/SNPs a sample has and in which population this sample belongs.

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

## Contact <a name="contact"></a>
Contact me at <code>ioannis.kutsukos@gmail.com</code> for reporting bugs or anything else! :)
