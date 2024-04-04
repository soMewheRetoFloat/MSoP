import numpy as np
import os

import tiktoken
import numpy as np
import torch

enc = tiktoken.get_encoding("gpt2")

# print(enc.encode_ordinary(';'))
#
# train_data = np.memmap(os.path.join('.\\processed_pretrain_sft', 'train.bin'), dtype=np.uint16, mode='r')
# val_data = np.memmap(os.path.join('.\\processed_pretrain_sft', 'val.bin'), dtype=np.uint16, mode='r')
#
# print(len(val_data))
# print(val_data)
# cal = []
# slow = 0
# for fast in range(len(val_data)):
#     if val_data[fast] == 91:
#         cal.append(val_data[slow:fast + 1])
#         slow = fast + 1
# print(cal)

# long_long = []
# tex = 0
# for index in range(len(val_data)):
#     if val_data[index] == 28:
#         tex = 0
#     long_long.append(tex)
#     # print(long_long)
#     if val_data[index] == 2:
#         tex = 1
#
# long_long = torch.tensor(long_long)
# print(torch.zeros_like(long_long).dtype)
# print(len(val_data))
# print(type(val_data))
# print(len(long_long))


# def get_batch_sft(split, batch_size=32, block_size=256):
#     global train_data, val_data
#     data = train_data if split == 'train' else val_data
#     long_long = []
#     tex = 0
#     for index in range(len(data)):
#         if data[index] == 28:
#             tex = 0
#         long_long.append(tex)
#         if data[index] == 2:
#             tex = 1
#
#     long_long = np.array(long_long)
#     ix = torch.randint(len(data) - block_size, (batch_size,))
#     l_list = torch.stack([torch.from_numpy((long_long[i:i + block_size]).astype(np.int64)) for i in ix])
#     x = torch.stack([torch.from_numpy((data[i:i + block_size]).astype(np.int64)) for i in ix])
#     y = torch.stack([torch.from_numpy((data[i + 1:i + 1 + block_size]).astype(np.int64)) for i in ix])
#     loss_mask = torch.zeros_like(x)
#     print(l_list.shape)
#     print(loss_mask.shape)
#     for index in range(l_list.shape[0]):
#         loss_mask[index][l_list[index] == 1] = 1
#     print(l_list[4])
#     print(loss_mask[4])


# xxx = []
# for item in cal[2]:
#     if item != -1:
#         xxx.append(item)
#
# xxx = enc.decode_bytes(xxx)
# print(bytes.decode(xxx))
# for index in range(len(xxx)):
#     byte_string += xxx[index]
#
# print(byte_string)
