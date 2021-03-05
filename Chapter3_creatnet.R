#创建网络
library(statnet)
creat <- function(y){
  path1 <- paste("data/",y,".csv",sep="")
  path2 <- paste("data/",y,"Node2.csv",sep='')
  edgelist <- read.csv(path1)
  n <- network(edgelist)
  #导入节点属性表，添加属性
  nodeinfo <- read.csv(path2,header=T,stringsAsFactors=FALSE,quote = "")
  n %v% "industry" <- nodeinfo[,4]
  n %v% "type" <- nodeinfo[,5]
  n %v% "area" <- nodeinfo[,6]
  n %v% "pop" <- nodeinfo[,7]
  n %v% "finrev" <- nodeinfo[,8]
  n %v% "finrevpc" <- nodeinfo[,9]
  return(n)
}

i = 2009
n <- creat(i)
assign(paste("n",substring(as.character(i),3,4),sep=""),n)

#保存网络数据
save(n09,file = 'data/n09.rda')
