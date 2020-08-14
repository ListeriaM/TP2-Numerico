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

# ----------------------- AUXILIARY FUNCTIONS -----------------------

def k_1(f, t, y):
    return np.array(f(t, y))

def k_2(f, t, y, h, k1):
    return np.array(f(t + h/2, h/2 * k1 + y))

#def k_3(f, t, y, h, k1, k2):
   # return np.array(f(t + h, y - h * k1 + 2*h * k2))

def k_4(f, t, y, h, k3):
    return np.array(f(t + h, y + h * k3))

# ----------------------------- METHODS -------------------------------

def euler(f, t, y, h):
    k1 = k_1(f, t, y)
    return y + h * k1

def rk4(f, t, y, h):
    k1 = k_1(f, t, y)
    k2 = k_2(f, t, y, h, k1)
    k3 = k_2(f, t, y, h, k2)
    k4 = k_4(f, t, y, h, k3)
    return y + h/6 * k1 + h/3 * k2 + h/3 * k3 + h/6 * k4

#TP nuestro

#Ingrese los datos:

g = 9.81
#Ingrese el paso deseado:
h = 0.2

#"""
#Ej 1 NO AMORTIGUADO
m = 1
l = 1
b = 0
theta0 = np.radians(30)
v0 = 0
#"""

"""
#Ej 2 AMORTIGUADO
m = 1
l = 1
b = 0.5
theta0 = np.radians(30)
v0 = np.radians(100)
"""

def edo_pendulo (t, y, args):
    b, m, l = args
    theta, v = y 

    return [v, (-b/m)*v-(g/l)*theta]

def energia (y, m, l):
    theta, v = y

    return m*g*l*(1-np.cos(theta))+0.5*m*((l*v)**2)

y0 = [theta0, v0]
theta = [theta0]
v = [v0]
t = np.arange(0, 20, h)
E = [energia(y0, m, l)]

solucion = ODE(edo_pendulo)

#""" RK4

solucion.set_f_params(b, m, l).set_initial_value(y0)

for i in range(len(t)-1):
    solucion.next(h)
    theta.append(solucion.y[0])
    v.append(solucion.y[1])
    E.append(energia(solucion.y, m, l))

plt.figure(0)
plt.plot(t, theta, label = 'Theta')  

plt.xlabel('t')
plt.title('Posicion')
plt.legend(loc='best')
plt.grid(True)
plt.show() 

plt.figure(1)

plt.plot(t, v, label = 'Velocidad')
plt.xlabel('t')
plt.title('Velocidad')
plt.legend(loc='best')
plt.grid(True)
plt.show() 

plt.figure(2)

plt.plot(t, E, label = 'Energia')  

plt.ylim(-5, 5)
plt.xlabel('t')
plt.title('Energia')
plt.legend(loc='best')
plt.grid(True)
plt.show() 
#"""

"""
solucion.set_integrator('euler')

solucion.set_f_params(b, m, l).set_initial_value(y0)

for i in range(len(t)-1):
    solucion.next(h)
    #if solucion.y[0] > theta0:
     #   solucion.y = y0
    #if solucion.y[0] < -theta0:
     #   solucion.y[0] = -theta0
      #  solucion.y[1] = 0
    theta.append(solucion.y[0])
    v.append(solucion.y[1])
    E.append(energia(solucion.y, m, l))

plt.figure(0)
plt.plot(t, theta, label = 'Theta')  

plt.xlabel('t')
plt.title('Posicion')
plt.legend(loc='best')
plt.grid(True)
plt.show() 

plt.figure(1)

plt.plot(t, v, label = 'Velocidad')
plt.xlabel('t')
plt.title('Velocidad')
plt.legend(loc='best')
plt.grid(True)
plt.show() 

plt.figure(2)

plt.plot(t, E, label = 'Energia')  

#plt.ylim(0, 20)
plt.xlabel('t')
plt.title('Energia')
plt.legend(loc='best')
plt.grid(True)
plt.show() 
"""