# Natural Computing, assignment 3 
# Guus, Bono, Charlotte 

# Compute area under the receiver operating characteristic curve (AUC)
# AUC to quantify how well the selection algorithm with parameters n=10, r=4 discriminates indiv English strings from Tagalog

# 1. AUC by merging two test string sets, and then sorting them by the 'anomaly score' that is given by negative selection
# 2. For each possible cut-off score (each distinct value in this list), you compute the sensitivity (percentage of 'anomalous' strings higher than score)
# and the specifity (percentage of 'normal' strings lower than that score. 
# 3. Generate the AUC curve from those values (R package AUC)

work_dir <- "/Users/charlottecvn/Downloads/Natural Computing/assignment_3/negative-selection"
setwd(work_dir)

english_test <- read.table('english.test')
tagalog_test <- read.table('tagalog.test')

merged_test <- rbind(english_test, tagalog_test)
write.table(merged_test, file = "merged.test", quote = FALSE, row.names = FALSE, col.names = FALSE)

