import numpy as np
import pandas as pd
import pickle
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.autograd import gradcheck

from torch_geometric.data import Data, DataListLoader

import networkx as nx
from scipy import sparse

from sklearn import preprocessing
# from sklearn.metrics import f1_score, roc_auc_score, average_precision_score, accuracy_score

from model import *
#from utils2 import *
from utils_serve import *

import argparse

import os

from torch.utils.data import DataLoader

class Get_args():
    def __init__(self):
        self.model = 'GEX_PPI_GAT_cat4_MLP'
        self.gex_feat = 'l1000'
        self.drug_feat = 'ecfp'

        self.seed = 44
        self.device = 'cpu'

        self.ecfp_nBits = 2048
        self.ecfp_radius = 2
        self.num_genes = 978

        self.drug_embed_dim = 256
        self.gcn_hidden_dim1 = 64
        self.num_gcn_hops = 3
        self.gat_num_heads = 4
        self.gene2vec_dim = 200

        self.batch_size = 32
        self.num_classes = 2
        self.n_epochs = 20
        self.learning_rate = 5e-4
        self.weight_decay = 1e-5
        self.g2v_pretrained = True
        self.network_name = 'omnipath'
        self.undir_graph = False
        self.dataset_ver = 4
        self.save_model = False
        self.eval = True

def Get_Models(ppi_adj, g2v_embedding, args, device):

    if args.model == 'GEX_PPI_GAT_cat4_MLP':
        return GEX_PPI_GAT_cat4_MLP(ppi_adj, g2v_embedding, args).to(device)

def get_gene_info(args):
    if args.gex_feat == 'l1000':
        gene_info = pd.read_csv('data/GSE92742/GSE92742_Broad_LINCS_gene_info.txt',
                           delimiter = '\t',
                           index_col = 0)
        gene_info = gene_info.loc[gene_info.loc[:, 'pr_is_lm'] == 1].copy()
    elif args.gex_feat == 'ptgs_total':
        gene_info = pd.read_csv('data/GSE92742/GSE92742_Broad_LINCS_gene_info_ptgs_total.txt',
                           delimiter = '\t',
                           index_col = 0)
    elif args.gex_feat == 'ptgs_core':
        gene_info = pd.read_csv('data/GSE92742/GSE92742_Broad_LINCS_gene_info_ptgs_core.txt',
                           delimiter = '\t',
                           index_col = 0)
    else:
        gene_info = pd.read_csv('data/GSE92742/GSE92742_Broad_LINCS_gene_info.txt',
                           delimiter = '\t',
                           index_col = 0)
    return gene_info

class Model_serve():
    def __init__(self):
        args = Get_args()

        gene_info = get_gene_info(args)
        if 'PPI' in args.model:
            gene2vecdict, gene_info, ppi_adj, ppi_nx, g2v_embedding, get_gex_idxs, args = get_ppi_features(gene_info, args)

        device = torch.device(args.device)
        model = Get_Models(ppi_adj, g2v_embedding, args, device)

        model_path = 'models/'+str(args.model)+str(args.num_gcn_hops)+'_'+str(args.drug_feat)+'_'+str(args.gex_feat)+'_'+str(args.learning_rate)+'_'+str(args.weight_decay)+'_'+str(args.n_epochs)+'_'+str(args.g2v_pretrained)+'_'+str(args.seed)+'_ver'+str(args.dataset_ver) 

        model.load_state_dict(torch.load(model_path, map_location = args.device))

        self.model = model
        self.get_gex_idxs = get_gex_idxs
        self.device = device
        self.ppi_adj = ppi_adj
        self.args = args

    # def predict(self, test_list):
    def predict(self, ecfp, gex, dosage, duration):
        """
        @input
        test_list : a list of ecfp, gex, dosage, duration -> turned into torch dataloader inside this module
        ecfp : 2048-dim ECFP fingerprint, type = np.ndarray
        gex : 978-dim gene expression, type = np.ndarray
        dosage: type = np.float64
        duration : type = np.ndarray
        """
        # test_loader = DataLoader(dataset = test_list,
        #                 batch_size = 1,
        #                 shuffle = False)


        # inferred_list = []
        # for i, x in enumerate(test_loader):
        #     proba = self.model(x, self.ppi_adj, self.get_gex_idxs, self.device, self.args, None, False)
        #     proba = F.softmax(proba)
        #     inferred_list.append(proba)

        # return inferred_list
        x = [torch.tensor([float(x) for x in ecfp]).view(1, -1), 
            torch.tensor([float(x) for x in gex]).view(1, -1, 1), 
            torch.tensor(float(dosage)), 
            torch.tensor(int(duration))]

        # proba = self.model(x, self.ppi_adj, self.get_gex_idxs, self.device, self.args, None, False)
        proba = self.model.forward_serving(x, self.ppi_adj, self.get_gex_idxs, self.device, self.args, None, False)
        proba = F.softmax(proba)
        # print(proba)
        return proba
