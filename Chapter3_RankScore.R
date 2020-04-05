#模型精确度评价 RankScore值
p1 <- read.csv('data/p1m1_2009.txt',header=F)
p2 <- read.csv('data/p2m1_2009.txt',header=F)

rank <- c()
len1 <- nrow(p1)
len2 <- nrow(p2) + 1
for (i in 1:len1){
  t1 <- Sys.time()
  p2n <- append(p1[i,1],p2[,1])
  rank <- append(rank,rank(p2n)[1]/len2)
  t2 <- Sys.time()
  cat(i,difftime(t2,t1),'\n')
}
mean(rank)

rankm2_2009 <- rank
save(rankm2_2009,file='data/rankm2_2009.rda')
