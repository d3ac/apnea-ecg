import os
import pandas as pd
import torch
from torch.utils import data

def get_dataloader_workers():
    return 4

def load_array(data_arrays, bathch_size, istrain):
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, bathch_size, shuffle=istrain)

def readfolder(foldername, batch_size, istrain):
    all_label = None
    all_feature = None
    for filename in os.listdir(foldername):
        excelname = os.path.join(foldername, filename)
        file = pd.read_excel(excelname)
        label = torch.tensor(file.iloc[:,0].values)
        feature = torch.tensor(file.iloc[:,1:].values)
        if all_label is None:
            all_label = label
        else:
            all_label = torch.cat((all_label, label), dim=0)
        if all_feature is None:
            all_feature = feature
        else:
            all_feature = torch.cat((all_feature, feature), dim=0)
    return load_array((all_feature, all_label), batch_size, istrain)

def read_to_csv(foldername):
    all_label = None
    all_feature = None
    for filename in os.listdir(foldername):
        excelname = os.path.join(foldername, filename)
        file = pd.read_excel(excelname,header=None).fillna(0)
        label = torch.tensor(file.iloc[:,0].values)
        feature = torch.tensor(file.iloc[:,1:].values/1000) # ..........
        if all_label is None:
            all_label = label
        else:
            all_label = torch.cat((all_label, label), dim=0)
        if all_feature is None:
            all_feature = feature
        else:
            all_feature = torch.cat((all_feature, feature), dim=0)
    all_feature = all_feature.detach().numpy()
    all_feature = pd.DataFrame(all_feature)
    all_feature.to_csv(foldername+'_feature.csv', header=None, index=False)
    
    all_label = all_label.detach().numpy()
    all_label = pd.DataFrame(all_label)
    all_label.to_csv(foldername+'_label.csv', header=None, index=False)

read_to_csv('test')