import numpy as np
import plotly.graph_objs as go
import random
import math


class MatModModel:
    def __init__(self):
        self.fig = None
        self._mObservers = []

        self.total_time = 100
        self.lines_number = 3
        self.time_ratio = 0.1
        self.storage_capacity = 1
        self.duration_ratio = 0.1
        self.erlang_parameter = 1

    def set_settings(self, total_time, lines_number, time_ratio, storage_capacity, duration_ratio, erlang_parameter):
        self.total_time = total_time
        self.lines_number = lines_number
        self.time_ratio = time_ratio
        self.storage_capacity = storage_capacity
        self.duration_ratio = duration_ratio
        self.erlang_parameter = erlang_parameter

        a, b, c, d, e, f = self.calc()
        self.make_figure(a, b, c, d, e, f)

        self.notifyObservers()

    def get_amount_of_busy_line(self, matrix):
        free_lines = 0
        for i in range(matrix.shape[0]):
            if np.all(matrix[i][:] == 0):
                free_lines += 1
        return matrix.shape[0] - free_lines

    def distribution(self, t_array, d_array):
        if self.lines_number > 0 and len(t_array) > 1:
            rejection = 0
            amount = math.ceil(self.total_time / 0.1)
            matrix = np.zeros((self.lines_number, amount), dtype=float)  # строки - линии, столбцы - время
            for i in range(len(t_array)):
                end = t_array[i] + d_array[i]  # время окончания
                start_index = int(t_array[i] / 0.1)  # индекс, соответсвующий времени начала
                end_index = int(end / 0.1)  # индекс, соответсвующий времени окончания
                if end > self.total_time:
                    end_index = amount - 1

                if i == 0:  # для первого события
                    for j in range(start_index, end_index + 1):
                        matrix[0][j] += 1
                else:
                    idx = []  # все индексы события
                    for j in range(start_index, end_index + 1):
                        idx.append(j)
                    flag = False
                    for line in range(0, self.lines_number):  # сначала находим полностью свободную линию
                        if np.any(matrix[line][idx] != 0):
                            continue
                        else:
                            matrix[line][idx] += 1
                            flag = True
                            break
                    if not flag:  # ищем среди частично занятых
                        for line in range(0, self.lines_number):
                            if np.all(matrix[line][idx] < self.lines_number):
                                matrix[line][idx] += 1
                                flag = True
                                break
                    if not flag:
                        rejection += 1
            return matrix, rejection

    def calc(self):
        t = 0.0
        t_array, d_array = [], []

        while True:
            z = random.expovariate(self.time_ratio) / 3
            t += z
            if t > self.total_time:
                break
            t_array.append(t)  # массив моментов
            d_array.append(random.expovariate(self.duration_ratio))  # массив длительностей

        t_array = [a for index, a in enumerate(t_array) if index % self.erlang_parameter == 0]
        d_array = [a for index, a in enumerate(d_array) if index % self.erlang_parameter == 0]

        m, r = self.distribution(t_array, d_array)
        num = len(t_array)
        efficiency = 1 - r / num
        busy_lines = self.get_amount_of_busy_line(m)

        amount = math.ceil(self.total_time / 0.1)
        time_points = np.linspace(0, self.total_time, num=amount)
        graphs = []
        for i in range(0, m.shape[0]):
            graphs.append(np.array([i + 1 if j != 0 else None for j in m[i]]))
        return num, r, efficiency, busy_lines, time_points, graphs

    def make_figure(self, count, rej, eff, busy, x, y):
        fg = go.Figure(data=[go.Scatter(x=x, y=y[i % self.lines_number],
                                        mode='lines',
                                        line=dict(width=2),
                                        name='Значение') for i in range(0, self.lines_number * 2)])

        fg.update_layout(title={"font": dict(size=20), "text": "Популяция"})

        steps = []
        frames = []

        for i in range(self.total_time):
            name = 'Число вызовов: {}, Загруженные линии: {},' \
                   '\nОтклонённые вызовы: {}, Эффективность {}'.format(count, busy, rej, eff)

            step = dict(
                label=name,
                method="animate",
                args=[[name],
                      {"frame": {"duration": 1, "redraw": False},
                       "mode": "immediate",
                       "transition": {"duration": 1}}
                      ])
            steps.append(step)

            frame = dict(
                data=[go.Scatter(
                    x=x,
                    y=y[k][[i]],
                    mode='markers',
                    marker=dict(size=20),
                    name='') for k in range(0, self.lines_number)
                ],
                name=name
            )
            frames.append(frame)

        sliders = [dict(
            len=0.9,
            x=0.1,
            pad={"b": 10, "t": 50},
            transition={"duration": 1, "easing": "cubic-in-out"},
            steps=steps,
        )]

        fg.update_layout(updatemenus=[dict(type='buttons',
                                           buttons=[dict(label='Play',
                                                         method='animate',
                                                         args=[None, {"frame": {"duration": 1, "redraw": False},
                                                                      "mode": "immediate",
                                                                      "fromcurrent": True, "transition": {"duration": 1,
                                                                                                          "easing": "quadratic-in-out"}}]),
                                                    dict(label='Pause',
                                                         method='animate',
                                                         args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                                        "mode": "immediate",
                                                                        "transition": {"duration": 0}}]),
                                                    dict(label='Reset',
                                                         method='animate',
                                                         args=[None])])])

        fg.layout.sliders = sliders
        fg.frames = frames

        self.fig = fg

    def get_figure(self):
        return self.fig

    def addObserver(self, inObserver):
        self._mObservers.append(inObserver)

    def removeObserver(self, inObserver):
        self._mObservers.remove(inObserver)

    def notifyObservers(self):
        for x in self._mObservers:
            x.modelIsChanged()
