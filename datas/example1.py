import random
import time
import pickle
import scipy
import struct
import redis
from sklearn import datasets
from sklearn.datasets.samples_generator import make_classification
import numpy as np
from sklearn.neighbors import BallTree, NearestNeighbors


def print_results(results):
    print('  Data \t| Distance')
    for r in results:
        data = r[1]
        dist = r[2]
        print('  {} \t| {:.4f}'.format(data, dist))


def distance(x, y):
    """
    Computes distance measure between vectors x and y. Returns float.
    """

    if scipy.sparse.issparse(x):
        x = x.toarray().ravel()
        y = y.toarray().ravel()
    return 1.0 - np.dot(x, y)


def toRedis(r, arr, redis_key):
    """Store given Numpy array 'a' in Redis under key 'n'"""
    h, w = arr.shape
    shape = struct.pack('>II', h, w)
    encoded = shape + arr.tobytes()
    lenth = len(encoded)
    # Store encoded data in Redis
    # r.set(redis_key, encoded)
    f = open(redis_key, 'wb')
    f.write(encoded)
    f.flush()
    f.close()
    return


def fromRedis(r, redis_key):
    """Retrieve Numpy array from Redis key 'n'"""
    # encoded = r.get(redis_key)
    f = open(redis_key, 'rb')
    encoded = f.read()
    f.close()
    l = len(encoded)
    h, w = struct.unpack('>II', encoded[:8])
    a = np.frombuffer(encoded, dtype=np.float64, offset=8).reshape(h, w)
    return a

def example1():
    # Dimension of feature space
    DIM = 128

    # Number of data points (dont do too much because of exact search)
    POINTS = 300000

    reader = open('data.txt', 'r')
    fx1 = list(map(float, reader.readline().rstrip('\n').strip('[').strip(']').split(',')))
    fx2 = list(map(float, reader.readline().rstrip('\n').strip('[').strip(']').split(',')))

    print(BallTree.valid_metrics)
    print('careate random vectors')

    dot = 0.25

    key = int(POINTS * dot + random.randint(1, POINTS * (1 - dot)))

    matrix = np.zeros((1, DIM))
    # arr = np.array([])
    matrix = np.append(matrix, [np.array(fx1)], axis=0)
    matrix = np.zeros((POINTS, DIM))
    for i in range(POINTS):
        if i == key:
            matrix[i, :] = np.array(fx1)
        else:
            v = np.random.randn(DIM)
            matrix[i, :] = v

    r = redis.Redis(host='localhost', port=6379, db=0)
    rkey = 'matrix.data'

    # start = time.clock()
    # toRedis(r, matrix, rkey)
    # end = time.clock()
    # print('save datas, clock %0.6f' % (end - start))

    start = time.clock()
    matrix = fromRedis(r, rkey)
    end = time.clock()
    print('load datas, clock %0.6f' % (end - start))
    # nn = NearestNeighbors(algorithm='brute')
    # nn.fit(matrix)
    # start = time.clock()
    # dist, ind = nn.kneighbors([np.array(fx2)], n_neighbors=1)
    # end = time.clock()
    # print('key: %s, clock %0.6f, result: %s' % (key,(end - start), ind))

    print('build tree')
    start = time.clock()
    tree = BallTree(matrix, leaf_size=500, metric='minkowski')
    end = time.clock()
    print('build complated\npoints: %s\nbuild clock: %0.2f s\nkey: %s' % (POINTS, (end - start), str(key)))

    # Get random query vector
    query = np.random.randn(DIM)
    query2 = matrix[376:377]
    times = 300
    start = time.clock()
    for i in range(times):
        dist, ind = tree.query([np.array(fx2)], k=1)
    end = time.clock()

    print('query times: %d, execution clock: %0.2f ms/per\nresult: %s' % (times, (end - start) / times * 1000, ind[0]))
