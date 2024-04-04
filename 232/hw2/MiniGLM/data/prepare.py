import os
import sys
import tiktoken
import numpy as np

enc = tiktoken.get_encoding("gpt2")

names = sys.argv[1:]

data_all = []

# TODO: read data from ([name]/input.txt for name in names)

for name in names:
    with open(f'./{name}/input.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
        data_formed = []
        for item in data:
            item = item.strip()
            if not item.startswith('\n'):
                items = item.split('　　')  # 每个段都分出来
                for x in items:
                    data_formed.append(x)
        data_all.append(data_formed[:-1])

# data_all中的变量都是二维list，每个list代表一本书，其中一个自然段又是一个一维list
# TODO: combine multiple books into one single data file
data_to_be = []  # 直接塞入所有自然段得了
for article in data_all:
    for passage in article:
        data_to_be.append(passage)  # 直接塞入自然段

# TODO: split data for train(0.9) and valid (0.1)
train_data, val_data = [], []

for idx in range(len(data_to_be)):
    print(data_to_be[idx])
    if idx % 10 != 9:
        train_data.append(data_to_be[idx])
    else:
        val_data.append(data_to_be[idx])
# TODO: tokenize raw data with tiktoken encoder
train_data = [enc.encode_ordinary(item) for item in train_data]

val_data = [enc.encode_ordinary(item) for item in val_data]

# TODO: transform to numpy array
train_ids, val_ids = [], []
for item in train_data:
    train_ids += item
for item in val_data:
    val_ids += item
train_ids = np.array(train_ids).astype(np.int16)
print(len(train_ids))
val_ids = np.array(val_ids).astype(np.int16)
# save numpy array to file [name]/train.bin and [name]/val.bin
train_ids.tofile(os.path.join(".\\processed_pretrain", "train.bin"))
val_ids.tofile(os.path.join(".\\processed_pretrain", 'val.bin'))
