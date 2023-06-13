import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.testing.decorators

import manylabels


@matplotlib.testing.decorators.image_comparison(
    baseline_images=['test_manylabels_valid_data'], tol=10, extensions=['png']
)
def test_manylabels_valid_data(): 
    n = 100
    x = np.array([pd.Timestamp(2000,1,1,5,0,0) + pd.Timedelta(minutes=i) for i in range(n)])
    y = np.sin(2*np.pi*np.arange(n)/n)
    
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
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(8))
    # manylabels.ManyLabels(ax, data)
    import matplotlib.dates as mdates
    myFmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(myFmt)
    return