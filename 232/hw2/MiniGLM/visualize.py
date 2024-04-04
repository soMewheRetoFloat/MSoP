### TODO: add your import
import matplotlib.pyplot as plt
import numpy as np


def visualize_loss(train_loss_list, train_interval, val_loss_list, val_interval, dataset, out_dir):
    fig, ax = plt.subplots()
    ax.plot([(i + 1) * train_interval for i in range(len(train_loss_list))], train_loss_list, label='train loss')
    ax.plot([i * val_interval for i in range(len(val_loss_list))], val_loss_list, label='val loss')
    ax.set_xlabel('epoch')
    ax.set_ylabel('loss')
    ax.set_title('Loss on ' + dataset)
    ax.legend()
    fig.savefig(out_dir + '/loss.png')
    plt.close(fig)
