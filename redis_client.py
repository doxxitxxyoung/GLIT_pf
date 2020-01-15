import redis
import numpy as np
#import struct
import pickle

#HOST = '0.0.0.0'
HOST = 'localhost'
PORT = 6379

client = redis.Redis(host = HOST, port = PORT)

# Fastest way to store numpy arrays?
# https://stackoverflow.com/questions/55311399/fastest-way-to-store-a-numpy-array-in-redis
# r == client()

#   Flush & initialize empty DB
#client.flushall()

#   Database Description
dbsize = client.dbsize()
print('DB size : '+str(dbsize))



#   Save 
#with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
with open('data/labeled_list_woAmbi_92742_70138.pkl', 'rb') as f:
    samples = pickle.load(f)
samples = samples[:10000]
"""
# 1. Using set / get
for i, x in enumerate(samples):
    ecfp = x[0]
    gex = x[1]
    dosage = x[2]
    duration = x[3]
    label = x[4]
    drugname = x[5]
    cellline = x[6]
    smiles = x[7]

    name = '_'.join([drugname, cellline])
    client.set(name+'_ecfp', ecfp.tostring())
    client.set(name+'_gex', gex.tostring())
    client.set(name+'_dosage', dosage)
    client.set(name+'_duration', int(duration))
    client.set(name+'_label', label)


    # Check 
    if i == 0:
        gex = client.get(name+'_gex')
        gex = np.frombuffer(gex, dtype = np.float64)
        print(gex)
        print(gex.shape)
"""

"""
# 2. Using hashes
for i, x in enumerate(samples):
    ecfp = x[0]
    gex = x[1]
    dosage = x[2]
    duration = x[3]
    label = x[4]
    drugname = x[5]
    cellline = x[6]
    smiles = x[7]

    name = '_'.join([drugname, cellline])
    client.hset(name, 'ecfp', ecfp.tostring())
    client.hset(name, 'gex', gex.tostring())
    client.hset(name, 'dosage', dosage)
    client.hset(name, 'duration', int(duration))
    client.hset(name, 'label', label)


    # Check 
    if i == 0:
        gex = client.hget(name, 'gex')
        gex = np.frombuffer(gex, dtype = np.float64)
        print(gex)
        print(gex.shape)

        print('length of '+name+' : ' + str(client.hlen(name)))
"""

# 3. Solely checking hset
for i, x in enumerate(samples):
    ecfp = x[0]
    gex = x[1]
    dosage = x[2]
    duration = x[3]
    label = x[4]
    drugname = x[5]
    cellline = x[6]
    smiles = x[7]
        
    name = '_'.join([drugname, cellline])
    if i == 0:
        """
        gex = client.hget(name, 'gex')
        gex = np.frombuffer(gex, dtype = np.float64)
        print(gex)
        print(gex.shape)
        """
#        print('ecfp: ', np.frombuffer(client.hget(name, 'ecfp')))
#        print('gex: ', np.frombuffer(client.hget(name, 'gex')))
        print('drugname & cellline: ', name)
        print('hkeys: ', client.hkeys(name))
        print('dosage: ', client.hget(name, 'dosage'))
        print('duration: ', client.hget(name, 'duration'))
#        print('smiles: ', client.hget(name, 'smiles'))
        print('label: ', client.hget(name, 'label'))





