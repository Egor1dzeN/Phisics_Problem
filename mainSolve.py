import math

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

k1, k2 = 7, 7
l = 3
m = 5
x_0 = 1
y_0 = 1
vx_ = 0.2
vy_ = 0
list_delta_l_left = []
list_delta_l_right = []
sol = None


def funcAx(x, y):
    global k1, k2, l, m
    len_left = math.sqrt((l + x) ** 2 + y ** 2)

    sum1 = -k1 * (len_left - l) * (l + x) / len_left

    len_right = math.sqrt((l - x) ** 2 + y ** 2)
    # print(len_right)
    sum2 = +k2 * (len_right - l) * (l - x) / len_right
    list_delta_l_left.append(abs(len_left - l))
    list_delta_l_right.append(abs(len_right - l))
    # print(sum2)
    return (sum1 + sum2) / m


def funcBy(x, y):
    global k1, k2, l, m
    len_left = math.sqrt((l + x) ** 2 + y ** 2)
    # print(len_left)
    sum1 = -k1 * (len_left - l) * y / len_left
    # print(sum1)
    len_right = math.sqrt((l - x) ** 2 + y ** 2)
    # print(len_right)
    sum2 = k2 * (len_right - l) * y / len_right
    # print(sum2)
    # print(sum1 + sum2)
    return (sum1 + sum2) / m


i = 0


def system(t, z):
    x1, x2, y1, y2 = z
    dx1_dt = x2
    dx2_dt = funcAx(x1, y1)
    dy1_dt = y2
    dy2_dt = funcBy(x1, y1)
    global i
    i += 1
    # print(i)
    return [dx1_dt, dx2_dt, dy1_dt, dy2_dt]


def solveDiffEq():
    x0 = [x_0, vx_]  # x(0) = 1, x'(0) = 0
    y0 = [y_0, vy_]  # y(0) = 1, y'(0) = 0
    z0 = x0 + y0
    # print('x0 = ', x0, 'y = ', y0)
    t_span = (0, 200)
    t_eval = np.linspace(t_span[0], t_span[1], (t_span[1] - t_span[0]) * 100)
    # print(t_eval, len(t_eval))
    # Решение системы ОДУ
    sol1 = solve_ivp(system, t_span, z0, t_eval=t_eval)
    # sol = sol1
    # print('x = ',sol.y[0][0])
    # print('y = ', sol.y[2][0])
    # print(sol1)
    return sol1


def potential_energy():
    sol1 = solveDiffEq()
    arr = []
    for i in range(len(sol1.y[0])):
        delta_l_left = abs(math.sqrt((l + sol1.y[0][i]) ** 2 + sol1.y[2][i] ** 2) - l) ** 2
        arr.append(k1 * delta_l_left / 2)
    return arr


def cinetic_energu():
    sol1 = solveDiffEq()
    arr_pot = potential_energy()
    arr = [0] * len(arr_pot)
    arr[0] = 0
    '''
    for i in range(1, len(sol.y[0])):
        delta_x = sol.y[0][i] - sol.y[0][i - 1]
        delta_y = sol.y[2][i] - sol.y[2][i - 1]
        delta_v = (math.sqrt(delta_x ** 2 + delta_y ** 2) / 0.01) ** 2
        arr.append(m * delta_v / 2)
    arr.append(6)
    '''
    for i in range(1, len(arr_pot)):
        arr[i] = arr[i-1] + (arr_pot[i-1] - arr_pot[i])
    return arr


sol = solveDiffEq()
