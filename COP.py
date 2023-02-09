from random import random
from random import randint
from math import sqrt
from math import exp
from copy import deepcopy
import matplotlib.pyplot as plt

a2b = [] # 容纳列表
aLen = 0 # A的元素个数
bLen = 0 # B的元素个数
A = [] # 列表A
B = [] # 列表B

temperature = 0 # 模拟退火标准参数：温度
T_min = exp(-5)  # 模拟退火标准参数：结束温度
ALPHA = 0.98  # 模拟退火标准参数：温度衰减系数

def Read():
    global a2b, A, B, aLen, bLen
    fp = open("input.txt", 'r') # 打开文件
    file = list(fp) # 列表化
    file = [line.strip().split(',') for line in file] # 文件处理
    file = [[float(x) for x in line] for line in file] # 文件处理
    aLen = int(file[0][0]) # 得到A长度
    bLen = int(file[2][0]) # 得到B长度
    A = file[1][:] # 得到A
    B = file[3][:] # 得到B
    a2b = [[] for i in range(aLen)] # 初始化容纳列表
    fp.close() # 关闭文件


def Generatea2b():
    global a2b
    i = 0 # B下标
    while (i < bLen):
        for j in range(aLen): # A下标
            if (sum(a2b[j]) + B[i]) <= A[j]: # 如果已经用于生产的j工料加上生产B[i]所需的工料少于或等于j工料的总数
                a2b[j].append(B[i]) # 将生产B[i]所需工料加入已经用于生产的j工料列表
                i += 1 # 继续遍历
                break


def Generatetemprature():
    global temperature
    temperature = sum(B) # 初始化温度为所有产品总和


def Output():
    global a2b
    file = open("output.txt", 'w') # 以读的方式创建文件
    for b in B: # 对于B中每个元素
        for i in range(aLen): # 对于工料i
            if b in a2b[i]: # 如果该元素在工料i的列表中
                a2b[i].remove(b) # 先将b移出
                file.write("%.1f,%d,%.1f\n" % (b, i, A[i])) # 按规定格式写入文件
                break
    file.close() # 关闭文件


def Generatestatus(a2b):
    i = randint(0, aLen - 1) # 随机选择一个工料i
    while (a2b[i] == []): # 如果工料i的列表为空
        i = randint(0, aLen - 1) # 继续选择i
    temp = a2b[i].pop(randint(0, len(a2b[i]) - 1)) # 随机从工料i的列表中选择一个产品
    j = randint(0, aLen - 1) # 随机选择另一个工料j
    while ((sum(a2b[j]) + temp) > A[j]): # 如果将该产品放入工料j的列表超过工料j的大小
        j = randint(0, aLen - 1) # 继续选择j
    a2b[j].append(temp) # 将该产品加入工料j的列表


def Effect(a2b):
    sum = 0 # 初始化总和
    for i in range(aLen): # 进行遍历
        if a2b[i] != []: # 如果工料已经被使用
            sum += A[i] # 总和加上整个工料i的大小
    return sum # 返回总和


def Accept(a2bnew):
    global a2b
    ds = Effect(a2bnew) - Effect(a2b) # 计算新状态与旧状态的效用差
    if ds <= 0: # 如果新状态效用小
        a2b = a2bnew # 接受新状态
    else: # 否则
        if (exp(-ds / temperature) > random()): # 以模拟退火规定的概率
            a2b = a2bnew # 接受新状态

Read() # 读取输入文件
Generatea2b() # 初始化容纳列表
Generatetemprature() # 初始化温度
effect = [] # 记录效用值
x = [] # x轴
n = 1 # x坐标
while (temperature > T_min): # 当温度大于最小值时
    for i in range(bLen):
        a2bnew = deepcopy(a2b) # 拷贝当前状态到新状态
        Generatestatus(a2bnew) # 产生新状态
        Accept(a2bnew) # 是否接受新状态函数
    print("%.1f" % Effect(a2b))
    x.append(n) # x轴添加坐标
    effect.append(Effect(a2b)) # 添加效用值
    n += 1 # 更新x坐标
    temperature = temperature * ALPHA # 更新温度
Output() # 输出
plt.plot(x, effect) # 画图
plt.show()