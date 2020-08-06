import numpy as np

class ODE:
    def __init__(self, f):
        self._f = f
        self.f = f
        self.integrate = rk4

    def set_integrator(self, method):
        methods = {
            'euler' : euler,
            'rk2' : rk2,
            'rk3' : rk3,
            'rk4' : rk4
        }
        self.integrate = methods.get(method, self.integrate)
        return self

    def set_initial_value(self, y, t = 0.0):
        self.y = y
        self.t = t
        return self

    def set_f_params(self, *args):
        self.f = lambda t, y: self._f(t, y, args)
        return self

    def next(self, step):
        self.y = self.integrate(self.f, self.t, self.y, step)
        self.t += step
        return self.y

# ----------------------- AUXILIARY FUNCTIONS -----------------------

def k_1(f, t, y):
    return np.array(f(t, y))

def k_2(f, t, y, h, k1):
    return np.array(f(t + h/2, h/2 * k1 + y))

def k_3(f, t, y, h, k1, k2):
    return np.array(f(t + h, y - h * k1 + 2*h * k2))

def k_4(f, t, y, h, k3):
    return np.array(f(t + h, y + h * k3))

# ----------------------------- METHODS -------------------------------

def euler(f, t, y, h):
    k1 = k_1(f, t, y)
    return y + h * k1

def rk2(f, t, y, h):
    k1 = k_1(f, t, y)
    k2 = k_2(f, t, y, h, k1)
    return y + h * k2

def rk3(f, t, y, h):
    k1 = k_1(f, t, y)
    k2 = k_2(f, t, y, h, k1)
    k3 = k_3(f, t, y, h, k1, k2)
    return y + h/6 * k1 + 2/3*h * k2 + h/6 * k3

def rk4(f, t, y, h):
    k1 = k_1(f, t, y)
    k2 = k_2(f, t, y, h, k1)
    k3 = k_2(f, t, y, h, k2)
    k4 = k_4(f, t, y, h, k3)
    return y + h/6 * k1 + h/3 * k2 + h/3 * k3 + h/6 * k4