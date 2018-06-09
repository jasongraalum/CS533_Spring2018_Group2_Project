library(tidyverse)
library(ggplot2)


pmeas<-read_csv("simple_data_move_data.csv",col_names = TRUE)
summary(pmeas)



mod_pmeas <- pmeas %>% 
  mutate(delta_power=power_end-power_start,loop=(loop)^2)


fctlb <-c("out_case1" = "Case 1", "out_case2"="Case 2","out_case3"="Case 3")



my_theme<-function() {
  theme_bw()+
    theme(plot.title = element_text(hjust=0.5),
          title = element_text(colour = "gray25"),
          strip.text.x=element_text(face="bold"),
          strip.background = element_rect(fill="#CCCCFF"),
          axis.text =element_text(color ="black" ) )
  }



f_pmeas <- mod_pmeas %>% 
  group_by(case,loop) %>% 
  summarize(instr_power=sum(instructions)/sum(delta_power))





ggplot(f_pmeas)+geom_col(aes(x=loop,y=instr_power))+
  facet_wrap(~case,labeller=labeller(case= fctlb))+ scale_x_log10()+
ggtitle("L1 Cache miss vs Loop")+ 
  xlab("No. of loop instructions")+
  ylab("Total Instructions / Power ")+my_theme()
ggsave(filename="L1cachemiss_pow-meas.png",width=9,height=7,dpi=300)  

###############################################################


  
  f_pmeas2 <- mod_pmeas %>% 
  group_by(case,loop) %>% 
  summarize(L1cachemiss_pow=sum(`L1-dcache-load-misses`)/sum(delta_power)) 





ggplot(f_pmeas2)+geom_col(aes(x=loop,y=L1cachemiss_pow))+
  facet_wrap(~case, labeller=labeller(case= fctlb))+ scale_x_log10()+
ggtitle("L1 Cache miss vs Loop")+ 
  xlab("No. of loop instructions")+
  ylab("L1 cache miss / Power ")+my_theme()
  ggsave(filename="L1cachemiss_pow-meas.png",width=9,height=7,dpi=300)  

###############################################################
  
  
  f_pmeas3 <- mod_pmeas %>% 
  group_by(case,loop) %>% 
  summarize(L1cache_pow=sum(`L1-dcache-loads`)/sum(delta_power))



ggplot(f_pmeas3)+geom_col(aes(x=loop,y=L1cache_pow))+
ggtitle("L1 Cache loads vs Loop")+ scale_x_log10()+
facet_wrap(~case,labeller=labeller(case= fctlb))+
  xlab("No. of loop instructions")+
  ylab("L1 cache loads / Power ")+my_theme()

ggsave(filename="L1cacheLoads_pow-meas.png",width=9,height=7,dpi=300)  

###############################################################  
  f_pmeas4 <- mod_pmeas %>% 
  group_by(case,loop) %>% 
  summarize(LLC_cache_pow=sum(`LLC-loads`)/sum(delta_power))



ggplot(f_pmeas4)+geom_col(aes(x=loop,y=LLC_cache_pow))+
  facet_wrap(~case,labeller=labeller(case= fctlb))+
ggtitle("LLC Cache Loads vs Loop")+ scale_x_log10()  +
xlab("No. of loop instructions")+
  ylab("LLC cache loads / Power ")+my_theme()
ggsave(filename="LLCcacheloads_pow-meas.png",width=9,height=7,dpi=300)  

###############################################################  
  f_pmeas5 <- mod_pmeas %>% 
  group_by(case,loop) %>% 
  summarize(LLC_cachemiss_pow=sum(`LLC-load-misses`)/sum(delta_power))



ggplot(f_pmeas5)+geom_col(aes(x=loop,y=LLC_cachemiss_pow))+
  facet_wrap(~case,labeller=labeller(case= fctlb))+
  ggtitle("LLC Cache miss vs Loop")+ scale_x_log10()+
xlab("No. of loop instructions")+
  ylab("LLC cache miss / Power ")+my_theme()

ggsave(filename="LLCcachemiss_pow-meas.png",width=9,height=7,dpi=300)  

