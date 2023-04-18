import numpy as np
from PIL import Image
import colorsys
import random

grey = 0.25

def ind_to_col(ind, r):
    y,x = ind
    y,x = y/32, x/32
    col = np.array(colorsys.hsv_to_rgb((x+r)%1, 1 - y, 1 + y*(grey - 1)), dtype=float)
    col *= 256
    col[col>255] = 255
    col = col.astype(np.uint8)
    return col

img_arr = np.ndarray((32,32,3), dtype=np.uint8)


r = random.random()
print(r)

for ind in np.ndindex((32,32)):
    img_arr[ind] = ind_to_col(ind, r)

white = np.full((3,), int(grey*256) if grey < 1 else 255, dtype=np.uint8)
for n in range(32):
    for i in random.sample(range(32),k=n):
        img_arr[n,i] = white

def scale(A, B, k):
    Y = A.shape[0]
    X = A.shape[1]
    for y in range(0, k):
        for x in range(0, k):
            A[y:Y:k, x:X:k] = B

factor = 32

output = np.ndarray((32*factor,)*2+(3,),dtype=np.uint8)

scale(output, img_arr, factor)

Image.fromarray(output).save('img.png')
