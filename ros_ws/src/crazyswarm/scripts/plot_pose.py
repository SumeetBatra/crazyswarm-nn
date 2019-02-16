import matplotlib.pyplot as plt
import numpy as np


TIME=0
X=1
Y=2
Z=3
QX=4
QY=5
QZ=6
QW=7
ROLL=8
PITCH=9
YAW=10

data = np.loadtxt("pose.csv", delimiter=",", skiprows=1)

# new figure
plt.figure(0)

# X, Y, Z
plt.subplot(2, 1, 1)
plt.plot(data[:,TIME], data[:,X], '-', label='X')
plt.plot(data[:,TIME], data[:,Y], '-', label='Y')
plt.plot(data[:,TIME], data[:,Z], '-', label='Z')
plt.xlabel('Time [s]')
plt.ylabel('Position [m]')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

# roll, pitch, yaw
plt.subplot(2, 1, 2)
plt.plot(data[:,TIME], data[:,ROLL], '-', label='roll')
plt.plot(data[:,TIME], data[:,PITCH], '-', label='pitch')
plt.plot(data[:,TIME], data[:,YAW], '-', label='yaw')
plt.xlabel('Time [s]')
plt.ylabel('orientation [rad]')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plt.show()

