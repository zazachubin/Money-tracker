from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import numpy as np
import seaborn as sns
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ PlotCanvas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlotCanvas(FigureCanvas):
    def __init__(self, title, ylabel, parent=None):
        self.title=title
        self.ylabel = ylabel
        plt.style.use('classic')
        self.fig, self.ax = plt.subplots(figsize=(5, 2), tight_layout=True)
        FigureCanvas.__init__(self, self.fig)
        self.ax.set(xlabel='დრო', ylabel=self.ylabel, title=self.title)
        #self.ax.set_facecolor('#33666630')
        self.ax.minorticks_on()
        # Handle date time conversions between pandas and matplotlib
        from pandas.plotting import register_matplotlib_converters
        register_matplotlib_converters()
        #self.fig.subplots_adjust(bottom=0.1) # or whatev
        
        # Formatting Date
        date_format = DateFormatter('%d/%m/%Y')
        self.ax.xaxis.set_major_formatter(date_format)
        self.ax.xaxis_date()
        self.ax.autoscale_view()
        self.fig.autofmt_xdate()
        self.ax.tick_params(axis='x', rotation=25)
        self.ax.grid()

    def plot(self,data):
        self.ax.clear()
        self.ax.bar(data[0], data[1], width=1, color='#0000ff50', align='center')
        self.ax.bar(data[2], data[3], width=1, color='#00ff0050', align='center')
        self.ax.bar(data[4], data[5], width=1, color='#ff000050', align='center')
        self.ax.legend(['ფინანსური დინამიკა','შემოსავალი','ხარჯი'], loc='lower right', fontsize=10)

        self.ax.set(xlabel='დრო', ylabel=self.ylabel, title=self.title)
        #self.ax.set_facecolor('#33666630')
        self.ax.minorticks_on()
        # Formatting Date
        date_format = DateFormatter('%d/%m/%Y')
        self.ax.xaxis.set_major_formatter(date_format)
        self.ax.tick_params(axis='x', rotation=25)
        self.ax.xaxis_date()
        self.ax.autoscale_view()
        self.ax.grid()
        self.draw()
# ~~~~~~~~~~~~~~~~~~~~~~~ PlotCanvasPieChart ~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlotCanvasPieChart(FigureCanvas):
    def __init__(self,parent=None):
        fig, self.ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        FigureCanvas.__init__(self, fig)
        self.ax.pie([1], wedgeprops=dict(width=0.5), startangle=-40)

    def updateChart(self, A, B):
        self.recipe = A
        self.data = B
        wedges, texts = self.ax.pie(self.data, wedgeprops=dict(width=0.5), startangle=-40)
        
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            self.ax.annotate(self.recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),horizontalalignment=horizontalalignment, **kw)
        
        self.ax.set_title("ხარჯების კატეგორიები")

        self.draw()
# ~~~~~~~~~~~~~~~~~~~~~~ PlotCanvasHistogram ~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlotCanvasHistogram(FigureCanvas):
    def __init__(self,title,parent=None):
        self.title = title
        self.Xlabel = "ვალუტა"
        fig, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        FigureCanvas.__init__(self, fig)
        self.ax.set(xlabel=self.Xlabel, ylabel='counts', title=self.title)
        self.ax.autoscale_view()
        self.ax.grid()
        # matplotlib histogram
        #plt.hist([], color = 'blue', edgecolor = 'black',
        #		bins = int(180/5))

        # seaborn histogram
        #sns.distplot([], hist=True, kde=False, 
        #			bins=int(180/5), color = 'blue',
        #			hist_kws={'edgecolor':'black'})
        # Add labels
        #plt.title('Histogram of Arrival Delays')
        #plt.xlabel('რუბლი')
        #plt.ylabel('counts')

    def updateHist(self, data):
        self.ax.clear()
        self.ax.hist(data, color = 'blue', edgecolor = 'black', bins = int(len(data)/5))
        sns.distplot(data, hist = False, kde = True,
                    kde_kws = {'shade': True, 'linewidth': 3}, 
                    label = 'airline')
        self.ax.set(xlabel=self.Xlabel, ylabel='counts', title=self.title)
        self.ax.autoscale_view()
        self.ax.grid()
        self.draw()

    def setXlabel(self, Xlabel):
        self.Xlabel = Xlabel