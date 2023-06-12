"""
Many plots in the heliophysics science community are of satellites showing various physical 
observations. To place these observations in context, scientists often include multiple
x-axis labels showing, for example, the satellite location. This is surprisingly hard to
implement using matplotlib. Nevertheless, `manylabels.ManyLabels()` class provides this
functionality.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.dates
import pandas as pd
import numpy as np


class ManyLabels:
    def __init__(
            self, ax:plt.Axes, data:pd.DataFrame, round:bool=True, 
            fill_missing:str='', gap_thresh:float=None, adjust_bottom:float=None,
            label_coord:tuple=None
            ) -> None:
        """
        Plot multiple x-axis labels on a subplot.

        Parameters
        ----------
        ax: plt.Axes
            The subplot to add labels to.
        data: pd.DataFrame
            The x-axis label data to plot. The DataFrame index must be time.
            The columns will correspond to the x-axis labels.
        round: bool
            Round data to nearest tenths to reduce plot clutter.
        fill_missing:str
            Character to fill a tick label if data is not within gap_thresh.
        gap_thresh: float
            The maximum time gap, in seconds, before the x-axis label is marked with
            fill_missing. If None, it will calculate gap_thresh using the median data time
            separation.
        adjust_bottom: float

        label_coord: tuple

        Example
        -------
        >>> import numpy as np
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import manylabels
        >>>
        >>> n = 100
        >>> x = np.array([pd.Timestamp(2000,1,1,5,0,0) + pd.Timedelta(minutes=i) for i in range(n)])
        >>> y = np.random.rand(n)
        >>> 
        >>> data = pd.DataFrame(
        >>>     index=x,
        >>>     data={
        >>>         'x':np.linspace(0, 10, num=n),
        >>>         'y':np.linspace(10, 20, num=n),
        >>>         'z':np.linspace(-5, 5, num=n)
        >>>         }
        >>>     )
        >>> 
        >>> fig, ax = plt.subplots()
        >>> ax.plot(x, y)
        >>> ManyLabels(ax, data)
        >>> plt.show()
        """
        self.ax = ax
        self.data=data
        self.round=round
        self.fill_missing=fill_missing
        self.gap_thresh=gap_thresh
        self.adjust_bottom = adjust_bottom
        self.label_coord = label_coord

        if self.gap_thresh is None:
            dt = np.array([
                (tf-ti).total_seconds() for ti, tf 
                in zip(self.data.index[:-1], self.data.index[1:])
                ])
            self.gap_thresh = np.median(dt)
        if fill_missing != '':
            raise NotImplementedError
        if round:
            self.data = self.data.round(1)

        cols = list(self.data.columns)
        if self.adjust_bottom is None:
            self.adjust_bottom = (1+len(cols))*0.04
        if self.label_coord is None:
            self.label_coord = (-0.1, -0.00*(1+len(cols)))

        self.label()
        return
    
    def label(self):
        cols = list(self.data.columns)
        self.ax.xaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(self._format_xaxis))
        self.ax.set_xlabel("\n".join(["Time"] + cols))
        self.ax.xaxis.set_label_coords(*self.label_coord)
        self.ax.format_coord = lambda x, y: "{}, {}".format(
            matplotlib.dates.num2date(x).replace(tzinfo=None).isoformat(), round(y)
        )
        plt.subplots_adjust(bottom=self.adjust_bottom)
        return self


    def _format_xaxis(self, tick_val, tick_pos):
        """
        The tick magic happens here. pyplot gives it a tick time, and this function 
        returns the closest label to that time. Read docs for FuncFormatter().
        """
        tick_time = matplotlib.dates.num2date(tick_val).replace(tzinfo=None)
        i_min_time = np.argmin(np.abs(self.data.index - tick_time))

        if np.abs(self.data.index[i_min_time] - tick_time).total_seconds() > self.gap_thresh:
            return tick_time.strftime("%H:%M:%S")

        ticks = '\n'.join(self.data.iloc[i_min_time, :].astype(str))
        ticks = self.data.index[i_min_time].strftime("%H:%M:%S") + '\n' + ticks
        return ticks
    

if __name__ == '__main__':
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
    ManyLabels(ax, data)
    plt.show()