library(statnet)
load('data/n09.rda')

#主效应模型
k <- c(1,2,3,7,8,10,11,12,16,17,29,23,23,26,27,33,38,41,42,44,45,48,49,52,53,56,58,62,63,66,68,72,73,74)
maineffect <- ergm(n09 ~ edges + nodeicov('pop') + nodeocov('pop') + nodeifactor('type') + nodeofactor('type') + nodematch('area') + nodematch('industry',diff=F,keep=k) + nodeicov('finrevpc') + nodeocov('finrevpc'),
                    control=control.ergm(MCMC.samplesize=200000, MCMC.burnin=2000000,MCMC.interval=2000, seed = 567, parallel=4,parallel.type='PSOCK'), 
                    eval.loglik = T, verbose = T)
summary(maineffect)
save(maineffect,file = 'data/maineffect.rda')

#混合模型
mix <- ergm(n09 ~ edges + mutual + gwesp(1,F) + gwodegree(1,F) + gwidegree(1,F) + nodeicov('pop') + nodeocov('pop') + nodematch('type') + nodematch('area') + nodematch('industry') + nodeicov('finrevpc') + nodeocov('finrevpc'),
            control=control.ergm(MCMC.samplesize=100000, MCMC.burnin=1000000,MCMC.interval=1000, seed = 567, parallel=3,parallel.type='PSOCK'), 
            eval.loglik = T, verbose = T)
summary(mix)
save(mix,file = 'data/mix.rda')

#用模型生成一个仿真网络
nsim <- simulate(mix2, verbose=TRUE, seed=5)
#将两个网络主要的统计量绘制成表格
rowgof <- rbind(summary(n09 ~ edges + idegree(0:20) + esp(1:15) + dsp(1:15) + triadcensus + mutual),
                summary(nsim ~ edges + idegree(0:20) + esp(1:15) + dsp(1:15) + triadcensus + mutual))
rownames(rowgof) <- c("n09", "nsim")
rowgof
#用模型生成多个仿真网络，构造置信区间，查看拟合优度
mix.gof <- gof(mix, GOF = ~triadcensus + idegree + odegree + espartners + dspartners + distance,
                 verbose=T, burnin=10000, interval=10000, control.gof.seed=567)
maineffect.gof <- gof(maineffect, GOF = ~triadcensus + idegree + odegree + espartners + dspartners + distance,
                verbose=T, burnin=10000, interval=10000, control.gof.seed=567)

save(mix.gof,file="data/gof_mix.rda")
save(maineffect.gof,file="data/gof_maineffect.rda")
#绘制拟合优度图形
load("data/gof_mix.rda")
load("data/gof_maineffect.rda")

par(mfrow = c(1,1))
plot(mix2.gof, cex.lab = 1.5, cex.axis = 1.5)
plot(mix2.gof, cex.lab = 1.5, cex.axis = 1.5, plotlogodds = T)
plot(maineffect.gof, cex.lab = 1.5, cex.axis = 1.5, plotlogodds = T)
