# TODO: prepare SFT data similar to `prepare.py`
import os
import json
import random
import sys
import tiktoken
import numpy as np
import torch

enc = tiktoken.get_encoding("gpt2")

item_len = 256

def pingjie(lhs, rhs):
    st = str(lhs + r";" + rhs)
    st = enc.encode_ordinary(st)
    return st + [enc.eot_token]


data_all = []

data_path = 'D:\\involuntary\\works\\missing-semester-of-python\\232\\hw2\\datasets\\sft_data.jsonl'
with open(data_path, 'r', encoding='utf-8') as f:  # jsonl文件导入为多个字符串
    file_content = f.readlines()
    for item in file_content:
        data_all.append(item.rstrip('\n'))

data_all_formed = []
for item in data_all:
    item = item.split('"')
    dic_x = {'Question': item[3], 'Answer': item[7]}
    data_all_formed.append(dic_x)
random.shuffle(data_all_formed)
# data_all_formed中的变量都是问答对，字典形式储存
train, val = [], []
for index in range(len(data_all_formed)):
    # print(data_all_formed[index])
    if index % 10 != 7:
        train.append(data_all_formed[index])
    else:
        val.append(data_all_formed[index])

train = [pingjie(dic['Question'], dic['Answer']) for dic in train]
val = [pingjie(dic['Question'], dic['Answer']) for dic in val]

train_ids, val_ids = [], []  # 直接把问题全部拼接起来
for item in train:
    if len(item) < item_len:
        item += ([220] * (item_len - len(item)))
    else:
        item = item[:item_len - 1] + [enc.eot_token]
    train_ids += item
for item in val:
    if len(item) < item_len:
        item += ([220] * (item_len - len(item)))
    else:
        item = item[:item_len - 1] + [enc.eot_token]
    val_ids += item

train_ids = np.array(train_ids).astype(np.int16)

long_long_train = []
tex = 0
for index in range(len(train_ids)):
    if train_ids[index] == enc.eot_token:
        tex = 0
    long_long_train.append(tex)
    if train_ids[index] == 26:
        tex = 1
long_long_train = np.array(long_long_train).astype(np.int16)

val_ids = np.array(val_ids).astype(np.int16)
long_long_val = []
tex = 0
for index in range(len(val_ids)):
    if val_ids[index] == 28:
        tex = 0
    long_long_val.append(tex)
    if val_ids[index] == 26:
        tex = 1
long_long_val = np.array(long_long_val).astype(np.int16)
# # save numpy array to file [name]/train.bin and [name]/val.bin
train_ids.tofile(os.path.join(".\\processed_pretrain_sft", "train.bin"))
val_ids.tofile(os.path.join(".\\processed_pretrain_sft", 'val.bin'))
long_long_train.tofile(os.path.join(".\\processed_pretrain_sft", "long_long_train.bin"))
long_long_val.tofile(os.path.join(".\\processed_pretrain_sft", "long_long_val.bin"))