with open('sft_data_t.jsonl', 'r', encoding='utf-8') as f:
    x = f.readlines()
    y = []
    for item in x:
        item = item.rstrip('\n')
        item = item.rstrip(',')
        y.append(item)

with open('sft_data_t.jsonl', 'w', encoding='utf-8') as f:
    for item in y:
        f.write(item + '\n')
