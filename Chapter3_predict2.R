#考察2009年概率较高的潜在关系在2010年网络中是否出现
load('data/p2m2_2009.rda')
edgelist <- read.csv('data/2009.csv')

#找出2009年网络中出现概率较高的潜在关系，前三列为起点、终点、概率
m1 <- matrix(data=0,nrow=711,ncol=3)
index1 <- 0
index2 <- 0
for (i in 1:2886){
  for (j in 1:2886){
    if (i != j){
      if (nrow(subset(edgelist,heads==i&tails==j))==0){
        index1 <- index1 + 1
        p <- p2m2_2009[index1]
        if (p > 0.1){
          index2 <- index2 + 1
          m1[index2,1] <- i
          m1[index2,2] <- j
          m1[index2,3] <- p
        }
      }
    }  
  }
  cat(i,'\n')
}

edge2010 <- read.csv('data/2010.csv')
node2010 <- read.csv('data/2010Node2.csv')

#给m2加上第四列
z <- matrix(data=0,nrow=711,ncol=1)
m2 <- cbind(m1,z)

#如果一条潜在关系出现在了2010年的网络中，m2的第四列标记1
index3 <- 0
for (i in 1:711){
  s09 <- as.character(subset(nodeinfo,code==m2[i,1])[1,'company'])
  e09 <- as.character(subset(nodeinfo,code==m2[i,2])[1,'company'])
  s10 <- as.character(subset(node2010,company==s09)[1,'code'])
  e10 <- as.character(subset(node2010,company==e09)[1,'code'])
  n <- nrow(subset(edge2010,heads==s10&tails==e10))
  if (m2[i,3] > 0.1){
    if (n == 1){
      index3 <- index3 + 1
      m2[i,4] <- n
    }
  }
}
