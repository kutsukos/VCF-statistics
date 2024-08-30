## INPUT 1: A tab delimited file that matches samples with population. It is providen by 1KGP
## INPUT 2: A vcf file with variants for statistic analysis

from optparse import OptionParser
import sys
from copy import deepcopy

parser = OptionParser()
parser.add_option("-v", "--vcf", dest="vcffile",
                  help="VCF for statistics", metavar="FILE")
parser.add_option("-p", "--pop", dest="popinfo",
                  help="File with information about populations", metavar="FILE")
(options, args) = parser.parse_args()

VCFfile=options.vcffile; POPfile=options.popinfo
outname=VCFfile.split("vcf")[0]

print("Psarema Statistics by kutsukos\n");
print("Reading pop file");


###READING DB from 1KGP and storing information to samplesDB
samplesDB={}
file = open(POPfile, "r")
for line in file:
    words = line.split("\t")
    lineSampleID=words[0]
    linePopulatioName=words[1][0:3]

    #check if population exists
    if((linePopulatioName in samplesDB) ==True):
        samplesDB[linePopulatioName].append(lineSampleID)
    else:
        samplesDB[linePopulatioName]=[]
        samplesDB[linePopulatioName].append(lineSampleID)
file.close()
print("Reading pop file...DONE!");
##DONE


zerozero="0/0"; zeroone="0/1"; oneone="1/1"
samples00={}; samples01={}; samples11={}
insertions=[]


### READING VCF file and storing information about each line in 3 dictionaries
##samples00, samples01, samples11
file = open(VCFfile, "r")
print("Reading VCF file");
for line in file:
    #lline=line.split("\n")
    words = line.split("\t")
    zerozeroCounter = 0;    zerooneCounter = 0;    oneoneCounter = 0;
    if ("#" not in line):

        lineChr = words[0];        linePos = words[1]
        insertionID=lineChr+"."+linePos
        samples00[insertionID]=[]; samples11[insertionID]=[]; samples01[insertionID]=[];
        insertions.append(insertionID)

        counter = 0

        for item in words:
            word=item.split(":")[0]
            if (zerozero in word):
                samples00[insertionID].append(counter)
            elif (oneone in word):
                samples11[insertionID].append(counter)
            elif (zeroone in word):
                samples01[insertionID].append(counter)
            counter = counter + 1;
    else:
        if ("##" not in line):
            headerSplit = line.split("\n")[0].split("\t")
file.close()
##DONE


print("Reading VCF file...DONE!");
print("Analysing data and exporting results");


outputfile=outname+"summaryStats.1.tab"
outputfile2=outname+"summaryStats.2.tab"
outFile = open(outputfile, "w")
outFile2=open(outputfile2,"w")

##time to write on our first 2 outputfiles
#the first one will contain information about each line. information about the number 
# of samples that have 0/0, 1/1 or 0/1 in each population. This information will 
# help us later to visualize the information from the vcf file
# The second file will contain the number of and which populations does have the SNP or whatever a line
# explains.
header="INSERTION\tNo00\tNo01\tNo11\t"
for item in samplesDB:
    header=header + str(item)+".00\t"
for item in samplesDB:
    header = header + str(item) + ".01\t"
for item in samplesDB:
    header=header + str(item)+".11\t"
outFile.write( header+"\n")

##we use deepcopy as the simple copy does a shallow copy of the first struct.
# and for this procedure we want to manipulate the copy and keep the original
# struct untouched
samplesBD2 = deepcopy(samplesDB)

outFile2.write("InsertionID\tno of populations\n")
for item in insertions:
    line2PRINT= item+ "\t"+str(len(samples00[item]))+ "\t"+str(len(samples01[item]))+"\t" +str(len(samples11[item]))+"\t"

    numofPOPs4INS = [];

    for item4 in samplesBD2:
        samplesBD2[item4] = 0;

    for item2 in samples00[item]:
        for pop in samplesDB:
            if (headerSplit[item2] in samplesDB[pop]):
                # print str(item) +"\t" + str(headerSplit[item]) +"\t" +str(pop)
                samplesBD2[pop] = samplesBD2[pop] + 1;
    for item3 in samplesBD2:
        line2PRINT = line2PRINT + str(samplesBD2[item3]) + "\t"

    for item4 in samplesBD2:
        samplesBD2[item4] = 0;

    for item2 in samples01[item]:
        for pop in samplesDB:
            if (headerSplit[item2] in samplesDB[pop]):
                if(pop not in numofPOPs4INS):
                    numofPOPs4INS.append(pop)
                samplesBD2[pop] = samplesBD2[pop] + 1;
    for item3 in samplesBD2:
        line2PRINT = line2PRINT + str(samplesBD2[item3]) + "\t"

    for item4 in samplesBD2:
        samplesBD2[item4] = 0;

    for item2 in samples11[item]:
        for pop in samplesDB:
            if (headerSplit[item2] in samplesDB[pop]):
                if (pop not in numofPOPs4INS):
                    numofPOPs4INS.append(pop)
                samplesBD2[pop] = samplesBD2[pop] + 1;
    for item3 in samplesBD2:
        line2PRINT = line2PRINT + str(samplesBD2[item3]) + "\t"

    outFile.write(line2PRINT+"\n")

    outFile2.write(str(item) +"\t"+ str(len(numofPOPs4INS)))
    for num in numofPOPs4INS:
        outFile2.write("\t"+str(num))

    outFile2.write("\n")
outFile.close()
outFile2.close()
##DONE


##Now lets do some population statistics
# The third and final file will contain information per sample.
# More on this, this file will inform us on how many insertions/SNPs a sample
# has and in which population this sample belongs
# This file will be used for a further analysis and then for visualizing
outputfile3=outname+"summaryStats.3.tab"
outFile3 = open(outputfile3, "w")

#make a dictionary with the same ids but counter as values
counters={}
for item in samplesDB:
    for sample in samplesDB[item]:
        counters[sample]=0;


#parse input file and count people
##
outFile3.write("SampleID\tInsertions\tPOP\n")
for INS in insertions:
    for lineSampleID in samples11[INS]:
        counters[headerSplit[lineSampleID]] = counters[headerSplit[lineSampleID]]+1
    for lineSampleID in samples01[INS]:
        counters[headerSplit[lineSampleID]] = counters[headerSplit[lineSampleID]] + 1

for pop in samplesDB:
    for sample in samplesDB[pop]:
        outFile3.write(sample + "\t" + str(counters[sample]) + "\t" + pop +"\n")

outFile3.close()
##DONE
print ("Analysing data and exporting results...DONE!")
