# coding=gbk
import pandas as pd
import math

# N=250

term = []  # 诗的正文的集合
Lnum = {}  # 记录每首诗的字数

title = []  # 题目的集合

for k in range(1, 251):
    # 读文档得到诗
    with open("dataset/" + str(k) + '.txt', 'r') as f:
        l_num = 0
        s = f.read()
        index = 0
        for i in range(1, len(s)):
            if s[i] == '》':
                index = i + 1

        for m in range(1, index - 1):
            if (s[m] != '-') and (s[m] != ')') and (s[m] != '(') and (s[m] != ":") and (s[m] != '（') \
                    and (s[m] != '？') and (s[m] != ',') and (s[m] != "）"):
                title.append(s[m])

        for j in range(index, len(s)):
            if (s[j] != '，') and (s[j] != "。") and (s[j] != '！') and (s[j] != '？') and (s[j] != ','):
                #  防止标点符号干扰
                term.append(s[j])  # 加入term集
                l_num += 1  # 统计字数
        Lnum[k] = l_num
    f.close()

'''all_data = {"docid": Lnum.keys(), "length": Lnum.values()}
all_data_df = pd.DataFrame(all_data)
all_data_df.to_csv('num.csv', index=False)'''

# 通过set去重，得到所有term
term = list(set(term))
title = list(set(title))

d = {}  # 诗正文term的字典
post = {}  # term的post file

dt = {}  # 诗题目的字典
tpost = {}  # 题目的post file

title_term = []
title_df = []
title_cf = []
title_idf = []
title_post = []
# 构建题目倒排索引
for word in title:
    lst = [0, 0, 0]  # 存 doc_num 和 call_freq
    dic = {}  # 存 doc_id 和 term_freq
    for k in range(1, 251):
        with open("dataset/" + str(k) + '.txt', 'r') as f:
            s = f.read()
            index = 0
            for i in range(1, len(s)):
                if s[i] == '》':
                    index = i + 1
            flag = 0
            cnt = 0
            for i in range(1, index - 1):
                if s[i] == word:  # term在这首诗出现
                    flag = 1  # 标记
                    cnt += 1  # 总出现次数+1
            if flag == 1:
                lst[0] += 1  # 文档出现次数 +1

            lst[1] += cnt
            if cnt != 0:
                dic[k] = cnt
        f.close()

    lst[2] = math.log(250 / lst[0], 10)
    dt[word] = lst
    # dic = dict(sorted(dic.items(), key=lambda x: x[1],reverse=True))
    tpost[word] = dic
    
    title_term.append(word)
    title_cf.append(dt[word][1])
    title_df.append(dt[word][0])
    title_idf.append(dt[word][2])
    title_post.append(tpost[word])

all_data = {"title_term": title_term, "title_df": title_df, "title_cf": title_cf, "title_idf": title_idf}
data = {"title_term": title_term, "title_post": title_post}
all_data_df = pd.DataFrame(all_data)

all_data_df.to_csv('title_dict.csv', index=False)
data_df = pd.DataFrame(data)
data_df.to_csv('title_post_old.csv', index=False)

con_term = []
con_df = []
con_cf = []
con_idf = []
con_post = []
# 构建正文倒排索引
for word in term:
    lst = [0, 0, 0]  # 存 doc_num 和 call_freq
    dic = {}  # 存 doc_id 和 term_freq
    for k in range(1, 251):
        with open("dataset/" + str(k) + '.txt', 'r') as f:
            s = f.read()
            index = 0
            for i in range(1, len(s)):
                if s[i] == '》':
                    index = i + 1
            flag = 0
            cnt = 0
            for i in range(index, len(s)):
                if s[i] == word:  # term在这首诗出现
                    flag = 1  # 标记
                    cnt += 1  # 总出现次数+1
            if flag == 1:
                lst[0] += 1  # 文档出现次数 +1

            lst[1] += cnt
            if cnt != 0:
                dic[k] = cnt
        f.close()
    lst[2] = math.log(250 / lst[0], 10)
    d[word] = lst
    # dic = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    post[word] = dic
    con_term.append(word)
    con_idf.append(d[word][2])
    con_cf.append(d[word][1])
    con_df.append(d[word][0])
    con_post.append(post[word])

all_data = {"con_term": con_term, "con_df": con_df, "con_cf": con_cf, "con_idf": con_idf}
all_data_df = pd.DataFrame(all_data)
all_data_df.to_csv('con_dict.csv', index=False)

data = {"con_term": con_term, "con_post": con_post}
data_df = pd.DataFrame(data)
data_df.to_csv('con_post_old.csv', index=False)
