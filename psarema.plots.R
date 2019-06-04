rm(list=ls())
library(tidyverse)

args <- commandArgs(trailingOnly=TRUE)
pID=args[1]


file1=paste(pID,".summaryStats.1.tab",sep="")
file2=paste(pID,".summaryStats.2.tab",sep="")
file3.1=paste(pID,".summaryStats.3.1.tab",sep="")
filePOP="popSUPERpop.tab"

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


pdf("plot.1.noPOPperINS.pdf", height = 7, width = 10)
table2=read.table(file2,sep="\t",fill = TRUE)

data2=data.frame(x=table2[2:nrow(table2),1],y=as.numeric(as.character(table2[2:nrow(table2),2])))
ylinedata2=unique(sort(as.numeric(as.character(table2[2:nrow(table2),2]))))


ggplot(data2,aes(x=x,y=y))+
  geom_point(size=6,color="red",alpha=0.5,shape=20,stroke=1) +
  geom_segment(aes(x=x, xend=x,y=0,yend=y))+
  ylab("Number of Populations") +
  xlab("Insertion")+
  #theme_light()+
  scale_y_continuous(breaks=ylinedata2)+
  guides(fill="colorbar")+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black")
        ,axis.text.x = element_text(angle=45,hjust=1,vjust=1,face="plain"))+
  geom_text(aes(label = y, y = y), size = 3, position = position_dodge(),color="black",vjust=-1.3)

dev.off()


table3.1=read.table(file3.1,sep="\t",header=TRUE)
plot_list3 = list()

pdf("plot.2.noSAMPLESperINSperPOP.pdf", height = 100, width = 10)
#layout( matrix(1:(2*length(unique(table3.1$POP))), ncol = 2, byrow = T))
for (i in(1:length(unique(table3.1$POP)))){
  pop=(unique(table3.1$POP))[i]
  popdata=table3.1[which(table3.1[,1]==pop),]
  
  data3=data.frame(x=popdata$INS,y=popdata$NoOfPeople)
  ylinedata3=unique(sort(popdata$NoOfPeople))
  xlinedata3=unique(sort(popdata$INS))
  
  x=ggplot(data3,aes(x=x,y=y))+
    geom_point(size=3,color="red",alpha=0.5,shape=20,stroke=1) +
    geom_segment(aes(x=x, xend=x,y=0,yend=y))+
    ylab("Number of Samples") +
    xlab(paste("Number of Insertions in",pop,sep=" "))+
    #theme_light()+
    scale_y_continuous(breaks=ylinedata3)+
    scale_x_continuous(breaks=xlinedata3)+
    guides(fill="colorbar")+
    theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          panel.background = element_blank(), axis.line = element_line(colour = "black")
          ,axis.text.x = element_text(angle=45,hjust=1,vjust=1,face="plain")) +
    geom_text(aes(label = y, y = y), size = 3, position = position_dodge(),color="black",vjust=-1.3)
  plot_list3[[i]]=x
}

multiplot(plot_list3[[1]],plot_list3[[2]],plot_list3[[3]],plot_list3[[4]],plot_list3[[5]],
          plot_list3[[6]],plot_list3[[7]],plot_list3[[8]],plot_list3[[9]],plot_list3[[10]],
          plot_list3[[11]],plot_list3[[12]],plot_list3[[13]],plot_list3[[14]],plot_list3[[15]],
          plot_list3[[16]],plot_list3[[17]],plot_list3[[18]],plot_list3[[19]],plot_list3[[20]],
          plot_list3[[21]],plot_list3[[22]],plot_list3[[23]],plot_list3[[24]],plot_list3[[25]],plot_list3[[26]],
          cols=2)

dev.off()


table1=read.table(file1,sep="\t",header = TRUE)
tablePOP=read.table(filePOP,sep="\t",header = TRUE)

data1=matrix(nrow = nrow(table1)*length(unique(table3.1$POP)),ncol = 6)
colnames(data1)=c("insID","pop","#11","#00","%11","SuperPOP")
z=1
for (ins in (1:nrow(table1))){
  for (i in unique(table3.1$POP)){
    
    id01=paste(i,"01",sep=".")
    id11=paste(i,"11",sep=".")
    
    counter=table1[ins,id11]*2 + table1[ins,id01]
    
    data1[z,1]=toString(table1[ins,1])
    data1[z,2]=i
    data1[z,3]=counter
    
    zerodata=table3.1[which(table3.1[,1]==i),]
    zerodata=zerodata[which(zerodata[,2]==0),]
    data1[z,4]=zerodata[1,3]*2 + table1[ins,id01]   #01 has also a 0
    data1[z,5]=0
    data1[z,6]=as.character(tablePOP[which(tablePOP[,1]==i),2])
    z=z+1
  }
}


for (i in(1:length(unique(tablePOP$superpop)))){
  pop=(unique(tablePOP$superpop))[i]
  subset=data1[which(data1[,6]==pop),]
  
  finaldata=matrix(nrow=length(unique(subset[,1])),ncol=6)
  colnames(finaldata)=c("insID","haps11","haps00","%11","%00","SUPERPOP")
  rownames(finaldata)=unique(subset[,1])
  for (o in (1:length(unique(subset[,1])))){
    ins=(unique(subset[,1]))[o]
    subset2=subset[which(subset[,1]==ins),]
    finaldata[o,1]=ins
    finaldata[o,2]=sum(as.numeric(as.character(subset2[,3])))
    finaldata[o,3]=sum(as.numeric(as.character(subset2[,4])))
    msum=sum(as.numeric(as.character(subset2[,3])))+sum(as.numeric(as.character(subset2[,4])))
    finaldata[o,4]=sum(as.numeric(as.character(subset2[,3])))/msum
    finaldata[o,5]=sum(as.numeric(as.character(subset2[,4])))/msum
    finaldata[o,6]=subset2[1,6]
  }
  
  write.table(finaldata,file=paste("sPOP.",pop,".quan.tab",sep=""),col.names = T,sep = "\t")
}
