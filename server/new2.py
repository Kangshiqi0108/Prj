import pandas as pd

# 定义 learners_map 字典
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

# 将字典转换为 DataFrame
data = []
for key, value in learners_map.items():
    data.append(value)
df = pd.DataFrame(data)

# 指定 Excel 文件的路径
file_path = 'learners_data.xlsx'

# 将 DataFrame 保存为 Excel 文件
df.to_excel(file_path, index=False)

print(f"数据已成功保存到 {file_path}")