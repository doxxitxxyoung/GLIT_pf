#!/bin/bash

lr="1e-3"
wd="1e-5"
epoch=20

python main4.py \
    --model="GEX_PPI_GAT_cat7_MLP" \
    --learning_rate=$lr \
    --weight_decay=$wd \
    --n_epochs=$epoch
	
