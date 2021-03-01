# Natural Computing, assignment 3 
# Guus, Bono, Charlotte 

# AUC when changing parameter r (n=10)

library(pROC)
library(comprehenr)
library(ggplot2)

work_dir <- "/Users/charlottecvn/Downloads/Natural Computing/assignment_3/negative-selection"
setwd(work_dir)
save_dir = paste(work_dir, '/Task1', sep="")

merged_test <- read.table('merged.test')[,1]
english_test <- read.table('english.test')[,1]
tagalog_test <- read.table('tagalog.test')[,1]

#r=1, r=3, r=7, r=9
r_values <- c(1,3,7,9)

sensitivity <- function(distinct, results){
  sensitivity_distinct = list()
  n = 0
  for (i in distinct) {
    higher_score = to_vec(for(x in results) if(x > i) x)
    sensitivity_i = length(higher_score)/length(results)
    sensitivity_distinct[n] = sensitivity_i
    n=n+1
  }
  return(array(as.numeric(unlist(sensitivity_distinct)), dim=c(length(sensitivity_distinct))))
}

specificity <- function(distinct, results){
  specificity_distinct = list()
  n = 0
  for (i in distinct) {
    higher_score = to_vec(for(x in results) if(x < i) x)
    specificity_i = length(higher_score)/length(results)
    specificity_distinct[n] = specificity_i
    n=n+1
  }
  return(array(as.numeric(unlist(specificity_distinct)), dim=c(length(specificity_distinct))))
}

#create function to loop over r values
auc_r <- function(r_values){
  for (i in r_values){
    command_merged <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < merged.test > Task1/merged_test_results_r%i.txt', i, i)
    command_english <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < english.test > Task1/english_test_results_r%i.txt', i, i)
    command_tagalog <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < tagalog.test > Task1/tagalog_test_results_r%i.txt', i, i)
    
    command_results_merged <- readline(prompt=paste("Execute in terminal:", command_merged))
    command_results_english <- readline(prompt=paste("Execute in terminal:", command_english))
    command_results_tagalog <- readline(prompt=paste("Execute in terminal:", command_tagalog))
    
    merged_results <- read.table(sprintf('Task1/merged_test_results_r%i.txt', i))[,1]
    english_results <- read.table(sprintf('Task1/english_test_results_r%i.txt', i))[,1]
    tagalog_results <- read.table(sprintf('Task1/tagalog_test_results_r%i.txt', i))[,1]
      
    sorted_anomaly <- sort(merged_results)
    distinct <- sort(unique(sorted_anomaly))
      
    predictors <- c(to_vec(for(i in 1:length(english_test))  0),  to_vec(for(i in 1:length(tagalog_test))  1))
    roc_object <- roc(predictors, merged_results)
    auc_roc_score <- auc(roc_object)
      
    sensitivity_auc <- sensitivity(distinct, tagalog_results)
    specificity_auc <- specificity(distinct, english_results)
      
    part_title <- sprintf('ROC-curve, n=10 r=%i, score=',i)
    setwd(save_dir)
    pdf(sprintf('task1-1_ROC_r%i.pdf',i))
    plot(sort(sensitivity_auc), sort(specificity_auc), type="l", col="red", xlim=c(0,1), ylim=c(0,1),
         xlab="sensitivity", ylab="specificity", 
         main=(paste(part_title,format(round(auc_roc_score, 2), nsmall = 2))))
    abline(0,1,lty=2,col="blue")
    dev.off()
    setwd(work_dir)
  }
}

auc_r(r_values)
