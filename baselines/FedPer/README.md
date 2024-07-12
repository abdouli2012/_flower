---
title: Federated Learning with Personalization Layers
url: https://arxiv.org/abs/1912.00818
labels: ["system heterogeneity", "image classification", "personalization", "horizontal data partition"] # please add between 4 and 10 single-word (maybe two-words) labels (e.g. "system heterogeneity", "image classification", "asynchronous", "weight sharing", "cross-silo")
dataset: ["CIFAR-10", "FLICKR-AES"] # list of datasets you include in your baseline
---

# Federated Learning with Personalization Layers

> Note: If you use this baseline in your work, please remember to cite the original authors of the paper as well as the Flower paper.

****Paper:**** : https://arxiv.org/abs/1912.00818

****Authors:**** : Manoj Ghuhan Arivazhagan, Vinay Aggarwal, Aaditya Kumar Singh, and Sunav Choudhary

****Abstract:**** : The emerging paradigm of federated learning strives to enable collaborative training of machine learning models on the network edge without centrally aggregating raw data and hence, improving data privacy. This sharply deviates from traditional machine learning and necessitates design of algorithms robust to various sources of heterogeneity. Specifically, statistical heterogeneity of data across user devices can severely degrade performance of standard federated averaging for traditional machine learning applications like personalization with deep learning. This paper proposes `FedPer`, a base + personalization layer approach for federated training of deep feed forward neural networks, which can combat the ill-effects of statistical heterogeneity. We demonstrate effectiveness of `FedPer` for non-identical data partitions of CIFAR datasets and on a personalized image aesthetics dataset from Flickr.

## About this baseline

****What’s implemented:**** : The code in this directory replicates the experiments in _Federated Learning with Personalization Layers_ (Arivazhagan et al., 2019) for MNIST and FLICKR-AES datasets, which proposed the `FedPer` model. Specifically, it replicates the results found in figures 2, 4, 7, and 8 in their paper. 

****Datasets:**** : MNIST from PyTorch's Torchvision and FLICKR-AES. FLICKR-AES was proposed as dataset in _Personalized Image Aesthetics_ (Ren et al., 2017) and can be found on thier [GitHub](https://github.com/alanspike/personalizedImageAesthetics). 

****Hardware Setup:**** :warning: *_Give some details about the hardware (e.g. a server with 8x V100 32GB and 256GB of RAM) you used to run the experiments for this baseline. Someone out there might not have access to the same resources you have so, could list the absolute minimum hardware needed to run the experiment in a reasonable amount of time ? (e.g. minimum is 1x 16GB GPU otherwise a client model can’t be trained with a sufficiently large batch size). Could you test this works too?_*

****Contributors:**** : William Lindskog


## Experimental Setup

****Task:**** : Image Classification

****Model:**** : Currently using ResNet34 (MobileNet-V1 will be implemented). 

****Dataset:**** : CIFAR10, CIFAR100, FLICKR-AES

****Training Hyperparameters:**** :warning: *_Include a table with all the main hyperparameters in your baseline. Please show them with their default value._*


## Environment Setup

- Ensure you are in ./baselines/FedPer
- running with Python 3.9.5
- `poetry shell` there to active environment. 
- Run module using python -m FedPer.main
- base.yaml has the configuration. Set to 2 `num_head_layers` for the same experiment set up as in Figure 2, see [paper](https://arxiv.org/pdf/1912.00818.pdf). 


## Running the Experiments

:warning: _Provide instructions on the steps to follow to run all the experiments._
```bash  
# The main experiment implemented in your baseline using default hyperparameters (that should be setup in the Hydra configs) should run (including dataset download and necessary partitioning) by executing the command:

poetry run -m <baseline-name>.main <no additional arguments> # where <baseline-name> is the name of this directory and that of the only sub-directory in this directory (i.e. where all your source code is)

# If you are using a dataset that requires a complicated download (i.e. not using one natively supported by TF/PyTorch) + preprocessing logic, you might want to tell people to run one script first that will do all that. Please ensure the download + preprocessing can be configured to suit (at least!) a different download directory (and use as default the current directory). The expected command to run to do this is:

poetry run -m <baseline-name>.dataset_preparation <optional arguments, but default should always run>

# It is expected that you baseline supports more than one dataset and different FL settings (e.g. different number of clients, dataset partitioning methods, etc). Please provide a list of commands showing how these experiments are run. Include also a short explanation of what each one does. Here it is expected you'll be using the Hydra syntax to override the default config.

poetry run -m <baseline-name>.main  <override_some_hyperparameters>
.
.
.
poetry run -m <baseline-name>.main  <override_some_hyperparameters>
```


## Expected Results

:warning: _Your baseline implementation should replicate several of the experiments in the original paper. Please include here the exact command(s) needed to run each of those experiments followed by a figure (e.g. a line plot) or table showing the results you obtained when you ran the code. Below is an example of how you can present this. Please add command followed by results for all your experiments._

```bash
# it is likely that for one experiment you need to sweep over different hyperparameters. You are encouraged to use Hydra's multirun functionality for this. This is an example of how you could achieve this for some typical FL hyperparameteres

poetry run -m <baseline-name>.main --multirun num_client_per_round=5,10,50 dataset=femnist,cifar10
# the above command will run a total of 6 individual experiments (because 3client_configs x 2datasets = 6 -- you can think of it as a grid).

[Now show a figure/table displaying the results of the above command]

# add more commands + plots for additional experiments.
```
