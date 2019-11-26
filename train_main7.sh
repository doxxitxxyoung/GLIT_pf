#!/bin/bash

lr="1e-4"
wd="1e-5"
epoch=10
device='cuda:0'

python main4.py \
    --model="GEX_PPI_GCN_cat4_MLP" \
    --learning_rate=$lr \
    --weight_decay=$wd \
    --n_epochs=$epoch \
    --device=$device
	
