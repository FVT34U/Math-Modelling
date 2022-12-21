import numpy as np
import plotly.graph_objs as go


class MatModModel:
    def __init__(self):
        self.fig = None
        self._mObservers = []

        self.dif_step = 1.0
        self.total_time = 1000
        self.gr_type = "Стандартные"
        self.ind_1 = 0
        self.ind_2 = 0
        self.number = [100, 200]
        self.up = [0.01, -0.01]
        self.matrix = [[0.0, -0.0001], [0.0001, 0.0]]

        self.n = int(self.total_time // self.dif_step)
        self.pops_num = len(self.number)
        self.new_number = np.copy(self.number)

        self.epidemic = True
        self.epidemic_chance = 0.01

    def get_value(self):
        """
        Возвращает значения для всех популяций на одном временном слое
        """
        res = []
        for i in range(0, self.pops_num):
            f = 0
            for j in range(0, self.pops_num):
                if i != j:
                    f += self.matrix[i][j] * self.new_number[i] * self.new_number[j]
            value = self.new_number[i] + (self.up[i] * self.new_number[i] + f) * self.dif_step
            #if value < 2:
                #value = 0
            res.append(value)

        """
        Код для эпидемии
        """
        if self.epidemic:
            if np.random.random() <= self.epidemic_chance:
                while(True):
                    index = np.random.default_rng().integers(self.pops_num, size=1)[0]
                    if bool(np.isclose(res, 0.0).all()):
                        break
                    if res[index] > 0.0:
                        res[index] /= 2.0
                        break
                print("EPIDEMIC!!!", index)

        self.new_number = np.copy(res)
        return res

    def graph(self):
        """
        Возвращает массив значений x и y, в каждом из которых содержатся массивы для всех популяций,
        в которых лежат значения для всех временных слоёв
        """
        a = np.linspace(0, self.total_time, self.n)
        y = []
        x = []
        res = [[], []]

        for i in range(0, self.n):
            y.append(self.get_value())
            x.append([a[i] for _ in range(0, self.pops_num)])

        for i in range(0, self.pops_num):
            res[0].append([])
            res[1].append([])

        for i in range(0, self.n):
            for j in range(0, self.pops_num):
                res[0][j].append(x[i][j])
                res[1][j].append(y[i][j])
        return res

    def phase_graph(self):
        res = []
        y = []
        x = []

        for i in range(0, self.n):
            val = self.get_value()
            y.append(val[self.ind_1])
            x.append(val[self.ind_2])

        res.append(x)
        res.append(y)
        res.append(np.linspace(0, self.total_time, self.n))

        return res

    def set_settings(self, dif_step, total_time, gr_type, ind_1, ind_2, number, up, matrix):
        self.dif_step = dif_step
        self.total_time = total_time
        self.gr_type = gr_type
        self.ind_1 = ind_1
        self.ind_2 = ind_2
        self.number = np.copy(number)
        self.up = np.copy(up)
        self.matrix = np.copy(matrix)

        self.n = int(self.total_time // self.dif_step)
        self.pops_num = len(self.number)
        self.new_number = np.copy(self.number)

        if self.gr_type == "Стандартные":
            self.make_figure(self.graph())
        if self.gr_type == "Фазовые кривые":
            self.make_figure_phase(self.phase_graph())

        self.notifyObservers()

    def make_figure_phase(self, _data):
        data = np.copy(_data)
        fg = go.Figure(data=[go.Scatter(x=data[0, :], y=data[1, :],
                                        mode='lines',
                                        line=dict(width=2),
                                        name='Значение'),
                             go.Scatter(x=data[0][:], y=data[1][:],
                                        mode='lines',
                                        line=dict(width=2),
                                        name='Значение')])

        fg.update_layout(title={"font": dict(size=20), "text": "Популяция"})

        steps = []
        frames = []

        for i in range(self.n):
            name = 'Особи: {}, Год: {}'.format(np.sum(data[:2, i]), data[2, i])
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
                    x=data[0, [i]],
                    y=data[1, [i]],
                    mode='markers',
                    marker=dict(size=20),
                    name='')
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

    def make_figure(self, _data):
        data = np.copy(_data)
        fg = go.Figure(data=[go.Scatter(x=data[0][i % self.pops_num, :], y=data[1][i % self.pops_num, :],
                                        mode='lines',
                                        line=dict(width=2),
                                        name='Популяция ' + str(i - self.pops_num)) for i in range(0, self.pops_num * 2)])

        fg.update_layout(title={"font": dict(size=20), "text": "Популяция"})

        steps = []
        frames = []

        for i in range(self.n):
            name = 'Особи: {}, Год: {}'.format(np.sum(data[1][:, i]), data[0][0, i])
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
                    x=data[0][k, [i]],
                    y=data[1][k, [i]],
                    mode='markers',
                    marker=dict(size=20),
                    name='') for k in range(0, self.pops_num)
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
