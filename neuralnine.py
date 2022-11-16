import matplotlib.pyplot as plt
import numpy as np

amount = 15
ls = np.random.randint(0,100, amount)

x = np.arange(0,amount, 1)
n = len(ls)
# y = np.arrange( )

for i in range(n):
    for j in range(0, n-i-1):
        plt.bar(x,ls)
        plt.pause(0.01) 
        plt.clf()
        if ls[j] > ls[j+1]:
                ls[j], ls[j+1] = ls[j+1], ls[j]
plt.show()
plt.pause(1)