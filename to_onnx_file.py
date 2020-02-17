import io
import numpy as np
import pickle

import torch
from torch import nn
import torch.onnx

from model_serve_onnx import Model_serve

m = Model_serve()
torch_model = m.model
torch_model.eval()

#   Example input
with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
    sample = pickle.load(f)[0]
for i, x in enumerate(sample):
    print(type(x))
sample_x = sample[0]
ecfp = sample[0]
gex = sample[1]
dosage = sample[2]
duration = sample[3]
label = sample[4]
#x = [ecfp, gex, dosage, duration]

x = (torch.tensor([float(x) for x in ecfp]).view(1, -1),
     torch.tensor([float(x) for x in gex]).view(1, -1, 1)[:, torch_model.get_gex_idxs],
     torch.tensor(float(dosage)),
     torch.tensor(int(duration)))



torch.onnx.export(torch_model,
                x,  #   input
                "glit_serve.onnx",
                export_params = True,
#                do_constant_folding = True,
                input_names = ["ecfp", "gex", "dosage", "duration"],
                output_names = ["output"]
                )
                


                




