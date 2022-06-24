# coding=gbk
import math

import pandas as pd

term = []
title = []
d = {}  # ʫ����term���ֵ�
post = {}  # term��post file

dt = {}  # ʫ��Ŀ���ֵ�
tpost = {}  # ��Ŀ��post file

Lum = {}
f = pd.read_csv("num.csv")
for i in range(0, 250):
    Lum[f.loc[i][0]] = f.loc[i][1]  # �����ĳ���

f = pd.read_csv("title_post_old.csv")
for i in range(0, 505):
    tpost[f.loc[i][0]] = eval(f.loc[i][1])

f = pd.read_csv('title_dict.csv')
for i in range(0, 505):
    lst = [0, 0, 0]
    lst[0] = f.loc[i][1]
    lst[1] = f.loc[i][2]
    lst[2] = f.loc[i][3]
    dt[f.loc[i][0]] = lst
    title.append(f.loc[i][0])

f = pd.read_csv("con_post_old.csv")
for i in range(0, 2365):
    post[f.loc[i][0]] = eval(f.loc[i][1])

f = pd.read_csv('con_dict.csv')
for i in range(0, 2365):
    lst = [0, 0, 0]
    lst[0] = f.loc[i][1]
    lst[1] = f.loc[i][2]
    lst[2] = f.loc[i][3]
    d[f.loc[i][0]] = lst
    term.append(f.loc[i][0])


# AND����,����Ϊ��
def AND(p1, p2, post, term):
    temp = []
    if p1 not in term or p2 not in term:
        return temp
    else:
        # �õ�p1��p2���ֵ�doc_id���б�
        post1 = list(post[p1].keys())
        post2 = list(post[p2].keys())
        temp1 = temp2 = 0
        p = []  # �洢��
        while temp1 < len(post1) and temp2 < len(post2):
            if temp1 == len(post1):
                return p
            elif temp2 == len(post2):
                return p
            elif post1[temp1] < post2[temp2]:
                temp1 += 1
            elif post1[temp1] == post2[temp2]:
                p.append(post1[temp1])
                temp1 += 1
                temp2 += 1
            else:
                temp2 += 1
        return p


# ����Ϊ�б��AND������Ϊʵ�ֶ���AND������
def AND_List(post1, post2, post):
    temp1 = temp2 = 0
    p = []
    while temp1 < len(post1) or temp2 < len(post2):
        if temp1 == len(post1):
            return p
        elif temp2 == len(post2):
            return p
        elif post1[temp1] < post2[temp2]:
            temp1 += 1
        elif post1[temp1] == post2[temp2]:
            p.append(post1[temp1])
            temp1 += 1
            temp2 += 1
        else:
            temp2 += 1
    # print(p)
    return p


# ����Ϊ�ֵ�OR����
def OR(p1, p2, post, term):
    temp = []
    if p1 not in term and p2 not in term:
        return temp
    elif p1 not in term:
        return post[p2]
    elif p2 not in term:
        return post[p1]
    else:
        post1 = list(post[p1].keys())
        # print(post1)
        post2 = list(post[p2].keys())
        # print(post2)
        temp1 = temp2 = 0
        p = []
        while temp1 < len(post1) and temp2 < len(post2):
            if post1[temp1] < post2[temp2]:
                p.append(post1[temp1])
                temp1 += 1
            elif post1[temp1] == post2[temp2]:
                p.append(post1[temp1])
                temp1 += 1
                temp2 += 1
            else:
                p.append(post2[temp2])
                temp2 += 1
        if temp1 == len(post1):
            while temp2 < len(post2):
                p.append(post2[temp2])
                temp2 += 1
        else:
            while temp1 < len(post1):
                p.append(post1[temp1])
                temp1 += 1
        # print(p)
        return p


# ����Ϊ�б��OR������Ϊʵ�ֶ���OR������
def OR_List(post1, post2, post):
    temp1 = temp2 = 0
    p = []
    while temp1 < len(post1) and temp2 < len(post2):
        if post1[temp1] < post2[temp2]:
            p.append(post1[temp1])
            temp1 += 1
        elif post1[temp1] == post2[temp2]:
            p.append(post1[temp1])
            temp1 += 1
            temp2 += 1
        else:
            p.append(post2[temp2])
            temp2 += 1
    if temp1 == len(post1):
        while temp2 < len(post2):
            p.append(post2[temp2])
            temp2 += 1
    else:
        while temp1 < len(post1):
            p.append(post1[temp1])
            temp1 += 1
    # print(p)
    return p


# AND_NOT������ʵ��p1 and_not p2
def AND_NOT(p1, p2, post, term):
    temp = []
    if p1 not in term:
        return temp
    else:
        post1 = list(post[p1].keys())
        post2 = AND(p1, p2, post, term)
        temp1 = temp2 = 0
        p = []
        while temp1 < len(post1) and temp2 < len(post2):
            if post1[temp1] < post2[temp2]:
                p.append(post1[temp1])
                temp1 += 1
            elif post1[temp1] == post2[temp2]:
                temp1 += 1
                temp2 += 1
            else:
                temp2 += 1
        if temp2 == len(post2):
            while temp1 < len(post1):
                p.append(post1[temp1])
                temp1 += 1

        # print(p)
        return p


# ����AND������Ϊ�ֵ��б�
def MULTI_AND(l1, post, term):
    temp = []
    for i in range(0, len(l1)):
        if l1[i] not in term:
            return temp

    # �洢�����ģ��֣���Ƶ��
    dict_sort = {}
    for i in range(0, len(l1)):
        dict_sort[l1[i]] = d[l1[i]][1]
    dict_sort = sorted(dict_sort.items(), key=lambda x: x[1])  # ����Ƶ��С��������
    post1 = list(post[dict_sort[0][0]])  # post1�洢�𰸣���ʼΪ��һ���ֵĳ����б�

    for j in range(1, len(dict_sort)):
        post2 = list(post[dict_sort[j][0]])
        # print(post2)
        post1 = AND_List(post1, post2, post)  # post2Ϊ��һ���ֵĳ����б���post1����AND��������ֵ��POST1
        # print(post1)
    return post1


# ����OR������Ϊ�ֵ��б�
def MULTI_OR(l1, post, term):
    dict_sort = {}
    temp = []
    err_count = 0
    for i in range(0, len(l1)):
        if l1[i] not in term:
            err_count += 1
        else:
            dict_sort[l1[i]] = d[l1[i]][1]
    if err_count == len(l1):
        return temp
    else:
        dict_sort = sorted(dict_sort.items(), key=lambda x: x[1], reverse=True)  # ����Ƶ�Ӵ�С����
        post1 = list(post[dict_sort[0][0]])  # post1�洢�𰸣���ʼΪ��һ���ֵĳ����б�

        for j in range(1, len(dict_sort)):
            post2 = list(post[dict_sort[j][0]])
            # print(post2)
            post1 = OR_List(post1, post2, post)  # post2Ϊ��һ���ֵĳ����б���post1����AND��������ֵ��POST1
            # print(post1)
        return post1


# ����OR������Ϊ�б��and_not����
def AND_NOT_List(post1, post2, post):
    temp1 = temp2 = 0
    p = []
    post2 = AND_List(post1, post2, post)
    while temp1 < len(post1) and temp2 < len(post2):
        if post1[temp1] < post2[temp2]:
            p.append(post1[temp1])
            temp1 += 1
        elif post1[temp1] == post2[temp2]:
            temp1 += 1
            temp2 += 1
        else:
            temp2 += 1
    if temp2 == len(post2):
        while temp1 < len(post1):
            p.append(post1[temp1])
            temp1 += 1
    return p


def Vectorq(str, post):
    sc = [0 for index in range(251)]  # ��ʼ��������
    for i in range(0, len(str)):
        t = str[i]
        temp = list(post[t].keys())
        cnt = 0
        for j in temp:
            sc[j] += d[t][2] * post[t][j]
    for k in range(1, 251):
        sc[k] = sc[k] / Lum[k]
    sc = sc / max(sc)
    return sc


# ���������ĺ���Ŀ��ѯ���б����÷֣�lst Ϊ���ĵõ��ķ�����l2Ϊ��Ŀ�����Ȩ�ؼ���0.1
def score(lst, l2):
    s = {}
    for i in range(1, len(lst)):
        if i in l2:
            s[i] = lst[i] + 0.5
        else:
            s[i] = lst[i]
    s = sorted(s.items(), key=lambda x: x[1], reverse=True)  # ���÷ֽ�������
    return s


# ��ӡ����������ʫ������
def display(l):
    cnt = 0
    for id in l:
        if cnt < 10:
            if id[1] != 0:
                with open("dataset/" + str(id[0]) + '.txt', 'r') as fi:
                    print(fi.read())
                    print("score: ", id[1])
                fi.close()
            cnt += 1
    print("���� ", cnt, " �����")


def search(str, post, term):
    s = str.split()
    length = len(s)
    if s[1] == "and":
        init = AND(s[0], s[2], post, term)
    elif s[1] == "or":
        init = OR(s[0], s[2], post, term)
    else:
        init = AND_NOT(s[0], s[2], post, term)
    if length == 3:
        return init
    else:
        for i in range(3, length, 2):
            if s[i] == "and":
                if s[i + 1] in term:  # �ֲ���term���У������and��initΪ�ռ�
                    init = AND_List(init, list(post[s[i + 1]].keys()), post)
                else:
                    init = []
            elif s[i] == "or":  # �����or����andnot��init���ı�
                if s[i + 1] in term:
                    init = OR_List(init, list(post[s[i + 1]].keys()), post)
            else:
                if s[i + 1] in term:
                    init = AND_NOT_List(init, list(post[s[i + 1]].keys()), post)
        return init


def old_score(l1, l2):
    temp = []
    for i in l1:
        temp.append(i)
    for j in l2:
        temp.append(j)
    ans = {}
    for id in temp:
        if id in l1 and id in l2:
            ans[id] = 0.3+0.7*20/Lum[id]
        elif id in l1 and id not in l2:
            ans[id] = 0.3
        elif id not in l1 and id in l2:
            ans[id] = 0.7*20/Lum[id]
        else:
            ans[id] = 0
    ans = sorted(ans.items(), key=lambda x: x[1], reverse=True)  # ����
    topk = ans[0:10]
    return topk


cs = sum(Lum.values()) / 250


def RSV(q):
    rsv = {}
    for k in range(1, 251):
        rsv[k] = 0  # ��ʼ��������
    for j in range(1, 251):
        for i in range(0, len(q)):
            temp = q[i]
            ls = list(post[temp].keys())                    # �õ��ʳ��ֵ��б�
            if j in ls:
                pi = 1 / 3 + 2 / 3 * d[temp][0] / 250       # 1/3+2/3(df/N)
                p = pi / (1 - pi)
                r = d[temp][2]                              # ri=df/N��log(1-ri/ri)������idf
                rsi = math.log(p, 10) + r
                fi = post[temp][j]                          # �����ڵ�jƪ�ĵ��ĳ��ִ���
                lj = Lum[j]                                 # ��jƪ�ĵ��ĳ���
                bij = 2 * fi / (0.25 + 0.75 * lj / cs + fi)  # BM25ģ�ͼ���
                rsi *= bij
                rsv[j] += rsi
    rsv = sorted(rsv.items(), key=lambda x: x[1], reverse=True)  # ���÷ֽ�������
    topk = rsv[0:10]
    for id in topk:
        with open("dataset/" + str(id[0]) + '.txt', 'r') as fi:
            print(str(id[0]))
            print(fi.read())
            print("score: " + str(id[1]))

    # print(rsv)

'''fi = post[temp][j]  # jƪ�ĵ��ĳ��ִ���
                lj = Lum[j]
                bij = 2 * fi / (0.25 + 0.75 * lj / cs + fi)  # BM25ģ�ͼ���
                rsi *= bij'''
def out_search(q1, q2):
    l1 = search(q1, tpost, title)
    l2 = search(q2, post, term)
    s = show(old_score(l1, l2))
    return s


def show(l):
    s = ""
    if len(l) == 0:
        s = "û�������ѯ����Ϣ"
    else:
        for id in l:
            with open("dataset/" + str(id[0]) + '.txt', 'r') as fi:
                s += str(id[0])
                s += fi.read() + '\n'
                s += "score: " + str(id[1]) + '\n'
            fi.close()
    return s


if __name__ == '__main__':
    while True:
        q1 = input("��ѯ���� >> ")
        # q2 = input("��ѯ��Ŀ >> ")
        '''out_search(q2, q1)'''
        # print(out_search(q2, q1))
        RSV(q1)
