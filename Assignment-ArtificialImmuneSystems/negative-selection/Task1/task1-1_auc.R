# Natural Computing, assignment 3 
# Guus, Bono, Charlotte 

# Compute area under the receiver operating characteristic curve (AUC)
# AUC to quantify how well the selection algorithm with parameters n=10, r=4 discriminates indiv English strings from Tagalog

# 1. AUC by merging two test string sets, and then sorting them by the 'anomaly score' that is given by negative selection
# 2. For each possible cut-off score (each distinct value in this list), 
# you compute the sensitivity (percentage of 'anomalous' strings higher than score)
# and the specifity (percentage of 'normal' strings lower than that score). 
# 3. Generate the AUC curve from those values 

library(pROC)
library(comprehenr)

work_dir <- "/Users/charlottecvn/Downloads/Natural Computing/assignment_3/negative-selection"
setwd(work_dir)
save_dir = paste(work_dir, '/Task1', sep="")

merged_test <- read.table('merged.test')[,1]
english_test <- read.table('english.test')[,1]
tagalog_test <- read.table('tagalog.test')[,1]

i=4
command_merged <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < merged.test > Task1/merged_test_results_r%i.txt', i, i)
command_english <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < english.test > Task1/english_test_results_r%i.txt', i, i)
command_tagalog <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < tagalog.test > Task1/tagalog_test_results_r%i.txt', i, i)
command_results_merged <- readline(prompt=paste("Execute in terminal:", command_merged))
command_results_english <- readline(prompt=paste("Execute in terminal:", command_english))
command_results_tagalog <- readline(prompt=paste("Execute in terminal:", command_tagalog))

merged_results <- read.table('Task1/merged_test_results_r4.txt')[,1]
english_results <- read.table('Task1/english_test_results_r4.txt')[,1]
tagalog_results <- read.table('Task1/tagalog_test_results_r4.txt')[,1]

sorted_anomaly <- sort(merged_results)
distinct <- unique(sorted_anomaly)

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

predictors <- c(to_vec(for(i in 1:length(english_test))  0),  to_vec(for(i in 1:length(tagalog_test))  1))
roc_object <- roc(predictors, merged_results)
auc_roc_score <- auc(roc_object)

sensitivity_auc <- sensitivity(distinct, tagalog_results)
specificity_auc <- specificity(distinct, english_results)

setwd(save_dir)
pdf("task1-1_ROC.pdf") 
plot(sort(sensitivity_auc), sort(specificity_auc), type="l", col="red",
     xlab="sensitivity", ylab="specificity", 
     main=(paste('ROC-curve, n=10 r=4, score=',format(round(auc_roc_score, 2), nsmall = 2))))
abline(coef = c(0,1),lty=2,col="blue")
dev.off()
setwd(work_dir)

 