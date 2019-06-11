import random
import time
from neighborpy.engine import Engine
# from datas import example1
import numpy as np

DIM = 128
dname = 'test'
engine = Engine(dim=DIM)
engine.create_db(dname)
POINTS = 100_000

reader = open('data.txt', 'r')
fx1 = list(map(float, reader.readline().rstrip('\n').strip('[').strip(']').split(',')))
fx2 = list(map(float, reader.readline().rstrip('\n').strip('[').strip(']').split(',')))

dot = round(random.uniform(0.3, 0.7),3)

key = random.randint(0, POINTS)

matrix = {}
for i in range(POINTS):
    if i == key:
        matrix['k_' + str(i)] = np.array(fx1)
    else:
        v = np.random.randn(DIM)
        matrix['k_' + str(i)] = v

c1 = time.clock()
engine.add_items(dname, vs=matrix)
c2 = time.clock()
print('add %d items clock: %0.6f' % (POINTS, (c2 - c1)))
# c1 = time.clock()
# for i in range(0, 5):
#     p = int(POINTS*round(random.uniform(0.01, 0.99),3))
#     rk = 'k_' + str(p)
#     engine.delete_item(dname, rk)
#     print('delete %s' % rk)
# c2 = time.clock()
#
# print('delete item clock: %0.6f' % (c2 - c1))
times = 100
c1 = time.clock()
for i in range(0, times):
    ind = engine.query_item(dname, np.array(fx2), 10)
c2 = time.clock()

print('query, clock: %0.6f' % ((c2 - c1)/times))

print('key: K_%s, result: %s' % (key, ind))

# dic = {}
# dic2 = {'key':'t1', 'val':'v1'}
# dic['t1'] = np.array([[1,2,3],[2,3,4,],[3,4,5]])
# dic['t2'] = np.array([[4,5,6],[5,6,7]])
# dic['t3'] = np.array([[6,7,8]])
#
# dic3 = np.append(dic['t1'], dic['t2'], axis=0)
#
# data = [[1,2,3,4],[4,5,6,7,8]]
# #dic['data'] = data
# dic['dic'] = dic2
# print(dic)
# dic7 = np.array(data)
# print(dic7)
# l2 = {
#     'key': 123,
#     'Value': 231
# }
# l3 = []
#
# try:
#     print(l2['ttt'])
# except BaseException as err:
#     print(err)
# print(dic3)
# print(np.size(dic3, 0))
# print(np.random.randn(128))

# matrix = np.ones((100000, 128))
# start = time.clock()
# tree = BallTree(matrix, leaf_size=2000)
# end = time.clock()
# print('build tree, clock %0.6f' % (end - start))
# example1()
