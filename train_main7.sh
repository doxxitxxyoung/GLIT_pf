#!/bin/bash

lrs="5e-4 1e-4 5e-5 1e-5"
wds="1e-5 1e-7"
epoch=20
device='cuda:0'
gcn_dim="32"
num_gcn_hops="4"


for hop in $num_gcn_hops
do
    for gcn_d in $gcn_dim
    do
        for lr in $lrs
        do
            for wd in $wds
            do
                python main4.py \
                    --model="GEX_PPI_SAGE_cat4_MLP" \
                    --learning_rate=$lr \
                    --weight_decay=$wd \
                    --n_epochs=$epoch \
                    --gcn_hidden_dim1=$gcn_d \
                    --num_gcn_hops=$hop \
                    --device=$device
            done
        done
    done
done
	
