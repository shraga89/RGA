import os
import pandas as pd

def read_results_file(fname):
    df = pd.read_csv(fname)
    return df


def read_offset_dir(dirname):
    list_df = []
    for file in os.listdir(dirname):
        fname = dirname + "/" + file
        list_df.append(read_results_file(fname))
    return list_df


def aggregate_data_frames(list_df, groupby_columns, reduced_columns):
    if set(groupby_columns) - set(reduced_columns):
        raise ValueError("error in specifiying visualization dataframe columns")
    total_df = pd.concat(list_df)
    return total_df[reduced_columns].groupby(groupby_columns).mean()


list_df = read_offset_dir("../simulation_res/0/")
totaldf = aggregate_data_frames(list_df,["buyer","turn"],["buyer","turn","budget"])
print(totaldf)


