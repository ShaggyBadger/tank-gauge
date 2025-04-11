import matplotlib.pyplot as plt
import numpy as np
import importlib
import initializer
import settings
from rich.traceback import install

install()


np.random.seed(0)
data = np.random.rand(50, 50)

plt.imshow(data, cmap='viridis', interpolation='mitchell')

plt.colorbar()

plt.show()

if __name__ == '__main__':
	importlib.reload(settings)
	importlib.reload(initializer)
