import numpy as np
import matplotlib.pyplot as plt

# citysCoordinates: 储存城市二维坐标的矩阵
citysCoordinates = np.array([[25.0, 185.0], [345.0, 750.0], [525.0, 1000.0],
                        [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0],
                        [725.0, 370.0], [145.0, 665.0], [510.0, 875.0], [560.0, 365.0],
                        [520.0, 585.0], [480.0, 415.0], [975.0, 580.0], [1215.0, 245.0],
                        [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [420.0, 555.0],
                        [1150.0, 1160.0], [685.0, 595.0], [795.0, 645.0], [760.0, 650.0],
                        [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [555.0, 815.0],
                        [830.0, 485.0], [1170.0, 65.0]])

# get_distance_array: 得到城市间距的矩阵
def get_distance_array(coordinates):
    count = coordinates.shape[0] # count: 矩阵行数，即城市数
    distance = np.zeros((count, count)) # distance: 城市间距矩阵，count[i][j]表示城市i与城市j间距
    for i in range(count):
        for j in range(i, count):
            distance[i][j] = distance[j][i] = np.linalg.norm(coordinates[i] - coordinates[j])
    return distance

# distance_array: 储存城市间距矩阵
count = citysCoordinates.shape[0]
distance_array = get_distance_array(citysCoordinates)
# solution_initial: 初始路径，即顺序选择经过城市0, 1, 2 ... count-1的路径
solution_initial = np.arange(count)
# temperature_initial: 初始温度，可以不断调整选择合理温度
temperature_initial = 100
# alpha: 温度递减系数，temperature_new = 0.99 * temperature_old，可以不断调整选择合理系数
alpha = 0.99
# frequency_per_circulation: 内循环次数，即每个温度下的循环次数，可以不断调整选择合理次数
frequency_per_circulation = 1000

# 初始化循环变量
solution_current = solution_initial.copy() # 当前路径
solution_new = solution_current.copy() # 循环中新路径
temperature_current = temperature_initial # 当前温度
value = 999999 # 当前最优路径值，初始化为较大数

# 绘制初始图形
for i in range(count):
    plt.plot(citysCoordinates[i][0], citysCoordinates[i][1], 'ro') # 绘制所有点为红色
for i in range(count - 1):
    x = []
    y = []
    x.append(citysCoordinates[solution_current[i]][0])
    x.append(citysCoordinates[solution_current[i + 1]][0])
    y.append(citysCoordinates[solution_current[i]][1])
    y.append(citysCoordinates[solution_current[i + 1]][1])
    plt.plot(x, y, 'b') # 绘制路径为蓝色
x = []
y = []
x.append(citysCoordinates[solution_current[count - 1]][0])
x.append(citysCoordinates[solution_current[0]][0])
y.append(citysCoordinates[solution_current[count - 1]][1])
y.append(citysCoordinates[solution_current[0]][1])
plt.plot(x, y, 'b')
plt.pause(0.01) # 暂定0.01秒展示效果

# 进入循环，终止条件为当前温度小于等于1
while temperature_current > 1:
    for i in np.arange(frequency_per_circulation):
        # 产生两个不相等的随机数，用于交换路径中这两个城市的位置
        while True:
            loc1 = np.int(np.ceil(np.random.rand() * (count - 1)))
            loc2 = np.int(np.ceil(np.random.rand() * (count - 1)))
            if loc1 != loc2:
                break
        # 交换路径中城市loc1, loc2的位置
        solution_new[loc1], solution_new[loc2] = solution_new[loc2], solution_new[loc1]
        # 计算交换后的路径长度
        value_new = 0
        for j in range(count - 1):
            value_new += distance_array[solution_new[j]][solution_new[j + 1]]
        value_new += distance_array[solution_new[0]][solution_new[count - 1]]
        # 判断是否接受新路径长度
        if value_new < value: # 如果路径长度减小，接受新路径
            value = value_new
            solution_current = solution_new.copy()
        else: # 否则，有一定概率接受新路径
            if np.random.rand() < np.exp(-(value_new - value) / temperature_current):
                value = value_new
                solution_current = solution_new.copy()
            else: # 放弃新路径
                solution_new = solution_current.copy()
    temperature_current = alpha * temperature_current

    # 图形绘制
    plt.cla() # 清除上次绘制的图形
    for i in range(count):
        plt.plot(citysCoordinates[i][0], citysCoordinates[i][1], 'ro') # 绘制所有点为红色
    for i in range(count - 1):
        x = []
        y = []
        x.append(citysCoordinates[solution_current[i]][0])
        x.append(citysCoordinates[solution_current[i + 1]][0])
        y.append(citysCoordinates[solution_current[i]][1])
        y.append(citysCoordinates[solution_current[i + 1]][1])
        plt.plot(x, y, 'b') # 绘制路径为蓝色
    x = []
    y = []
    x.append(citysCoordinates[solution_current[count - 1]][0])
    x.append(citysCoordinates[solution_current[0]][0])
    y.append(citysCoordinates[solution_current[count - 1]][1])
    y.append(citysCoordinates[solution_current[0]][1])
    plt.plot(x, y, 'b')
    plt.pause(0.01) # 暂定0.01秒展示效果