import pandas as pd
import os

def readInData(url,separator,skiprows_num=None,*args):
    '''This method takes in a url and outputs a dataframe
    Parameters are:
        url or file location
        column delimeter
        number of rows to skip (default is None)
        names of columns
    '''
    return pd.read_table(url,sep=separator,skiprows=skiprows_num,names=args)

def join_qr_frame_index(frame_1, *args):
    data = pd.concat([frame_1.join(arg, how='outer') for arg in args], sort=True)
    return data

def cache_df_as_json(dataframe,file_loc):
    '''converts a dataframe to a json object and saves it to a file'''
    pass

def get_json_cache_as_df(file_path):
    pass
