args <- commandArgs(trailingOnly=TRUE)
file2open=args[1]
outname=paste(strsplit(x = file2open,".tab")[[1]],".1.tab",sep = "")

#This program need *summary.3.tab file from psaremaPhase1.py output
data=read.table(file=file2open,sep="\t",header=T)

write("POP\tINS\tNoOfPeople",file = outname)
for (i in(1:length(unique(data$POP)))){
  pop=unique(data$POP)[i]
  popdata=data[which(data[,3]==pop),]
  
  for (z in (0:max(popdata[,2]))){
    number=nrow(popdata[(which(popdata[,2]==z)),])
    write(paste(pop,z,number,sep="\t"),file = outname,append=T)
  }
}
