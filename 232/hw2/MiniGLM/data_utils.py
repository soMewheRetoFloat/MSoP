import os

import torch
import numpy as np

train_data = None
val_data = None
long_long_train = None
long_long_val = None

def init_data_pretrain(dataset):
    global train_data, val_data

    data_dir = os.path.join('data', dataset)
    train_data = np.memmap(os.path.join(data_dir, 'train.bin'), dtype=np.uint16, mode='r')
    val_data = np.memmap(os.path.join(data_dir, 'val.bin'), dtype=np.uint16, mode='r')


def init_data_sft(dataset):
    global train_data, val_data, long_long_train, long_long_val
    data_dir = os.path.join('data', dataset)
    train_data = np.memmap(os.path.join(data_dir, 'train.bin'), dtype=np.uint16, mode='r')
    val_data = np.memmap(os.path.join(data_dir, 'val.bin'), dtype=np.uint16, mode='r')
    long_long_train = np.memmap(os.path.join(data_dir, 'long_long_train.bin'), dtype=np.uint16, mode='r')
    long_long_val = np.memmap(os.path.join(data_dir, 'long_long_val.bin'), dtype=np.uint16, mode='r')

def get_batch_pretrain(split, batch_size, block_size, device):
    global train_data, val_data
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([torch.from_numpy((data[i:i + block_size]).astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy((data[i + 1:i + 1 + block_size]).astype(np.int64)) for i in ix])
    loss_mask = torch.ones_like(x, dtype=torch.float64)

    device_type = 'cuda' if 'cuda' in device else 'cpu'
    if device_type == 'cuda':
        # pin arrays x,y, which allows us to move them to GPU asynchronously (non_blocking=True)
        x, y, loss_mask = x.pin_memory().to(device, non_blocking=True), y.pin_memory().to(device,
                                                                                          non_blocking=True), loss_mask.pin_memory().to(
            device, non_blocking=True)
    else:
        x, y, loss_mask = x.to(device), y.to(device), loss_mask.to(device)
    return x, y, loss_mask


def get_batch_sft(split, batch_size, block_size, device):
    global train_data, val_data, long_long_train, long_long_val
    data = train_data if split == 'train' else val_data
    long_long = long_long_train if split == 'train' else long_long_val
    questions = len(data) / 256
    # long_long = []
    # tex = 0
    # for index in range(len(data)):
    #     if data[index] == 28:
    #         tex = 0
    #     long_long.append(tex)
    #     if data[index] == 26:
    #         tex = 1
    # long_long = np.array(long_long)
    ix = torch.randint(int(questions - 1), (batch_size,))
    # print(ix)
    ix = torch.tensor([i * 256 for i in ix])
    l_list = torch.stack([torch.from_numpy((long_long[i:i + block_size]).astype(np.int64)) for i in ix])
    x = torch.stack([torch.from_numpy((data[i:i + block_size]).astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy((data[i + 1:i + 1 + block_size]).astype(np.int64)) for i in ix])
    loss_mask = l_list
    # for index in range(l_list.shape[0]):
    #     loss_mask[index][l_list[index] == 1] = 1

    device_type = 'cuda' if 'cuda' in device else 'cpu'
    if device_type == 'cuda':
        # pin arrays x,y, which allows us to move them to GPU asynchronously (non_blocking=True)
        x, y, loss_mask = x.pin_memory().to(device, non_blocking=True), y.pin_memory().to(device,
                                                                                          non_blocking=True), loss_mask.pin_memory().to(
            device, non_blocking=True)
    else:
        x, y, loss_mask = x.to(device), y.to(device), loss_mask.to(device)
    return x, y, loss_mask
