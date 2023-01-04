# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Federated XGBoost utility functions."""

import xgboost as xgb
from xgboost import XGBClassifier, XGBRegressor
from xgboost import plot_tree
import numpy as np
import torch
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader, Dataset


class TreeDataset(Dataset):
    def __init__(self, data, labels):
        self.labels = labels
        self.data = data
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        label = self.labels[idx]
        data = self.data[idx, :]
        sample = {0: data, 1: label}
        return sample


def plot_xgbtree(tree, n_tree):
    xgb.plot_tree(tree, num_trees=n_tree)
    plt.rcParams['figure.figsize'] = [50, 10]
    plt.show()
    return


def construct_tree(dataset, label, n_estimators, tree_type='BINARY'):
    if tree_type == 'BINARY':
        tree = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1, max_depth = 10, n_estimators = n_estimators,
            subsample=0.8, colsample_bylevel=1, colsample_bynode=1, colsample_bytree=1,
            alpha=5, gamma=5,
            num_parallel_tree=1, min_child_weight=1)

    elif tree_type == 'REG':
        tree = xgb.XGBRegressor(objective ='reg:squarederror', learning_rate = 0.1, max_depth = 10, n_estimators = n_estimators,
            subsample=0.8, colsample_bylevel=1, colsample_bynode=1, colsample_bytree=1,
            alpha=5, gamma=5,
            num_parallel_tree=1, min_child_weight=1)
            
    tree.fit(dataset, label)
    return tree


def construct_tree_from_loader(dataset_loader, n_estimators, tree_type='BINARY'):
    for dataset in dataset_loader:
        data, label = dataset[0], dataset[1]
    return construct_tree(data, label, n_estimators, tree_type)


def single_tree_prediction(tree, n_tree, dataset):
    # How to access a single tree
    # https://github.com/bmreiniger/datascience.stackexchange/blob/master/57905.ipynb
    num_t = len(tree.get_booster().get_dump())
    if n_tree > num_t:
        print("The index of tree to be extracted is larger than the total number of trees.")
        return None

    return tree.predict(dataset, iteration_range=(n_tree, n_tree+1), output_margin=True)


def tree_encoding(trainloader, batch_size, client_trees, client_tree_num, client_num):
    if trainloader is None:
        return None
    
    for local_dataset in trainloader:
        X_train, y_train = local_dataset[0], local_dataset[1]
    
    X_train_enc = np.zeros((X_train.shape[0], client_num * client_tree_num))
    X_train_enc = np.array(X_train_enc, copy=True)
    
    if type(client_trees) is not list:
        temp = [client_trees] * client_num
        client_trees = temp
    elif type(client_trees) is list and len(client_trees) != client_num:
        client_trees = client_trees[0]
        temp = [client_trees] * client_num
        client_trees = temp

    for i in range(len(client_trees)):
        for j in range(client_tree_num):
            X_train_enc[:, i*client_tree_num+j] = single_tree_prediction(client_trees[i], j, X_train)

    X_train_enc, y_train = np.float32(X_train_enc), np.float32(y_train)
    X_train_enc, y_train  = torch.from_numpy(np.expand_dims(X_train_enc, axis=1)), torch.from_numpy(np.expand_dims(y_train, axis=-1)) 
    trainset = TreeDataset(X_train_enc, y_train)
    trainset = DataLoader(trainset, batch_size=batch_size, pin_memory=True, shuffle=False)

    return trainset