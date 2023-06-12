import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.testing.decorators

import manylabels

@matplotlib.testing.decorators.image_comparison(
    baseline_images=['test_manylabels_valid_data'], tol=10, extensions=['png']
)
def test_manylabels_valid_data(): 
    n = 100
    x = np.array([pd.Timestamp(2000,1,1,5,0,0) + pd.Timedelta(minutes=i) for i in range(n)])
    y = np.random.rand(n)
    
    data = pd.DataFrame(
        index=x,
        data={
            'x':np.linspace(0, 10, num=n),
            'y':np.linspace(10, 20, num=n),
            'z':np.linspace(-5, 5, num=n)
            }
        )
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    manylabels.ManyLabels(ax, data)
    return