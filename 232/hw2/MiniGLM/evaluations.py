# TODO: Implement metrics Perplexity, Rouge-L, etc.
import numpy as np
import torch
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import tiktoken

what_is = 'sft-256-384'

enc = tiktoken.get_encoding("gpt2")
out_dir = './analyze'
data_path_re = f'{what_is}/samples.txt'  # 这里输入模型回答和答案的文件路径
data_path_ans = 'analyze/answers.txt'
with open(data_path_re, 'r', encoding='utf-8') as f:
    dataset = f.readlines()

rouge_l_metrics = []

with open(data_path_ans, 'r', encoding='utf-8') as f:
    ans = f.readlines()

wdf = []

for i in range(len(dataset)):
    query = dataset[i]
    answer = ans[i]
    wdf.append({'q': query, 'a': answer})

for item in wdf:  # 遍历所有的标准答案和生成答案
    query_enc = enc.encode_ordinary(item['q'])
    ans_enc = enc.encode_ordinary(item['a'])
    # query_jieba = jieba.lcut(query)
    # ans_jieba = jieba.lcut(ans)

    queryx = query_enc
    ansx = ans_enc
    m, n = len(queryx), len(ansx)
    # 这个地方其实我在想是用jieba比较子序列还是用enc编码比较合适
    dp = [[0] * (n + 1) for _ in range(m + 1)]  # dp计算最长子序列
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if queryx[i - 1] == ansx[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    beta = 114514  # 这玩意只要大就行

    # 套公式时间
    R_lcs = lcs / m
    P_lcs = lcs / n
    F_lcs = ((1 + beta ** 2) * R_lcs * P_lcs) / (R_lcs + (beta ** 2) * P_lcs)
    rouge_l_metrics.append(F_lcs)

fig, ax = plt.subplots()
ax.bar([i + 1 for i in range(len(rouge_l_metrics))], rouge_l_metrics, width=0.7)
ax.set_xlabel('index')
ax.set_ylabel('rouge-l feature')
plt.xticks([i + 1 for i in range(len(rouge_l_metrics))], [i + 1 for i in range(len(rouge_l_metrics))])
plt.show()
fig.savefig(what_is + f'/rouge-l-{what_is}.png')
