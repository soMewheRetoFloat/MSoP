import os
import sys

name = sys.argv[1]
assert name in ["shediao", "shendiao", "tianlong", 'feihu'], "Unidentified dataset name!"

links = {
    "shendiao": "/mnt/d/involuntary/works/missing-semester-of-python/232/jywxFenxi-master/神雕侠侣.txt",
    "shediao": "/mnt/d/involuntary/works/missing-semester-of-python/232/jywxFenxi-master/射雕英雄传.txt",
    "tianlong": "/mnt/d/involuntary/works/missing-semester-of-python/232/jywxFenxi-master/天龙八部.txt",
    "feihu": "/mnt/d/involuntary/works/missing-semester-of-python/232/jywxFenxi-master/飞狐外传.txt",
}

os.makedirs(name, exist_ok=True)
os.system(f"cp {links[name]} {os.path.join(name, 'input.txt')}")
