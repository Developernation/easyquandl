import pandas as pd
import os
import json

def quandl_data_sets():
    data_sets = {
        'Realestate':'quandlrealestate.QuandlRealestateSDKv1'
    }
    return data_sets

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

class CacheData:
    def __init__(self,file_name):
        self.__file_path = file_name
        self.__dataframe = None
        self.__json_data = None

    def df_as_json(self,dataframe):
        '''converts a dataframe to a json object and saves it to a file'''
        self.__dataframe = dataframe
        self.__json_data = dataframe.to_json(orient='columns')
        return self.__json_data

    def get_json_cache_as_df(self,new_file_name=None):
        '''Reterns json file cache information as a dataframe:
        Optional arguments:
            new_file_name (str):: allows the user to override the file name
                                  used in the constructor'''
        if new_file_name is None:
            new_file_name = self.__file_path
        with open(new_file_name,'r') as j:
            x = json.load(j)
        return pd.read_json(x,orient='columns')

    def write_json_cache(self):
        '''writes json files containing dataframe info to a cache'''
        with open(self.__file_path,'w') as f:
            json.dump(self.__json_data,f)

    @staticmethod
    def show_cached_files(self,data_dir):
        '''returns a generator containing cached json files
        Parameters are:
            data_dir (str):: a directory location of data files'''
        dir_list = os.listdir(data_dir)
        return (fle for fle in dir_list if fle.endswith('.json'))
            :
