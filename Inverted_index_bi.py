# coding=gbk
import pandas as pd

bi_term = []


def MD(i):  # 得到文档内容列表
    md = []
    with open("dataset/" + str(i) + '.txt', 'r') as f:
        s = f.read()  # 得到文档内容
        index = 0
        for i in range(1, len(s)):
            if s[i] == '》':
                index = i + 1
        for j in range(index, len(s)):
            if (s[j] != '，') and (s[j] != "。") and (s[j] != '！') and (s[j] != '？') and (s[j] != ','):
                #  防止标点符号干扰
                md.append(s[j])
    return md


for k in range(1, 251):
    # 读文档得到诗
    md = MD(k)
    for i in range(0, len(md) - 1):
        bi = md[i] + md[i + 1]
        bi_term.append(bi)

bi_term = list(set(bi_term))  # 得到bi-gram集合

d = {}  # 诗正文term的字典
post = {}  # term的post file
con_term = []
con_cf = []
con_post = []
for j in range(0, len(bi_term)):
    word = bi_term[j]
    cnt = 0  # 存 call_freq
    dic = {}  # 存 doc_id 和 term_freq
    for k in range(1, 251):
        md = MD(k)
        s = ""
        for m in md:
            s += m
        a = s.count(word)  # 统计该篇文档出现词的数量
        cnt += a
        if a != 0:
            dic[k] = a
    d[word] = cnt
    post[word] = dic
    con_term.append(word)
    con_cf.append(d[word])
    con_post.append(post[word])

all_data = {"con_term": con_term, "con_cf": con_cf, "con_post": con_post}
all_data_df = pd.DataFrame(all_data)
all_data_df.to_csv('con_dict_bi.csv', index=False)


