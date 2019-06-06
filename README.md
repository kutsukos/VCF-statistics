# VCF statistics - psarema
###### For using this tool you will need to be able to run R code and python.


## TUTORIAL - PIPELINE
#### STEP1 - Analysis phase 1
The first step for this analysis is to run psaremaPhase1.py.

<pre>Usage: python psaremaPhase1.py [options]
Options:
  -v FILE, --vcf=FILE  VCF for statistics
  -p FILE, --pop=FILE  File with information about populations</pre>
  
  The vcf file that will used for this analysis should be defined with -v option.<br/>
The file "1KGP.sample.pop.tab" has the format, that is expected for the second file that we need for this analysis.<br/>
The file "1KGP.sample.pop.tab" was used for analysis in samples contained in 1000 genome project. So if your vcf file's samples belong to 1000 genome project,
you will probably use "1KGP.sample.pop.tab" file.<br/>
Or else try to keep the same format and the output will be ok

In conclusion your command line will like this: <br/>
``` $ python psaremaPhase1.py -p 1KGP.sample.pop.tab -v yourfile.vcf ```

This command line will produce 3 files.
If lets say you have a vcf file named as "test.vcf" and you have runned Step1, now you have 3 files:
1. test.summaryStats.1.tab
2. test.summaryStats.2.tab
3. test.summaryStats.3.tab

The first one will contain information about each line. Information about the number of samples that have 0/0, 1/1 or 0/1 in each population. This information will help us later to visualize the information from the vcf file.
The second file will contain the number of and which populations does have the SNP or whatever a line explains.
The third and final file will contain information per sample. This file will inform us on how many insertions/SNPs a sample has and in which population this sample belongs. This file will be used for a further analysis (Step2) and then for visualization


#### STEP2 - Analysis phase 2
The second step is the easiest one.<br/>
The only file that is needed is one of the files that are already produced by Step1.<br/>
In fact, we need *summaryStats.3.tab.<br/>

For Step2 you will need to run the following command line:<br/>
``` $ Rscript psaremaPhase2.R test.summaryStats.3.tab ```

And this will produce "test.summaryStats.3.1.tab" file which will be used as input in Step3


#### STEP3 - Visualization
For Step3, we will also need to run Rscript and 1 package: tidyverse.<br/>
As you may have noticied the name of the vcf file, we used in Step1 is this pipeline's ID. All products from Step1 have the name of the vcf file that was used.<br/>
In order to run Step3, we only need one argument and this is this ID and the file "popSUPERpop.tab", in the same directory with "psarema.plots.R" script, which contains information about each population, that was analyzed in this pipeline.<br/> 
The file "popSUPERpop.tab", that is providen in this folder has information about the populations from 1000 genome project.

In our example the ID was "test", because the vcf file was named "test.vcf"

So the following command line will run Step3, which will output 2 pdf files and 5 files (5 super families) with tables, with statistics about each super population<br/>
``` $ Rscript psarema.plots.R test ```

The plot1 is showing us in how many populations, a SNP/insertion exists.<br/>
The plot2 is showing us, in each population how many samples do have 0,1,2,... insertions/SNPs depending again on the information each line explains in the vcf file and the number of lines.


## ABOUT VCF statistics
This toolset was created when we needed to visualize some of our data and also to make some basic statistical analysis.<br/>
Ψάρεμα-Psarema means fishing (in Greek), and this toolkit was named after this, because we try to fish information out of a vcf file...


## VERSION CHANGELOG
<pre>
-0.1 
     +support files included
     +files added as arguments and not as hardcoded paths
<br/>
-0.2 
     +a more informative and well-formated README file
     +phased data are also supported
<br/>
-0.3 CURRENT
     +bug fixed on psarema.plots.R
</pre>
## Contact
Contact me at skarisg@gmail.com for reporting bugs or anything else! :)
