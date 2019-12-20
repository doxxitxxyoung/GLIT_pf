import numpy as np
import pandas as pd
import pickle
import random

import networkx as nx
from scipy import sparse



def get_ppi_features(gene_info, args):

    symb2id_dict = {}
    id2symb_dict = {}
    id2order_dict = {}  #   gene id - index order dict
    order2id_dict = {}  #   gene id - index order dict
    for i, x in enumerate(gene_info.index):
        symb2id_dict[gene_info.loc[x, 'pr_gene_symbol']] = x
        id2symb_dict[x] = gene_info.loc[x, 'pr_gene_symbol']
        id2order_dict[x] = i
        order2id_dict[i] = x

    #   get gene2vec dict
    with open('data/gene2vec_dim_200_iter_9_dict.pkl', 'rb') as f:
        gene2vecdict = pickle.load(f)

    gene_info = gene_info.loc[[x for x in gene_info.index if id2symb_dict[x] in gene2vecdict.keys()]]

    #   get ppi/kegg pathway networkx

    if args.network_name == 'biogrid' :
        biogrid = pd.read_csv('data/BIOGRID-ALL-3.5.169.tab.graphonly.txt', 
                             delimiter = '\t')
        biogridppi = nx.Graph()
        genes = list(set(biogrid.iloc[:,2].values) & set(biogrid.iloc[:,3]))
        biogridppi.add_nodes_from(genes)
        for i, x  in enumerate(biogrid.index):
            biogridppi.add_edge(biogrid.iloc[i,2], biogrid.iloc[i,3])
        biogridppi.remove_node(np.nan)
        ppi_nx = biogridppi

    elif args.network_name == 'omnipath' : 
        with open('data/Omnipath_190806_nx_DiGraph.pkl', 'rb') as f:
            omnipath = pickle.load(f)

        #   Get weakly connected components
        wcc = list([x for x in nx.weakly_connected_components(omnipath)][0])
        omnipath = nx.subgraph(omnipath, wcc)

        ppi_nx = omnipath



    #   get common genes

    common_genes = set(gene_info.loc[:,'pr_gene_symbol'].values)&set(gene2vecdict.keys()) & set(ppi_nx.nodes)

    ppi_nx = nx.subgraph(ppi_nx, list(common_genes)).copy()

    common_symbols = [x for x in gene_info.loc[:, 'pr_gene_symbol'].values.tolist()\
                        if x in common_genes]

    #   remove isolated nodes
    ppi_nx = ppi_nx.subgraph(common_symbols).copy()
    isol_nodes = nx.isolates(ppi_nx)
    common_symbols = [x for x in common_symbols if x not in isol_nodes]

    #   sort gene ids into fixed order
    common_orders = np.sort([id2order_dict[symb2id_dict[x]] for x in common_symbols])

    common_ids = [order2id_dict[x] for x in common_orders]

    common_symbols = [id2symb_dict[x] for x in common_ids]

    ppi_nx = ppi_nx.subgraph(common_symbols)

    #   to undirected graph (for gcn)
    if args.undir_graph == True:
        ppi_nx = ppi_nx.to_undirected()

    ppi_adj = nx.to_numpy_matrix(ppi_nx, nodelist = common_symbols)

    g2v_embedding = np.vstack([gene2vecdict[x] for x in common_symbols])

    get_gex_idxs = common_orders

    #   get adj as COO row x col form
    ppi_adj = np.array([sparse.coo_matrix(ppi_adj).row, 
                        sparse.coo_matrix(ppi_adj).col])

    with open('ppi_'+args.gex_feat+'_feats.pkl', 'wb') as f:
        pickle.dump((ppi_adj, g2v_embedding, get_gex_idxs), f)

    args.num_genes = len(get_gex_idxs)

    print('num PPI extracted genes : '+str(args.num_genes))
        
    return gene2vecdict, gene_info, ppi_adj, ppi_nx, g2v_embedding, get_gex_idxs, args