# Natural Computing, assignment 3 
# Guus, Bono, Charlotte 

# folder lang contains 4 other languages. determine which can be best discriminated from english using negative selection

library(pROC)
library(comprehenr)
library(ggplot2)

work_dir <- "/Users/charlottecvn/Downloads/Natural Computing/assignment_3/negative-selection"
setwd(work_dir)
save_dir = paste(work_dir, '/Task1', sep="")

#r=4
r_values <- c(4)

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
auc_r_language <- function(language, r_values){
  for (i in r_values){
    english_test <- read.table('english.test')[,1]
    language_test <- read.table(sprintf('lang/%s.txt',language))[,1]
    
    command_language <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < lang/%s.txt > Task1/%s_test_results_r%i.txt', i, language,language, i)
    command_english <- sprintf('java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r %i -c -l < english.test > Task1/english_test_results_r%i.txt', i, i)
    
    command_results_language <- readline(prompt=paste("Execute in terminal:", command_language))
    command_results_english <- readline(prompt=paste("Execute in terminal:", command_english))
    
    language_results <- read.table(sprintf('Task1/%s_test_results_r%i.txt', language,i))
    english_results <- read.table(sprintf('Task1/english_test_results_r%i.txt', i))
    
    merged_results <- rbind(english_results, language_results)[,1]
    
    language_results <- language_results[,1]
    english_results <- english_results[,1]
    
    sorted_anomaly <- sort(merged_results)
    distinct <- sort(unique(sorted_anomaly))
    
    predictors <- c(to_vec(for(i in 1:length(english_test))  0),  to_vec(for(i in 1:length(language_test))  1))
    roc_object <- roc(predictors, merged_results)
    auc_roc_score <- auc(roc_object)
    
    sensitivity_auc <- sensitivity(distinct, language_results)
    specificity_auc <- specificity(distinct, english_results)
    
    part_title <- sprintf('ROC-curve, language:%s, n=10 r=%i, score=',language,i)
    setwd(save_dir)
    pdf(sprintf('task1-3_ROC_%s_r%i.pdf',language,i))
    plot(sort(sensitivity_auc), sort(specificity_auc), type="l", col="red", xlim=c(0,1), ylim=c(0,1),
         xlab="sensitivity", ylab="specificity", 
         main=(paste(part_title,format(round(auc_roc_score, 2), nsmall = 2))))
    abline(0,1,lty=2,col="blue")
    dev.off()
    setwd(work_dir)
  }
}
auc_r_language("hiligaynon", r_values)
auc_r_language("middle-english", r_values)
auc_r_language("plautdietsch", r_values)
auc_r_language("xhosa", r_values)
