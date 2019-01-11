#TODO: add more documentation
#TODO: add zipcode option
import quandl
import pandas as pd
import requests
from queue import Queue
import threading
from qndlvars import *

class QuandlRealestateSDK(threading.Thread):
    '''The QuandlRealestateSDK is a wrapper for the Quandl real estate API.
    The package allows you to view the information returned by the Quandl real estate API
    in a pandas dataframe.

    Because not all types of real estate information are available for every area type this
    package checks to see which inidicator code is valid for the area type you are searching.

    Inherits from:
        threading.Thread

    Dependencies:
        quandl
        pandas
        requests

    class QuandlRealestateSDK(threading.Thread)
          Class variables:
            API KEY:
                quandl.ApiConfig.api_key = <insert your api key here>

            Urls of API resources formatted into pandas dataframes:
                STATECODES_URL = 'https://s3.amazonaws.com/quandl-production-static/zillow/areas_state.txt'
                COUNTYCODES_URL = 'https://s3.amazonaws.com/quandl-production-static/zillow/areas_county.txt'
                METROCODES_URL = 'https://s3.amazonaws.com/quandl-production-static/zillow/areas_metro.txt'
                CITYCODES_URL = 'https://s3.amazonaws.com/quandl-production-static/zillow/areas_city.txt'
                NBHCODES_URL = 'https://s3.amazonaws.com/quandl-production-static/zillow/areas_neighborhood.txt'
                INDCODES_URL = 'https://s3.amazonaws.com/quandl-production-static/zillow/indicators.csv

            The following codes dictate the size/nature of the area your would like to search:
                (DICT)AREA_TYPE=
                    STATE:   S
                    County: CO
                    Greater Metropolitan Area: M
                    City: C
                    Neighborhood: N
                    Zip Code: Z

            CODES
                This is list of resource urls that contain data which are parsed into the dictionaries used to make pandas
                dataframes.

            CODE_LIST
                This variable contains all of the parsed dictionaries

            STATECODES
                keys for the states dictionary
            COUNTYCODES
                keys for the county dictionary
            METROCODES
                keys for the metro areas dictionary
            CITYCODES
                keys for the city dictionary
            NBHCODES
                keys for the neiborhood dictionary
            INDCODES_CD
                keys for the indicator codes dictionary
            AREA_TYPECODES
                keys for the area types dictionary
            LEN_INDCODES_CD
                Current number of indicator codes used in the API

            DFS
                Class variable containing all of the area type and indicator code dictionaries as pandas dataframes

            STATESCODES_DF
                states codes dataframe
            COUNTYCODES_DF
                county codes dataframe
            METROCODES_DF
                metro codes dataframe
            CITYCODES_DF
                city codes dataframe
            NBHCODES_DF
                neigborhood codes dataframe
            INDCODES_DF
                indicator codes dataframe
            AREA_TYPE_DF
                area type dataframe

            FRAME_DICT
                A dictionary containing normalized codes that should be used to specify the area type to be searched.
                The values for each key are dataframes containing API resource information.
                The keys are:
                    'STATE'
                    'COUNTY'
                    'METRO'
                    'CITY'
                    'NBH' (Neighborhood)
                    'IND_CODES' (Indicator codes)

        --------------------------------------------------------------------------------------------------------------
        Instance Variables:
            Private:
                self.__item_code = None
                    (string) The item code is a combination of the area type code and a specific area:
                        Example:
                            'CO516'
                                C is for CITY
                                O516 is the specific city you would like to get information about
                            Item code information is automatically formatted in the dataframe.
                            The user will set the specific item code to be used in the program by calling the
                            <class>.set_item_code(self,<item_code>) method.

                self.__valid_codes_list = []
                        (list of strings) this is a list of valid indicator codes for the selected area type
                        and specific locale
            Public:
                self.valid_codes_df = None
                    This is a dynamically updating pandas dataframe of valid indicator codes. The dataframe is updated
                    as the worker threads complete their tasks and pass the information the <class>.__validz_codes_list
                    variable.

                self.selection_frame = None

                self.custom_frame = None

                self.queue = Queue()
                    This is a queue of lists containing indicator codes that are validated by workers in each thread
        ---------------------------------------------------------------------------------------------------------------
        Instance Methods:
            Public:
                <class>.lookup_codes(self,selection,conditional_one,*args)
                <class>.set_item_code(self, item_code)
                <class>.run_indicator_validation(self)
                <class>.lookup_ind_codes(self,ind_codes_list)
                <class>.custom_qr_query(self,ind_code,info_date=None)
                <class>.join_qr_frame_index(self,frame_1,*args)

            Private:
                <class>.__set_valid_indcodes(self,lst)
                <class>.__set_queue(self)
        '''
    quandl.ApiConfig.api_key = '<YOUR DEVELOPER KEY HERE>'

    CODES = [STATECODES_URL,COUNTYCODES_URL,METROCODES_URL,CITYCODES_URL,NBHCODES_URL,INDCODES_URL]

    #associative array

    #parses ursl into lists
    CODE_LIST = [dict(map(lambda x: x.split('|'),requests.get(info).text.split('\n')[1:-1])) for info in CODES]+[AREA_TYPE]
    STATECODES = CODE_LIST[0].keys()
    COUNTYCODES = CODE_LIST[1].keys()
    METROCODES = CODE_LIST[2].keys()
    CITYCODES = CODE_LIST[3].keys()
    NBHCODES = CODE_LIST[4].keys()
    INDCODES_CD = CODE_LIST[5].keys()
    AREA_TYPECODES = CODE_LIST[6].keys()
    LEN_INDCODES_CD = len(INDCODES_CD)


    #DATAFRAMES
    DFS = [pd.DataFrame(list(codes.items()), index=None,columns=['DESCRIPTION','CODE']) for codes in CODE_LIST]

    STATESCODES_DF = DFS[0]
    COUNTYCODES_DF = DFS[1]
    METROCODES_DF = DFS[2]
    CITYCODES_DF = DFS[3]
    NBHCODES_DF = DFS[4]
    INDCODES_DF = DFS[5]
    AREA_TYPE_DF = DFS[6]

    ALL_CODES = [[STATESCODES_DF,'S'],[COUNTYCODES_DF,'CO'],[METROCODES_DF,'M'],
                 [CITYCODES_DF,'C'],[NBHCODES_DF,'N']]

    FRAME_DICT = {
        'STATE': STATESCODES_DF,
        'COUNTY': COUNTYCODES_DF,
        'METRO': METROCODES_DF,
        'CITY': CITYCODES_DF,
        'NBH': NBHCODES_DF,
        'IND_CODES': INDCODES_DF
    }

    def __init__(self):
        threading.Thread.__init__(self)
        self.__item_code = None
        self.__valid_codes_list = []
        self.valid_codes_df = None
        self.selection_frame = None
        self.custom_frame = None
        self._queue = Queue()

        for lst in QuandlRealestateSDK.ALL_CODES:
            if not lst[0]['CODE'].str.contains(lst[1]).all():
                lst[0]['CODE'] = lst[0]['CODE'].apply(lambda x: lst[1]+str(x))

    def lookup_codes(self,selection,conditional_one,*args):
        selection = selection.upper()
        if selection not in QuandlRealestateSDK.FRAME_DICT:
            raise KeyError("{} not a valid selection. Choose from: {}".format(selection,list(QuandlRealestateSDK.FRAME_DICT.keys())))

        cond_list = [conditional_one] + list(args)

        set_cond_query ="QuandlRealestateSDK.FRAME_DICT['{}']".format(selection) +"[" +" & ".join(["QuandlRealestateSDK.FRAME_DICT['{}']['DESCRIPTION'].str.contains('{}')".format(selection,cond) for cond in cond_list])+']'

        self.selection_frame = eval(set_cond_query)
        return self.selection_frame

    #setter
    def set_item_code(self, item_code):
        self.__item_code = item_code
        return self.__item_code


    def __set_valid_indcodes(self,lst):
        available_ind_list = []
        for val in lst:
            try:
                rental_Indx_SFR = quandl.get('ZILLOW/{}_{}'.format(self.__item_code,val))
                available_ind_list.append(QuandlRealestateSDK.INDCODES_DF[QuandlRealestateSDK.INDCODES_DF['CODE']==val])
            except:
                #log exceptions
                pass

        self.__valid_codes_list += available_ind_list

        if len(self.__valid_codes_list)>0:
            self.valid_codes_df = pd.concat(self.__valid_codes_list, ignore_index=True)

        return self.__valid_codes_list


    def __set_queue(self):
        num = len(QuandlRealestateSDK.INDCODES_DF['CODE'].values)
        codes = QuandlRealestateSDK.INDCODES_DF['CODE'].values
        for i in range(0,num,2):
            if (num - i) < 2:
                self._queue.put(codes[i:num])
                self._queue.task_done()
            else:
                self._queue.put(codes[i:i+3])
                self._queue.task_done()

    def run_indicator_validation(self):
        self.__set_queue()
        for i in range(self._queue.qsize()):
            t = threading.Thread(target=self.__set_valid_indcodes, args=(list(self._queue.get()),))
            t.daemon = True
            t.start()
        t.join()

    def lookup_ind_codes(self,ind_codes_list):
        data = [QuandlRealestateSDK.INDCODES_DF[QuandlRealestateSDK.INDCODES_DF['CODE'] == ind_code] for ind_code in ind_codes_list]
        return pd.concat(data)

    def custom_qr_query(self,ind_code,info_date=None):
        assert self.valid_codes_df is not None,"The are currently no indicator codes for your query. Please try again later."
        if len(self.valid_codes_df[self.valid_codes_df['CODE']==ind_code])<1:
            raise ValueError("{} is not a valid Indicator Code".format(ind_code))
        desc = self.valid_codes_df[self.valid_codes_df['CODE']==ind_code]
        if info_date is not None:
            self.final_frame = quandl.get('ZILLOW/{}_{}'.format(self.__item_code,ind_code),start_date=info_date).rename(columns={'Value':desc['DESCRIPTION'].values[0]})
            return self.final_frame
        custom_frame = quandl.get('ZILLOW/{}_{}'.format(self.__item_code,ind_code),start_date=info_date).rename(columns={'Value':desc['DESCRIPTION'].values[0]})
        return custom_frame

    def join_qr_frame_index(self,frame_1,*args):
        data = pd.concat([frame_1.join(arg,how='outer') for arg in args],sort=True)
        return data
