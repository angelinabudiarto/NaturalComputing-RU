Natural Computing Project - Group 8

This repository includes source code, data, a short manual, and a sample run.

# Data
The PCam dataset consists of 220K labeled images. Each image is of size 96x96. When the images is labeled as positive, the center (32x32) contains at least one pixel containing a cancer cell (metastatic tissue). The dataset contains 2 classes. In order to execute the code, 1000 samples have been selected due to limited computing resources.
Data can be retrieved from [Kaggle](https://github.com/basveeling/pcam) or [GitHub](https://www.kaggle.com/andrewmvd/metastatic-tissue-classification-patchcamelyon).

# VGG16 + evolutionary algorithms
In this project we explore three nature inspired alternatives for gradient descent to retrain a well known deep learning model to apply it on a new classification task. The techniques we evaluate are Particle Swarm Optimization, States of Matter Search and Genetic Algorithm. We will retrain the prediction layer of the VGG16 network that was pretrained on ImageNet. In the end we apply this network to the patch camelyon dataset which is a benchmark dataset for a pathological classification problem concerning the identification of metastatic tissue in lymph nodes. Performanced are compared with an instantiation of the network that is trained using Stochastic Gradient Descent with the backpropagation algorithm.

# Manual 
Instructions to repeat project experiments in general when not using Kaggle:

1) Install the requirements (txt file)
   ```` 
    cd VGG16-evolutionary
    pip install -r requirements.txt
   ```` 
2) Download the data
2) Run the wanted experiment to reproduce. Results will be outputed in the notebook.

## Kaggle notebooks
#### Genetic Algorithm
In the case of the Genetic Algorithm a Kaggle notebook is used. There are several example runs on how that looked on Kaggle but for repeating the following has to be done:
1) Import the base notebook to a Kaggle notebook
2) Make sure to include the `metastatic-tissue-classification-patchcamelyon` dataset.
3) Run all (this might take up to 6 hours to complete depending on the parameters set). This is best done by saving the version and when saving select the "Save & Run All" option. In this way the notebook will be executed in the background.
4) When the notebook is finished the results can be checked in the version management of the notebook.

#### PSO
In the case of the PSO a Kaggle notebook is used. There are several example runs on how that looked on Kaggle but for repeating the following has to be done:
1) Import the base notebook to a Kaggle notebook
2) Make sure to include the `metastatic-tissue-classification-patchcamelyon` dataset.
3) Run all (this might take up to 4 hours to complete depending on the parameters set). This is best done by saving the version and when saving select the "Save & Run All" option. In this way the notebook will be executed in the background.
4) When the notebook is finished the results can be checked in the version management of the notebook.

#### SMS


# Sample run
! TO DO
