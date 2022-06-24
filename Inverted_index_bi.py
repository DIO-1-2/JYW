# coding=gbk
import pandas as pd

bi_term = []


def MD(i):  # �õ��ĵ������б�
    md = []
    with open("dataset/" + str(i) + '.txt', 'r') as f:
        s = f.read()  # �õ��ĵ�����
        index = 0
        for i in range(1, len(s)):
            if s[i] == '��':
                index = i + 1
        for j in range(index, len(s)):
            if (s[j] != '��') and (s[j] != "��") and (s[j] != '��') and (s[j] != '��') and (s[j] != ','):
                #  ��ֹ�����Ÿ���
                md.append(s[j])
    return md


for k in range(1, 251):
    # ���ĵ��õ�ʫ
    md = MD(k)
    for i in range(0, len(md) - 1):
        bi = md[i] + md[i + 1]
        bi_term.append(bi)

bi_term = list(set(bi_term))  # �õ�bi-gram����

d = {}  # ʫ����term���ֵ�
post = {}  # term��post file
con_term = []
con_cf = []
con_post = []
for j in range(0, len(bi_term)):
    word = bi_term[j]
    cnt = 0  # �� call_freq
    dic = {}  # �� doc_id �� term_freq
    for k in range(1, 251):
        md = MD(k)
        s = ""
        for m in md:
            s += m
        a = s.count(word)  # ͳ�Ƹ�ƪ�ĵ����ִʵ�����
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


