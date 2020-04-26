import numpy as np 
import scipy.integrate as spi
import matplotlib.pyplot as plt

def dU_dx(U, x):
    # Here U is a vector such that y=U[0] and z=U[1]. This function should return [y', z']
    return [U[1], - 1.5 * (U[0] * U[0] - 1) * U[1] - U[0]]
    
U0 = [0.5, 0]
ts = np.linspace(-20, 20, 400)
Us = spi.odeint(dU_dx, U0, ts)

plt.xlabel("t")
plt.ylabel("x(t)")
plt.title("x(t)")
plt.plot(ts,  Us[:, 0])
plt.grid()
plt.show()

plt.xlabel("x(t)")
plt.ylabel("x_prime(t)")
plt.title("x_prime(t) vs x(t)")
plt.plot(Us[:,0], Us[:,1])
plt.grid()
plt.show()
