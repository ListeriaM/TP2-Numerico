import numpy as np
import matplotlib.pyplot as plt

class ODE:
    def __init__(self, f):
        self._f = f
        self.f = f
        self.integrate = rk4

    def set_integrator(self, method):
        methods = {
            'euler' : euler,
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

# ----------------------- FUNCIONES AUXILIARES K -----------------------

def k_1(f, t, y):
    return np.array(f(t, y))

def k_2(f, t, y, h, k1):
    return np.array(f(t + h/2, h/2 * k1 + y))

#def k_3(f, t, y, h, k1, k2):
   # return np.array(f(t + h, y - h * k1 + 2*h * k2))

def k_4(f, t, y, h, k3):
    return np.array(f(t + h, y + h * k3))

# ----------------------------- METODOS -------------------------------

def euler(f, t, y, h):
    k1 = k_1(f, t, y)
    return y + h * k1

def rk4(f, t, y, h):
    k1 = k_1(f, t, y)
    k2 = k_2(f, t, y, h, k1)
    k3 = k_2(f, t, y, h, k2)
    k4 = k_4(f, t, y, h, k3)
    return y + h/6 * k1 + h/3 * k2 + h/3 * k3 + h/6 * k4

# --------------------------- FUNCIONES DEL TP -----------------------

def edo_pendulo (t, y, args):
    b, m, l = args
    theta, v = y 

    return [v, (-b/m)*v-(g/l)*theta]

def energia (y, m, l):
    theta, v = y

    return m*g*l*(1-np.cos(theta))+0.5*m*((l*v)**2)


#Ingresar los datos:

#Ingrese el paso deseado:
h = 0.2 #propuesto
h_euler = 0.0002 #Funciona bien Euler Ej 1
#h_euler = 0.002 #Funciona bien Euler Ej 2

#""" DESCOMENTAR PARA UTILIZAR LOS PARAMETROS DEL EJ1
#Ej 1 NO AMORTIGUADO
m = 1
l = 1
b = 0
theta0 = np.radians(30)
v0 = 0
#"""

""" DESCOMENTAR PARA UTILZAR LOS PARAMETROS DEL EJ2
#Ej 2 AMORTIGUADO
m = 1
l = 1
b = 0.5
theta0 = np.radians(30)
v0 = np.radians(100)
#"""

g = 9.81
y0 = [theta0, v0]


#----------------------- RK4 ----------------------------------

theta_rk = [theta0]
v_rk = [v0]
t_rk = np.arange(0, 20, h)
E_rk = [energia(y0, m, l)]

solucion_rk = ODE(edo_pendulo)

solucion_rk.set_f_params(b, m, l).set_initial_value(y0)

for i in range(len(t_rk)-1):
    solucion_rk.next(h)
    theta_rk.append(solucion_rk.y[0])
    v_rk.append(solucion_rk.y[1])
    E_rk.append(energia(solucion_rk.y, m, l))


#--------------------- EULER ----------------------------------

theta_euler = [theta0]
v_euler = [v0]
t_euler = np.arange(0, 20, h_euler)
E_euler = [energia(y0, m, l)]

solucion_euler = ODE(edo_pendulo)

solucion_euler.set_integrator('euler')

solucion_euler.set_f_params(b, m, l).set_initial_value(y0)


for i in range(len(t_euler)-1):
    solucion_euler.next(h_euler)
    theta_euler.append(solucion_euler.y[0])
    v_euler.append(solucion_euler.y[1])
    E_euler.append(energia(solucion_euler.y, m, l))


#-------------------- GRAFICOS -------------------------------

fig, axs = plt.subplots(3, 2)
fig.suptitle('Ej 1: no amortiguado')
axs[0, 0].set_title('RK4 h = ' + str(h))
axs[0, 0].plot(t_rk, theta_rk)
axs[0, 0].set(ylabel = 'Posicion [rad]')
axs[0, 0].grid(True)
axs[1, 0].plot(t_rk, v_rk)
axs[1,0].set(ylabel = 'Velocidad [rad/s]')
axs[1,0].grid(True)
axs[2,0].plot(t_rk, E_rk)
axs[2,0].set(ylabel = 'Energia [J]')
axs[2,0].grid(True)
axs[2,0].set_ylim(-5,5)
axs[2,0].set(xlabel = 'Tiempo [s]')
axs[0,1].set_title('Euler h = ' + str(h_euler))
axs[0,1].plot(t_euler, theta_euler)
axs[0,1].grid(True)
axs[1,1].plot(t_euler, v_euler)
axs[1,1].grid(True)
axs[2,1].plot(t_euler, E_euler)
axs[2,1].grid(True)
axs[2,1].set_ylim(-5,5)
axs[2,1].set(xlabel = 'Tiempo [s]')
plt.show()