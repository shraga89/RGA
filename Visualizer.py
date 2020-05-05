import pandas as pd
import os
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self,results_folder):
        self.results_folder = results_folder

    def read_results_file(self,fname):
        df = pd.read_csv(fname)
        return df

    def read_offset_dir(self,dirname):
        list_df = []
        for file in os.listdir(dirname):
            fname = dirname+"/"+file
            list_df.append(self.read_results_file(fname))
        return list_df

    def aggregate_data_frames(self,list_df):
        values = []
        # if set(groupby_columns)-set(reduced_columns):
        #     raise ValueError("error in specifiying visualization dataframe columns")
        total_df = pd.concat(list_df)
        buyers = sorted(total_df["buyer"].drop_duplicates().values)
        turns = total_df["turn"].drop_duplicates().values
        for buyer in buyers:
            cuurent_values = total_df[total_df["buyer"]==buyer].groupby("turn")['budget'].mean().values
            values.append(cuurent_values)
        return values,buyers,turns


    def create_figure(self, x, y_axes, y_label, x_label, legends, colors, output_fname):

        if not os.path.exists(os.path.dirname(output_fname)):
            try:
                os.makedirs(os.path.dirname(output_fname))
            except:
                output_fname=os.path.basename(output_fname)

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

    def extract_data_for_figure(self,df,buyers):
        y_axes = []
        legends = []

        for buyer in buyers:
            y_axes.append(df[df["buyer"]==buyer][["turn"]].values)
            legends.append(buyer)
        x = df["turn"].drop_duplicates().values
        return x,y_axes,legends


    def create_figure_per_offset(self,y_label,x_label,output_fname):
        all_dfs = []
        for offset in os.listdir(self.results_folder):
            dirname = self.results_folder+"/"+offset+"/"
            list_df = self.read_offset_dir(dirname)
            all_dfs.append(pd.concat(list_df))
            y_axes,legends,x = self.aggregate_data_frames(list_df)
            # x, y_axes, legends = self.extract_data_for_figure(aggregated_df,buyers)
            colors = ["b","k","r","y","g","violet"]
            self.create_figure(x,y_axes,y_label,x_label,legends,colors,output_fname+"_"+str(offset))
        return all_dfs


if __name__=="__main__":
    visual = Visualizer("simulation_res/")
    all_dfs = visual.create_figure_per_offset("budget","turn","average_budget")
    y_axes, legends, x = visual.aggregate_data_frames(all_dfs)
    colors = ["b", "k", "r", "y", "g", "violet"]
    visual.create_figure(x, y_axes, "budget","turn", legends, colors, "average_budget_aggregated")
