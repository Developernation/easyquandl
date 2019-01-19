import quandl
import pandas as pd
import requests
from queue import Queue
import threading
from qndlvars import *
from utils.qndl_urls import *
from utils.quandlutils import *
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
logger = logging.getLogger()

# TODO: add more documentation
# TODO: add zipcode option
# TODO: Add unit tests
# TODO? lookup_codes selection shortcuts e.g. if starts with s, state
# TODO? separate data retrieval to model class
class QuandlRealestateSDK(threading.Thread):
    """The QuandlRealestateSDK is a wrapper for the Quandl real estate API.
    The package allows you to view the information returned by the Quandl real estate API
    in a pandas dataframe.

    Because not all types of real estate information are available for every area type this
    package checks to see which indicator code is valid for the area type you are searching.

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

            The following codes dictate the size/nature of the area your would like to search:
                (DICT)AREA_TYPE=
                    STATE:   S
                    County: CO
                    Greater Metropolitan Area: M
                    City: C
                    Neighborhood: N
                    Zip Code: Z

            AREA_TYPECODES
                keys for the area types dictionary
            LEN_INDCODES_CD
                Current number of indicator codes used in the API

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
                            For example, the user can set the specific item code to be used in the program
                            <class>.item_code = 'C0516'

                self.__valid_codes_list = []
                        (list of strings) this is a list of valid indicator codes for the selected area type
                        and specific locale

                self.__lookup_frame = None

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
                <class>.lookup_codes(self,selection)
                <class>.set_item_code(self, item_code)
                <class>.run_indicator_validation(self)
                <class>.custom_qr_query(self,ind_code,info_date=None)
                <class>.drill_down_loc(self,conditional_one,*args)
            Private:
                <class>.__set_valid_indcodes(self,lst)
                <class>.__set_queue(self)
        ---------------------------------------------------------------------------------------------------------------
        Static Methods:
            Public:
                lookup_ind_codes(ind_codes_list)
                join_qr_frame_index(frame_1,*args)
        """

    # -------------REMEMBER TO ADD YOUR DEVELOPER KEY BELOW---------------------
    # **************************************************************************
    ###########################################################################
    quandl.ApiConfig.api_key = '<INSERT API KEY HERE>'
    ###########################################################################
    # **************************************************************************
    # --------------------------------------------------------------------------
    #QUERY CODES
    INDCODES_DF=readInData(INDCODES_URL,'|',1,'DESCRIPTION','CODE')
    LEN_INDCODES_CD = len(INDCODES_DF)

    FRAME_DICT = {
        'STATE': ['S', STATECODES_URL],
        'COUNTY' : ['CO', COUNTYCODES_URL],
        'METRO': ['M',METROCODES_URL],
        'CITY': ['C',CITYCODES_URL],
        'NBH': ['N',NBHCODES_URL],
        'IND_CODES': INDCODES_DF
    }

    def __init__(self):
        threading.Thread.__init__(self)
        self.__item_code = None
        self.__valid_codes_list = []
        self.valid_codes_df = None
        self.__lookup_frame = None
        self.selection_frame = None
        self.custom_frame = None
        self._queue = Queue()

    def lookup_codes(self,selection:'string of AREA_TYPE'):
        selection = selection.upper()
        f_dict = QuandlRealestateSDK.FRAME_DICT[selection]
        if selection not in QuandlRealestateSDK.FRAME_DICT:
            raise KeyError("'{}' not a valid selection. "
                           "Choose from: {}".format(selection, [x for x in f_dict.keys() if x is not 'IND_CODES']))
        codes = readInData(f_dict[1],'|',1,'DESCRIPTION','CODE')
        codes['CODE'] = codes['CODE'].apply(lambda x: f_dict[0]+str(x))
        self.__lookup_frame = codes
        return self.__lookup_frame

    def drill_down_loc(self,conditional_one, *args):
        cond_list = [conditional_one] + list(args)

        mask = self.__lookup_frame
        x = None
        for cond in cond_list:
            x = mask[mask['DESCRIPTION'].str.contains(cond)]
            mask = x

        self.selection_frame = mask
        return self.selection_frame

    @property
    def item_code(self):
        return self.__item_code

    @item_code.setter
    def item_code(self, item_code):
        self.__item_code = item_code

    def __set_valid_indcodes(self, lst):
        available_ind_list = []
        for val in lst:
            try:
#<<<<<<< HEAD:quandlrealestate.py
                res = quandl.get('ZILLOW/{}_{}'.format(self.__item_code,val))
                available_ind_list.append(QuandlRealestateSDK.INDCODES_DF[QuandlRealestateSDK.INDCODES_DF['CODE']==val])
#=======
                quandl.get('ZILLOW/{}_{}'.format(self.__item_code, val))
                available_ind_list.append(
                    QuandlRealestateSDK.INDCODES_DF[QuandlRealestateSDK.INDCODES_DF['CODE'] == val])
#>>>>>>> 8d613f334f1a35f6b03adb23d0204ebce2db6d9b:src/quandlrealestate.py
            except:
                # log exceptions
                pass

        self.__valid_codes_list += available_ind_list

        if len(self.__valid_codes_list) > 0:
            self.valid_codes_df = pd.concat(self.__valid_codes_list, ignore_index=True)

        return self.__valid_codes_list

    def __set_queue(self):
        num = len(QuandlRealestateSDK.INDCODES_DF['CODE'].values)
        codes = QuandlRealestateSDK.INDCODES_DF['CODE'].values
        for i in range(0, num, 2):
            if (num - i) < 2:
                self._queue.put(codes[i:num])
                self._queue.task_done()
            else:
                self._queue.put(codes[i:i + 3])
                self._queue.task_done()

    def run_indicator_validation(self):
        self.__set_queue()
        for i in range(self._queue.qsize()):
            t = threading.Thread(target=self.__set_valid_indcodes, args=(list(self._queue.get()),))
            t.daemon = True
            t.start()
        t.join()

    def custom_qr_query(self, ind_code, info_date=None):
        assert self.valid_codes_df is not None, "The are currently no indicator codes for your query. Please try " \
                                                "again later. "
        if len(self.valid_codes_df[self.valid_codes_df['CODE'] == ind_code]) < 1:
            raise ValueError("{} is not a valid Indicator Code".format(ind_code))
        desc = self.valid_codes_df[self.valid_codes_df['CODE'] == ind_code]
        if info_date is not None:
            self.final_frame = quandl.get('ZILLOW/{}_{}'.format(self.__item_code, ind_code),
                                          start_date=info_date).rename(columns={'Value': desc['DESCRIPTION'].values[0]})
            return self.final_frame
        custom_frame = quandl.get('ZILLOW/{}_{}'.format(self.__item_code, ind_code), start_date=info_date).rename(
            columns={'Value': desc['DESCRIPTION'].values[0]})
        return custom_frame

    @staticmethod
    def lookup_ind_codes(ind_codes_list):
        data = [QuandlRealestateSDK.INDCODES_DF[QuandlRealestateSDK.INDCODES_DF['CODE'] == ind_code] for ind_code in
                ind_codes_list]
        return pd.concat(data)

    @staticmethod
    def join_qr_frame_index(frame_1, *args):
        data = pd.concat([frame_1.join(arg, how='outer') for arg in args], sort=True)
        return data
