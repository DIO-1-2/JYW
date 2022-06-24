# coding=gbk
import pandas as pd

term = []
title = []
d = {}  # ʫ����term���ֵ�
post = {}  # term��post file

Lnum = {}
f = pd.read_csv("num.csv")
for i in range(0, 250):
    Lnum[f.loc[i][0]] = f.loc[i][1]  # �����ĳ���

f = pd.read_csv("con_post.csv")
for i in range(0, 2365):
    post[f.loc[i][0]] = eval(f.loc[i][1])

f = pd.read_csv('con_dict.csv')
for i in range(0, 2365):
    lst = [0, 0, 0]
    lst[0] = f.loc[i][1]  # df
    lst[1] = f.loc[i][2]  # cf
    lst[2] = f.loc[i][3]  # idf
    d[f.loc[i][0]] = lst
    term.append(f.loc[i][0])

bi = {}
post_bi = {}
bi_term = []
f = pd.read_csv('con_dict_bi.csv')
for i in range(0, 14560):
    bi[f.loc[i][0]] = f.loc[i][1]  # cf
    post_bi[f.loc[i][0]] = eval(f.loc[i][2])
    bi_term.append(f.loc[i][0])

cs = sum(Lnum.values())  # ���ݼ�������term������


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


def conditional_p(a, b, j):  # �����jƪ����������term����������
    r = 0.8
    if a in term:
        a_cf = d[a][1]  # a�������ĵ��ĳ��ִ���
        ls = list(post[a].keys())
        bt = a + b
        if bt in bi_term:
            bi_cf = bi[bt]  # ab�������ĵ��ĳ��ִ���
            ls = list(post_bi[bt].keys())  # ab��j�ĵ����ֵĴ���
            if j in ls:
                bi_j = post_bi[bt][j]
            else:
                bi_j = 0
        else:
            bi_cf = 0
            bi_j = 0
        if j in ls:
            a_j = post[a][j]  # a��j�ĵ����ֵĴ���
            p1 = r * bi_j / a_j + (1 - r) * (bi_cf + 1) / (a_cf + 2365)  # ���ʽ����
        else:
            p1 = (1 - r) * (bi_cf + 1) / (a_cf + 2365)
    else:
        p1 = (1 - r) * 1 / 2365
    return p1


# ��Ȫ  ����  ����  ����  ����  ��ɽ
def MLE_uni(s, post, r):
    sc = {}
    for k in range(1, 251):
        sc[k] = 1  # ��ʼ��������
    for i in range(1, 251):
        md = MD(i)
        for j in range(0, len(s)):
            temp = s[j]
            if temp in term:
                if s[j] in md:
                    sc[i] *= (r * post[temp][i] / Lnum[i]) + (1 - r) * (d[temp][1] / cs)  # tf/����
                else:
                    sc[i] *= (1 - r) * (d[temp][1] / cs)
            else:
                sc[i] *= (1 - r) * (1 / (cs + 2365))  # ��ѯ���в���term������
    sc = sorted(sc.items(), key=lambda x: x[1], reverse=True)  # ����
    topk = sc[0:10]
    return topk


def MLE_bi(s, post, r):
    sc = {}
    for k in range(1, 251):
        sc[k] = 1  # ��ʼ��������
    for i in range(1, 251):
        md = MD(i)
        temp = s[0]
        if s[0] in term:
            if s[0] in md:  # �����һ��term
                pa = (r * post[temp][i] / Lnum[i]) + (1 - r) * (d[temp][1] / cs)
                sc[i] *= pa  # tf/����
            else:
                pa = (1 - r) * (d[temp][1] / cs)
                sc[i] *= pa
        else:
            sc[i] *= (1 - r) * (1 / (cs + 2365))

        for j in range(1, len(s)):  # ����ʣ�µ�term����Ҫʹ����������
            p_con = conditional_p(s[j - 1], s[j], i)
            sc[i] *= p_con
    sc = sorted(sc.items(), key=lambda x: x[1], reverse=True)  # ����
    topk = sc[0:10]
    return topk


def dis(l):
    s = ""
    for id in l:
        if id[1] != 0:
            with open("dataset/" + str(id[0]) + '.txt', 'r') as fi:
                s += str(id[0]) + '\n'
                s += fi.read() + '\n'
                s += "score: " + str(id[1]) + '\n'
        fi.close()
    return s
