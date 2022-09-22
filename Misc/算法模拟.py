from math import sin, cos, pi 

def calc(func, x_s, x_t, freq, delta):
    x = x_s
    ans_sin = 0
    ans_cos = 0
    while x < x_t:
        ans_sin += func(x) * sin(2 * pi * freq * x) 
        ans_cos += func(x) * cos(2 * pi * freq * x)
        x += delta
    return (ans_cos * 2 / pi * delta, ans_sin * 2 / pi * delta)

TIME_DELTA = 1e-3

def solve(func, f_s, f_t, delta):
    f   = f_s
    lis = []
    while f < f_t:
        pair = calc(func, -pi, pi, f, TIME_DELTA)
        lis.append((pair[0] ** 2 + pair[1] ** 2) ** 0.5)
        f += delta
    return lis

import numpy as np

func = lambda x: (sin(x * 2) + cos(x * 2))/2

x = np.linspace(0, 2, 100)
y = np.linspace(0, 2, 100)
for i in range(len(x)):
    pair = calc(func, -pi, pi, x[i], TIME_DELTA)
    y[i] = (pair[0] ** 2 + pair[1] ** 2) ** 0.5

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y)
plt.show()
