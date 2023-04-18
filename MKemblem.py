from random import randrange
import numpy as np

def shuffle(data):
    def swap(lst, i, j):
        lst[i], lst[j] = lst[j], lst[i]
    n = len(data)
    for i in range(n-1):
        r = randrange(i+1, n)
        swap(data, i, r)
    return data

def gen_grid(n):
    output = None

if __name__ == '__main__':
    a = np.array([0,1,2,3])
    print(a)
    print(shuffle(a))
    print(a)