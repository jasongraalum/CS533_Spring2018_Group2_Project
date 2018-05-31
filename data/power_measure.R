library(tidyverse)
library(ggplot2)


pmeas<-read_csv("Dataset_Template.csv",col_names = TRUE)
summary(pmeas)


mod_pmeas <- pmeas %>%   
  group_by(`Case Number`,`Loop Count`)%>% 
  summarize(Avg_time=mean(`Time(ms)`),Avg_Power=mean(`Power(kW)`)) 


mod_pmeas<-mod_pmeas %>% 
  mutate(Lines_Code = ifelse(`Loop Count`==100000,"100K",
        ifelse(`Loop Count`==1000000,"1M",
  ifelse(`Loop Count`==10000000,"10M",
  ifelse(`Loop Count`==100000000,"100M","1G")))))           
           

fctlb <-c("1" = "Case 1", "2"="Case 2","3"="Case 3", "4"="Case 4")

p<-ggplot(mod_pmeas)+geom_col(aes(x=Avg_time,y=Avg_Power,
              fill=Lines_Code))+
  facet_wrap(~`Case Number`, labeller=labeller(`Case Number`= fctlb))+
  xlab("Time (ms)")+
  ylab("Power Consumed (kW)")+
  ggtitle("Variance in Power measured across the execution\nof map reduce code on different core execution cases")+
  theme_bw()


p +theme(plot.title = element_text(hjust=0.5),
           title = element_text(colour = "gray25"),
           strip.text.x=element_text(face="bold"),
           strip.background = element_rect(fill="#CCCCFF"),
           axis.text =element_text(color ="black" ) )+
    guides(fill=guide_legend(title="No. of loop\niterations"))
   

ggsave(filename="power_measurement.png",width=9,height=7,dpi=300)  