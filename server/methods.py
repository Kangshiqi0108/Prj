import pandas as pd
import numpy as np
from collections import Counter
from sko.GA import GA
from sko.operators import crossover, mutation, ranking, selection

data = {}
criterions = {}
def calculate_entropy(probabilities):
    # 过滤掉概率为 0 的元素
    non_zero_probs = [p for p in probabilities if p > 0]
    # 计算熵
    entropy = -np.sum([p * np.log2(p) for p in non_zero_probs])
    return entropy
def func1(index:list,attribute:str):
    if attribute == "gender":
        female = 0
        male = 0
        for i in index:
            if data[i][attribute] == 0:
                female += 1
            else:
                male += 1
        probabilities = [female/len(index),male/len(index)]
        entropy = calculate_entropy(probabilities)
        return (entropy/np.log2(2))*100
    elif attribute == "style":
        type1=0
        type2=0
        type3=0
        for i in index:
            if data[i][attribute] == 1:
                type1 += 1
            elif data[i][attribute] == 2:
                type2 += 1
            else:
                type3 += 1
        counts = [type1,type2,type3]
        length = len(index)
        probabilities = [count / length for count in counts]
        entropy = calculate_entropy(probabilities)
        return (entropy/np.log2(3))*100
    else:
        list_of_capability = [data[i][attribute] for i in index]
        #mean = np.mean(list_of_capability)
        counts = Counter(list_of_capability)
        length = len(index)
        probabilities = [count / length for count in counts]
        entropy = calculate_entropy(probabilities)
        return (entropy/np.log2(10))*100

def get_ranks(lst):
    sorted_lst = sorted(lst)
    ranks = []
    for value in lst:

        rank = sorted_lst.index(value) + 1
        ranks.append(rank)
    return ranks


   
def aim_func(index:list):
    index = get_ranks(index)
    group_size = 5
    group_score=[]
    start = 0
    end = start+group_size
    total_importance = sum([criterions[i]["importance"] for i in criterions])
    while start<len(data):
        score = 0
        groupIndex = index[start:end]
        start+=group_size
        end = start+group_size
        if criterions["gender"]["group_type"] == "Homogeneous":
            score+=(100-func1(groupIndex,"gender"))*criterions["gender"]["importance"]/total_importance
        elif criterions["gender"]["group_type"] == "Heterogeneous":
            score+=(func1(groupIndex,"gender"))*criterions["gender"]["importance"]/total_importance
        if criterions["style"]["group_type"] == "Homogeneous":
            score+=(100-func1(groupIndex,"style"))*criterions["style"]["importance"]/total_importance
        elif criterions["style"]["group_type"] == "Heterogeneous":
            score+=(func1(groupIndex,"style"))*criterions["style"]["importance"]/total_importance
        if criterions["capability"]["group_type"] == "Homogeneous":
            score+=(100-func1(groupIndex,"capability"))*criterions["capability"]["importance"]/total_importance
        elif criterions["capability"]["group_type"] == "Heterogeneous":
            score+=(func1(groupIndex,"capability"))*criterions["capability"]["importance"]/total_importance
        group_score.append(score)
        
    average_score = np.mean(group_score)
    vars = np.var(group_score)
    return 1/(vars+average_score+1e-7)
    
def grouping1(learners:dict,cri:dict)->dict:
    global data, criterions
    data = learners
    criterions = cri
    ga = GA(func=aim_func, n_dim=len(data), size_pop=10, max_iter=10, lb=[1]*len(data), ub=[100]*len(data), precision=1e-7)
    ga.register(operator_name="crossover",operator=crossover.crossover_pmx)
    
    best_x, best_y = ga.run()
    best_x = get_ranks(best_x)
    res = {}
    for i in range(0,len(data),5):
        res[(i//5)+1] = best_x[i:i+5]
    return res

"""
测试数据：
learners_map = {
    1: {
        "id": 1,
        "name": "Alice",
        "capability": 3,
        "gender": 0,
        "style": 2
    },
    2: {
        "id": 2,
        "name": "Bob",
        "capability": 7,
        "gender": 1,
        "style": 1
    },
    3: {
        "id": 3,
        "name": "Charlie",
        "capability": 5,
        "gender": 1,
        "style": 3
    },
    4: {
        "id": 4,
        "name": "David",
        "capability": 2,
        "gender": 1,
        "style": 2
    },
    5: {
        "id": 5,
        "name": "Eve",
        "capability": 9,
        "gender": 0,
        "style": 1
    },
    6: {
        "id": 6,
        "name": "Frank",
        "capability": 4,
        "gender": 1,
        "style": 3
    },
    7: {
        "id": 7,
        "name": "Grace",
        "capability": 6,
        "gender": 0,
        "style": 2
    },
    8: {
        "id": 8,
        "name": "Heidi",
        "capability": 8,
        "gender": 0,
        "style": 1
    },
    9: {
        "id": 9,
        "name": "Ivan",
        "capability": 1,
        "gender": 1,
        "style": 3
    },
    10: {
        "id": 10,
        "name": "Judy",
        "capability": 5,
        "gender": 0,
        "style": 2
    },
    11: {
        "id": 11,
        "name": "Kevin",
        "capability": 7,
        "gender": 1,
        "style": 1
    },
    12: {
        "id": 12,
        "name": "Luna",
        "capability": 3,
        "gender": 0,
        "style": 3
    },
    13: {
        "id": 13,
        "name": "Mike",
        "capability": 6,
        "gender": 1,
        "style": 2
    },
    14: {
        "id": 14,
        "name": "Nora",
        "capability": 2,
        "gender": 0,
        "style": 1
    },
    15: {
        "id": 15,
        "name": "Oscar",
        "capability": 9,
        "gender": 1,
        "style": 3
    },
    16: {
        "id": 16,
        "name": "Penny",
        "capability": 4,
        "gender": 0,
        "style": 2
    },
    17: {
        "id": 17,
        "name": "Quinn",
        "capability": 8,
        "gender": 0,
        "style": 1
    },
    18: {
        "id": 18,
        "name": "Ray",
        "capability": 1,
        "gender": 1,
        "style": 3
    },
    19: {
        "id": 19,
        "name": "Sara",
        "capability": 5,
        "gender": 0,
        "style": 2
    },
    20: {
        "id": 20,
        "name": "Tom",
        "capability": 7,
        "gender": 1,
        "style": 1
    },
    21: {
        "id": 21,
        "name": "Ursula",
        "capability": 3,
        "gender": 0,
        "style": 3
    },
    22: {
        "id": 22,
        "name": "Victor",
        "capability": 6,
        "gender": 1,
        "style": 2
    },
    23: {
        "id": 23,
        "name": "Wendy",
        "capability": 2,
        "gender": 0,
        "style": 1
    },
    24: {
        "id": 24,
        "name": "Xavier",
        "capability": 9,
        "gender": 1,
        "style": 3
    },
    25: {
        "id": 25,
        "name": "Yvonne",
        "capability": 4,
        "gender": 0,
        "style": 2
    },
    26: {
        "id": 26,
        "name": "Zach",
        "capability": 8,
        "gender": 1,
        "style": 1
    },
    27: {
        "id": 27,
        "name": "Amelia",
        "capability": 1,
        "gender": 0,
        "style": 3
    },
    28: {
        "id": 28,
        "name": "Benjamin",
        "capability": 5,
        "gender": 1,
        "style": 2
    },
    29: {
        "id": 29,
        "name": "Cora",
        "capability": 7,
        "gender": 0,
        "style": 1
    },
    30: {
        "id": 30,
        "name": "Daniel",
        "capability": 3,
        "gender": 1,
        "style": 3
    },
    31: {
        "id": 31,
        "name": "Elena",
        "capability": 6,
        "gender": 0,
        "style": 2
    },
    32: {
        "id": 32,
        "name": "Finn",
        "capability": 2,
        "gender": 1,
        "style": 1
    },
    33: {
        "id": 33,
        "name": "Gabriella",
        "capability": 9,
        "gender": 0,
        "style": 3
    },
    34: {
        "id": 34,
        "name": "Henry",
        "capability": 4,
        "gender": 1,
        "style": 2
    },
    35: {
        "id": 35,
        "name": "Isabella",
        "capability": 8,
        "gender": 0,
        "style": 1
    },
    36: {
        "id": 36,
        "name": "Jack",
        "capability": 1,
        "gender": 1,
        "style": 3
    },
    37: {
        "id": 37,
        "name": "Kylie",
        "capability": 5,
        "gender": 0,
        "style": 2
    },
    38: {
        "id": 38,
        "name": "Liam",
        "capability": 7,
        "gender": 1,
        "style": 1
    },
    39: {
        "id": 39,
        "name": "Mia",
        "capability": 3,
        "gender": 0,
        "style": 3
    },
    40: {
        "id": 40,
        "name": "Noah",
        "capability": 6,
        "gender": 1,
        "style": 2
    },
    41: {
        "id": 41,
        "name": "Olivia",
        "capability": 2,
        "gender": 0,
        "style": 1
    },
    42: {
        "id": 42,
        "name": "Peter",
        "capability": 9,
        "gender": 1,
        "style": 3
    },
    43: {
        "id": 43,
        "name": "Quinn",
        "capability": 4,
        "gender": 0,
        "style": 2
    },
    44: {
        "id": 44,
        "name": "Ryan",
        "capability": 8,
        "gender": 1,
        "style": 1
    },
    45: {
        "id": 45,
        "name": "Sophia",
        "capability": 1,
        "gender": 0,
        "style": 3
    },
    46: {
        "id": 46,
        "name": "Tyler",
        "capability": 5,
        "gender": 1,
        "style": 2
    },
    47: {
        "id": 47,
        "name": "Victoria",
        "capability": 7,
        "gender": 0,
        "style": 1
    },
    48: {
        "id": 48,
        "name": "William",
        "capability": 3,
        "gender": 1,
        "style": 3
    },
    49: {
        "id": 49,
        "name": "Xena",
        "capability": 6,
        "gender": 0,
        "style": 2
    },
    50: {
        "id": 50,
        "name": "Yuri",
        "capability": 2,
        "gender": 1,
        "style": 1
    }
}
criterion={
    "capability":{
        "importance":5,
        "group_type":"Homogeneous"
    },
    "gender":{
        "importance":2,
        "group_type":"Homogeneous"
    },
    "style":{
        "importance":8,
        "group_type":"Heterogeneous"
    }
    
}
"""   