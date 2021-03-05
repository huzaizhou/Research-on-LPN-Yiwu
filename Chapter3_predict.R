library(statnet)
load('data/n09.rda')

#模型1预测值
predictm1=function(start,end,n,nodeinfo){
  start.attr <- nodeinfo[start,]
  end.attr <- nodeinfo[end,]
  
  start.area <- start.attr[1,'area']
  end.area <- end.attr[1,'area']
  area <- ifelse (start.area == end.area, 1, 0)
  
  start.ind <- start.attr[1,'industry']
  end.ind <- end.attr[1,'industry']
  ind <- ifelse (start.ind == end.ind, 1, 0)
  
  start.type <- start.attr[1,'type']
  end.type <- end.attr[1,'type']
  start.type <- ifelse (start.type == 'E', 1, 0)
  end.type <- ifelse (end.type == 'E', 1, 0)
  
  start.pop <- start.attr[1,'总人口']
  end.pop <- end.attr[1,'总人口']
  
  start.pcr <- start.attr[1,'人均财政收入']
  end.pcr <- end.attr[1,'人均财政收入']
  
  p <- 1/(1+exp(-(-7.176 + 2.224*area - 0.06856*ind + 0.1717*start.type + 0.1554*end.type - 5.323e-07*start.pop - 5.648e-07*end.pop - 7.293e-05*start.pcr - 6.676e-06*end.pcr)))
  return (p)
}

#模型2预测值
predictm2=function(start,end,n,nodeinfo){
  start.attr <- nodeinfo[start,]
  end.attr <- nodeinfo[end,]
  
  start.area <- start.attr[1,'area']
  end.area <- end.attr[1,'area']
  area <- ifelse (start.area == end.area, 1, 0)
  
  start.ind <- start.attr[1,'industry']
  end.ind <- end.attr[1,'industry']
  ind <- ifelse (start.ind == end.ind, 1, 0)
  
  start.type <- start.attr[1,'type']
  end.type <- end.attr[1,'type']
  start.type <- ifelse (start.type == 'E', 1, 0)
  end.type <- ifelse (end.type == 'E', 1, 0)
  
  start.pop <- start.attr[1,'总人口']
  end.pop <- end.attr[1,'总人口']
  
  start.pcr <- start.attr[1,'人均财政收入']
  end.pcr <- end.attr[1,'人均财政收入']
  
  recp <- length(get.edges(n,end,alter=start,neighborhood='out'))
  
  start.neighbor <- get.neighborhood(n,start,type='out')
  end.neighbor <- get.neighborhood(n,end,type='in')
  esp <- length(intersect(start.neighbor,end.neighbor))
  gwesp <- (1-exp(-0.3467))^esp
  
  od <- length(start.neighbor)
  id <- length(end.neighbor)
  gwod <- (1-exp(-1.516))^od
  gwid <- (1-exp(-1.552))^id
  
  p <- 1/(1+exp(-(-7.462 + 1.42*area + 0.05195*ind - 0.1077*start.type + 0.1829*end.type - 2.814e-07*start.pop - 7.530e-07*end.pop - 0.0003893*start.pcr + 0.0001906*end.pcr + 11.97*recp + 0.1005*gwesp - 0.716*gwod - 3.35*gwid)))
  return (p)
}

#已有关系的概率
existing <- function(fun,n,edgelist,nodeinfo){
  value <- c()
  for (i in 1:nrow(edgelist)){
    x <- fun(edgelist[i,1],edgelist[i,2],n,nodeinfo)
    value <- append(value,x)
  }
  return(value)
}

#潜在关系的概率
potential <- function(fun,n,edgelist,nodeinfo){
  value <- c()
  for (i in 1:nrow(nodeinfo)){
    a <- c()
    for (j in 1:nrow(nodeinfo)){
      if (i != j){
        if (nrow(subset(edgelist,heads==i&tails==j))==0){
          x <- fun(i,j,n,nodeinfo)
          a <- append(a,x)
        }
      }  
    }
    value <- append(value,a)
  }
  return(value)
}

predict <- function(model,tie,year){
  #model(预测所用模型):predictm1,predictm2
  #tie(要预测的关系类型):existing,potential
  #year(年份):2009-2017
  y <- substring(as.character(year),3,4)
  edgelist <- read.csv(paste('data/20',y,'.csv',sep=""))
  nodeinfo <- read.csv(paste('data/20',y,'Node2.csv',sep=""))
  value <- tie(model,get(paste("n",y,sep="")),edgelist,nodeinfo)
  mtype <- ifelse((as.character(substitute(model)) == 'predictm1'),1,2)
  ttype <- ifelse((as.character(substitute(tie)) == 'existing'),1,2)
  name <- paste("p",ttype,"m",mtype,"_",year,sep="")
  assign(name,value)
  save(list=c(name),file=paste('data/',name,'.rda',sep=""))
  write.csv(value, file = paste('data/',name,'.txt',sep=""), row.names = FALSE)
  return(value)
}

predict(predictm2,existing,2009)

load('data/p1m2_2009.rda')
read.csv('data/p1m2_2009.txt')
