import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
data = np.random.rand(50, 50)

plt.imshow(data, cmap='viridis', interpolation='mitchell')

plt.colorbar()

plt.show()
