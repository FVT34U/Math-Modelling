import numpy as np
import plotly.graph_objs as go


class MatModModel:
    def __init__(self, m=None, x=None, y=None, v_x=None, v_y=None, G=None, total_time=None, step=None):
        if m is None:
            m = [1.2166e+30, ]
        if y is None:
            y = [0, ]
        if v_x is None:
            v_x = [0, ]
        if v_y is None:
            v_y = [0, ]
        if total_time is None:
            total_time = 0
        if step is None:
            step = 1
        if G is None:
            G = 6.67e-11

        self._mObservers = []

        self.mass = np.copy(m)
        self.x = np.copy(x)
        self.y = np.copy(y)
        self.v_x = np.copy(v_x)
        self.v_y = np.copy(v_y)
        self.total_time = total_time
        self.time_step = step
        self.n = total_time // step

        self.G_const = G

        self.scheme = ''

        self.fig = None

    def euler_scheme(self):
        """
        Функция расчета координат планет по схеме Эйлера
        Входные данные берутся из класса
        :return: двумерные массивы координат (в массиве данные для всех планет на всех временных слоях),
        массивы скорости звезды на всех временных слоях
        """
        xs = np.zeros((len(self.mass), self.n))
        ys = np.zeros((len(self.mass), self.n))
        vxsc = np.zeros(self.n)
        vysc = np.zeros(self.n)
        vxs = np.copy(self.v_x)
        vys = np.copy(self.v_y)
        print(xs.shape, ys.shape)
        xs[:, 0] = np.copy(self.x)
        ys[:, 0] = np.copy(self.y)

        for i in range(1, self.n):
            rnx = np.copy(xs[1:, i - 1])
            rny = np.copy(ys[1:, i - 1])
            rnx -= xs[0, i - 1]
            rny -= ys[0, i - 1]
            forces_x = self.G_const * self.mass[0] * self.mass[1:] * rnx / (rnx * rnx + rny * rny) ** 1.5
            forces_y = self.G_const * self.mass[0] * self.mass[1:] * rny / (rnx * rnx + rny * rny) ** 1.5
            a_nx = -forces_x / self.mass[1:]
            a_ny = -forces_y / self.mass[1:]
            a_nxs = np.sum(forces_x) / self.mass[0]
            a_nys = np.sum(forces_y) / self.mass[0]
            xs[:, i] = xs[:, i - 1] + vxs * self.time_step
            ys[:, i] = ys[:, i - 1] + vys * self.time_step
            vxs[1:] = vxs[1:] + a_nx * self.time_step
            vxs[0] = vxs[0] + a_nxs * self.time_step
            vxsc[i] = vxs[0]
            vys[1:] = vys[1:] + a_ny * self.time_step
            vys[0] = vys[0] + a_nys * self.time_step
            vysc[i] = vxs[0]
        return xs, ys, vxsc, vysc

    def euler_kramer_scheme(self):
        """
        Функция расчета координат планет по схеме Эйлера-Крамера
        Входные данные берутся из класса
        :return: двумерные массивы координат (в массиве данные для всех планет на всех временных слоях),
        массивы скорости звезды на всех временных слоях
        """
        xs = np.zeros((len(self.mass), self.n))
        ys = np.zeros((len(self.mass), self.n))
        vxsc = np.zeros(self.n)
        vysc = np.zeros(self.n)
        vxs = np.copy(self.v_x)
        vys = np.copy(self.v_y)
        xs[:, 0] = np.copy(self.x)
        ys[:, 0] = np.copy(self.y)

        for i in range(1, self.n):
            rnx = np.copy(xs[1:, i - 1])
            rny = np.copy(ys[1:, i - 1])
            rnx -= xs[0, i - 1]
            rny -= ys[0, i - 1]
            forces_x = self.G_const * self.mass[0] * self.mass[1:] * rnx / (rnx * rnx + rny * rny) ** 1.5
            forces_y = self.G_const * self.mass[0] * self.mass[1:] * rny / (rnx * rnx + rny * rny) ** 1.5
            a_nx = -forces_x / self.mass[1:]
            a_ny = -forces_y / self.mass[1:]
            a_nxs = np.sum(forces_x) / self.mass[0]
            a_nys = np.sum(forces_y) / self.mass[0]
            vxs[1:] = vxs[1:] + a_nx * self.time_step
            vxs[0] = vxs[0] + a_nxs * self.time_step
            vxsc[i] = vxs[0]
            vys[1:] = vys[1:] + a_ny * self.time_step
            vys[0] = vys[0] + a_nys * self.time_step
            vysc[i] = vxs[0]
            xs[:, i] = xs[:, i - 1] + vxs * self.time_step
            ys[:, i] = ys[:, i - 1] + vys * self.time_step
        return xs, ys, vxsc, vysc

    def verlet_scheme(self):
        """
        Функция расчета координат планет по схеме Верле
        Входные данные берутся из класса
        :return: двумерные массивы координат (в массиве данные для всех планет на всех временных слоях),
        массивы скорости звезды на всех временных слоях
        """
        xs = np.zeros((len(self.mass), self.n))
        ys = np.zeros((len(self.mass), self.n))
        vxsc = np.zeros(self.n)
        vysc = np.zeros(self.n)
        vxs = np.copy(self.v_x)
        vys = np.copy(self.v_y)
        xs[:, 0] = np.copy(self.x)
        ys[:, 0] = np.copy(self.y)

        for i in range(1, self.n):
            rnx = np.copy(xs[1:, i - 1])
            rny = np.copy(ys[1:, i - 1])
            rnx -= xs[0, i - 1]
            rny -= ys[0, i - 1]
            forces_x = self.G_const * self.mass[0] * self.mass[1:] * rnx / (rnx * rnx + rny * rny) ** 1.5
            forces_y = self.G_const * self.mass[0] * self.mass[1:] * rny / (rnx * rnx + rny * rny) ** 1.5
            a_nx = np.zeros(len(self.mass))
            a_ny = np.zeros(len(self.mass))
            a_nx[1:] = -forces_x / self.mass[1:]
            a_ny[1:] = -forces_y / self.mass[1:]
            a_nx[0] = np.sum(forces_x) / self.mass[0]
            a_ny[0] = np.sum(forces_y) / self.mass[0]
            if i == 1:
                xs[:, i] = xs[:, i - 1] + vxs * self.time_step
                ys[:, i] = ys[:, i - 1] + vys * self.time_step
                vxs = vxs + a_nx * self.time_step
                vxsc[i] = vxs[0]
                vys = vys + a_ny * self.time_step
                vysc[i] = vxs[0]
            else:
                xs[:, i] = 2 * xs[:, i - 1] - xs[:, i - 2] + a_nx * self.time_step ** 2
                ys[:, i] = 2 * ys[:, i - 1] - ys[:, i - 2] + a_ny * self.time_step ** 2
                vxs -= vxs
                vxs += (xs[:, i] - xs[:, i - 2]) / 2 / self.time_step
                vxsc[i] = vxs[0]
                vys -= vys
                vys += (ys[:, i] - ys[:, i - 2]) / 2 / self.time_step
                vysc[i] = vys[0]
        return xs, ys, vxsc, vysc

    def beeman_scheme(self):
        """
        Функция расчета координат планет по схеме Бимана
        Входные данные берутся из класса
        :return: двумерные массивы координат (в массиве данные для всех планет на всех временных слоях),
        массивы скорости звезды на всех временных слоях
        """
        xs = np.zeros((len(self.mass), self.n))
        ys = np.zeros((len(self.mass), self.n))
        vxsc = np.zeros(self.n)
        vysc = np.zeros(self.n)
        vxs = np.copy(self.v_x)
        vys = np.copy(self.v_y)
        xs[:, 0] = np.copy(self.x)
        ys[:, 0] = np.copy(self.y)
        a_nx_prev = np.zeros(len(self.mass))
        a_ny_prev = np.zeros(len(self.mass))
        a_nx_next = np.zeros(len(self.mass))
        a_ny_next = np.zeros(len(self.mass))

        for i in range(1, self.n):
            rnx = np.copy(xs[1:, i - 1])
            rny = np.copy(ys[1:, i - 1])
            rnx -= xs[0, i - 1]
            rny -= ys[0, i - 1]
            forces_x = self.G_const * self.mass[0] * self.mass[1:] * rnx / (rnx * rnx + rny * rny) ** 1.5
            forces_y = self.G_const * self.mass[0] * self.mass[1:] * rny / (rnx * rnx + rny * rny) ** 1.5
            a_nx = np.zeros(len(self.mass))
            a_ny = np.zeros(len(self.mass))
            a_nx[1:] = -forces_x / self.mass[1:]
            a_ny[1:] = -forces_y / self.mass[1:]
            a_nx[0] = np.sum(forces_x) / self.mass[0]
            a_ny[0] = np.sum(forces_y) / self.mass[0]
            xs[:, i] = xs[:, i - 1] + vxs * self.time_step - (4 * a_nx - a_nx_prev) / 6 * self.time_step ** 2
            ys[:, i] = ys[:, i - 1] + vys * self.time_step - (4 * a_ny - a_ny_prev) / 6 * self.time_step ** 2
            rnx = np.copy(xs[1:, i])
            rny = np.copy(ys[1:, i])
            rnx -= xs[0, i]
            rny -= ys[0, i]
            forces_x = self.G_const * self.mass[0] * self.mass[1:] * rnx / (rnx * rnx + rny * rny) ** 1.5
            forces_y = self.G_const * self.mass[0] * self.mass[1:] * rny / (rnx * rnx + rny * rny) ** 1.5
            a_nx_next[1:] = -forces_x / self.mass[1:]
            a_ny_next[1:] = -forces_y / self.mass[1:]
            a_nx_next[0] = np.sum(forces_x) / self.mass[0]
            a_ny_next[0] = np.sum(forces_y) / self.mass[0]
            vxs = vxs + (2 * a_nx_next + 5 * a_nx - a_nx_prev) / 6 * self.time_step
            vxsc[i] = vxs[0]
            vys = vys + (2 * a_ny_next + 5 * a_ny - a_ny_prev) / 6 * self.time_step
            vysc[i] = vxs[0]
            a_nx_prev = np.copy(a_nx)
            a_ny_prev = np.copy(a_ny)
        return xs, ys, vxsc, vysc

    def runge_kutta_scheme(self):
        """
        Функция расчета координат планет по схеме Эйлера
        Входные данные берутся из класса
        :return: двумерные массивы координат (в массиве данные для всех планет на всех временных слоях),
        массивы скорости звезды на всех временных слоях
        """
        xs = np.zeros((len(self.mass), self.n))
        ys = np.zeros((len(self.mass), self.n))
        vxsc = np.zeros(self.n)
        vysc = np.zeros(self.n)
        vxs = np.copy(self.v_x)
        vys = np.copy(self.v_y)
        xs[:, 0] = np.copy(self.x)
        ys[:, 0] = np.copy(self.y)

        for i in range(1, self.n):
            rnx = np.copy(xs[1:, i - 1])
            rny = np.copy(ys[1:, i - 1])
            rnx -= xs[0, i - 1]
            rny -= ys[0, i - 1]
            forces_x = self.G_const * self.mass[0] * self.mass[1:] * rnx / (rnx * rnx + rny * rny) ** 1.5
            forces_y = self.G_const * self.mass[0] * self.mass[1:] * rny / (rnx * rnx + rny * rny) ** 1.5
            a_nx = -forces_x / self.mass[1:]
            a_ny = -forces_y / self.mass[1:]
            a_nxs = np.sum(forces_x) / self.mass[0]
            a_nys = np.sum(forces_y) / self.mass[0]
            asx = np.concatenate((np.array([a_nxs]), a_nx), axis=None)
            asy = np.concatenate((np.array([a_nys]), a_ny), axis=None)
            kx_1 = np.copy(vxs)
            ky_1 = np.copy(vys)
            kvx_1 = np.copy(asx)
            kvy_1 = np.copy(asy)
            kx_2 = vxs + kvx_1 / 2
            ky_2 = vys + kvy_1 / 2
            kvx_2 = np.copy(asx)
            kvy_2 = np.copy(asy)
            kx_3 = vxs + kvx_2 / 2
            ky_3 = vys + kvy_2 / 2
            kvx_3 = np.copy(asx)
            kvy_3 = np.copy(asy)
            kx_4 = vxs + kvx_3
            ky_4 = vys + kvy_3
            kvx_4 = np.copy(asx)
            kvy_4 = np.copy(asy)
            xs[:, i] = xs[:, i - 1] + (kx_1 + 2 * kx_2 + 2 * kx_3 + kx_4) * self.time_step / 6
            ys[:, i] = ys[:, i - 1] + (ky_1 + 2 * ky_2 + 2 * ky_3 + ky_4) * self.time_step / 6
            vxs = vxs + (kvx_1 + 2 * kvx_2 + 2 * kvx_3 + kvx_4) * self.time_step / 6
            vxsc[i] = vxs[0]
            vys = vys + (kvy_1 + 2 * kvy_2 + 2 * kvy_3 + kvy_4) * self.time_step / 6
            vysc[i] = vxs[0]
        return xs, ys, vxsc, vysc

    def setSettings(self, _m, _x, _y, _v_x, _v_y, _G, _total_time, _step, _scheme):
        self.mass = np.copy(_m)
        self.x = np.copy(_x)
        self.y = np.copy(_y)
        self.v_x = np.copy(_v_x)
        self.v_y = np.copy(_v_y)
        self.total_time = _total_time
        self.time_step = _step
        self.scheme = _scheme
        self.n = self.total_time // self.time_step
        self.G_const = _G

        if self.scheme == 'Эйлера':
            self.make_figure(self.euler_scheme())
        if self.scheme == 'Эйлера-Крамера':
            self.make_figure(self.euler_kramer_scheme())
        if self.scheme == 'Верле':
            self.make_figure(self.verlet_scheme())
        if self.scheme == 'Бимана':
            self.make_figure(self.beeman_scheme())
        if self.scheme == 'Рунге-Кутты':
            self.make_figure(self.runge_kutta_scheme())

        self.notifyObservers()

    def make_figure(self, scheme):
        fg = go.Figure(data=[go.Scatter(x=scheme[0][i % self.mass.size, :], y=scheme[1][i % self.mass.size, :],
                             mode='lines',
                             line=dict(width=2), name='Way ' + str(i - self.mass.size)) for i in range(0, self.mass.size * 2)])

        fg.update_layout(title={"font": dict(size=20), "text": "Солнечная система"})

        steps = []
        frames = []

        kinetic = np.sum(self.mass[1:]) * (scheme[2][-1] ** 2 + scheme[3][-1] ** 2) / 2
        xx = scheme[0][:, -1]
        yy = scheme[1][:, -1]
        rx = xx[1:] - xx[0]
        ry = yy[1:] - yy[0]
        potential = self.G_const * (np.sum(self.mass[1:] / (rx**2 + ry**2)**0.5)) * self.mass[0]
        energy = kinetic - potential

        for i in range(self.n):
            name = 'Общая энергия (Дж): {}, Текущее время (с): {}, Центр масс vx: {}, Центр масс vy: {}'.format(energy, i * self.time_step, scheme[2][-1], scheme[3][-1])
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
                    x=scheme[0][k, [i]],
                    y=scheme[1][k, [i]],
                    mode='markers',
                    marker=dict(size=int(self.mass[k] / np.max(self.mass) * 20)),
                    name='Planet ' + str(k)) for k in range(0, self.mass.size)
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
