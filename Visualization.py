import matplotlib.pyplot as plt
import pandas as pd

class Visualization:
    def __init__(self,history):
        self.history = history

    #TODO: add functionality to different kinds of figures - will be added after we know wtf we want
    def create_figure(self, x, y_axes, y_label, x_label, legends, colors, output_fname):
        params = {'legend.fontsize': 'x-large',
                  'figure.figsize': (13, 8),
                  'axes.labelsize': 'x-large',
                  'axes.titlesize': 'x-large',
                  'xtick.labelsize': 'small',
                  'ytick.labelsize': 'x-large',
                  'font.family': 'serif'}

        plt.rcParams.update(params)
        plt.figure()
        if legends is not None:
            for j, y in enumerate(y_axes):
                plt.plot(x, y, color=colors[j], linewidth=5, markersize=5, mew=1, label=legends[j])
        plt.xticks(x, fontsize=25)
        plt.yticks(fontsize=25)
        plt.ylabel(y_label, fontsize=30)
        plt.xlabel(x_label, fontsize=30)
        plt.legend(loc="best")
        plt.savefig(output_fname + ".png")
        plt.clf()


    def infer_aggregated_stats(self,df,column,stat="mean"):
        if stat=="mean":
            return df[["turn", column]].apply(pd.to_numeric).groupby("turn").mean()[column]
        elif stat == "max":
            return df[["turn", column]].apply(pd.to_numeric).groupby("turn").max()[column]
        elif stat == "min":
            return df[["turn", column]].apply(pd.to_numeric).groupby("turn").min()[column]
        elif stat == "median":
            return df[["turn", column]].apply(pd.to_numeric).groupby("turn").median()[column]
        else:
            raise ValueError("undefined statistic parameter for plot")

    def create_price_plot(self,stat="mean"):
        """
        Creates plot for price statistics while considering only succesfull transactions.

        :param stat: parameter for statistics choosing - {"mean","max","min","median"}
        :return:
        """
        df = self.history.copy()
        df = df[df['outcome'] == 'successful']
        buyer_prices = self.infer_aggregated_stats(df,"buying_price",stat)
        seller_prices = self.infer_aggregated_stats(df,"selling_price",stat)
        y_axes = [buyer_prices,seller_prices]
        x = df["turn"].drop_duplicates().values
        self.create_figure(x,y_axes,stat+" price","iteration",["Buyers","Sellers"],["b","r"],stat+"_prices")