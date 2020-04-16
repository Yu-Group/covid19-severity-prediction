# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:13:38 2016

@author: adityanagarajan
"""

import pandas as pd
import os

import numpy as np
import time
import multiprocessing


def unwrap_self_f(arg, **kwarg):
    """Taken from 
    http://www.rueckstiess.net/research/snippets/show/ca1d7d90
    """
    return parse_AHRF_ascii.create_ahrf_frame(*arg, **kwarg)


class parse_AHRF_ascii(object):
    """This class extracts information from AHRF ascii
    
    Attributes:
    ----------------------
    file_path: the path of the ascii file to parse
    meta_data_path: path of the .sas file
    meta_data: data frame containing column name and location of variable in ascii
    num_cores: number of cores/workers to use while parsing the file
    """

    def __init__(self, num_cores=4, ascii_file_path='../data/ahrf2016.asc',
                 sas_file_path='../data/DOC/ahrf2015-16.sas'):
        self.file_path = ascii_file_path
        self.meta_data_path = sas_file_path
        self.num_cores = num_cores
        self.meta_data = self.load_meta_data()
        self.ahrf_columns = []

    def load_meta_data(self):
        if os.path.exists('DOC/meta_data.csv'):
            print('meta data file exists loading...')
            meta_data = pd.read_csv('DOC/meta_data.csv')
        else:
            print('meta data file does not exists, creating and saving to DOC/meta_data.csv')
            meta_data = self.parse_meta_data()

        return meta_data

    def parse_meta_data(self):
        """This function extracts the meta data to parse the AHRF
        """
        meta_data_frame = pd.DataFrame(columns=['FieldId', 'Position', 'FieldLength', 'FieldName'])
        ctr = 0
        with open(self.meta_data_path, 'r') as md:
            for line in md.readlines():
                temp = line.split()
                # Check for position indicator field
                if len(temp) > 1 and temp[0][0] == '@':
                    if temp[2] == '$':
                        field_length = float(temp[3].strip('.'))
                    else:
                        field_length = float(temp[2].strip('.'))

                    field = [temp[1], int(temp[0].strip('@')), field_length]
                    meta_data_frame.loc[ctr, :3] = field
                    ctr += 1
                # check for field name definitions and fill the meta_data_frame
                if len(temp) > 1 and temp[0][0] == 'f':
                    meta_data_frame.loc[meta_data_frame.FieldId == temp[0], 'FieldName'] = ''.join(temp[2:]).strip('"')
        if not os.path.exists('DOC/'):
            os.mkdir('DOC/')
        meta_data_frame.to_csv('DOC/meta_data.csv', index=False)

        return meta_data_frame

    def parse_ahrf_file(self, columns):
        """Single core implementation much slower than the multi core version
        input : columns to extract
        output: data frame with the column and the fields size = (3230,len(columns))
        """
        self.ahrf_columns = columns

        start_time = time.time()
        with open(self.file_path, 'rb') as ahrf_file:
            ahrf_lines = ahrf_file.readlines()
            ahrf_data = self.create_ahrf_frame(ahrf_lines)
        # Ensure that the total number of records is 3230 as per the 
        # technical documentation
        assert ahrf_data.shape[0] == 3230
        if not os.path.exists('DATA/'):
            os.mkdir('DATA/')
        ahrf_data.to_csv('DATA/ahrf_data.csv', index=False)
        end_time = time.time()
        print('Total time taken %.4f s' % (end_time - start_time))
        return ahrf_data

    def _divide_data_set(self):
        """Divides the AHRF into blocks for each worker to process
        """
        divide = 3230 / self.num_cores
        index_list = [slice(x * divide, (x + 1) * divide) for x in range(self.num_cores - 1)]
        index_list.extend([slice((self.num_cores - 1) * divide, None)])
        print(index_list)
        return index_list

    def create_ahrf_frame(self, ahrf_lines):
        ahrf_data = pd.DataFrame(columns=self.ahrf_columns)
        ctr = 0
        for line in ahrf_lines:
            for c_name in self.ahrf_columns:
                start_pos = self.meta_data[self.meta_data['FieldName'] == c_name].Position.values[0] - 1
                temp_end_pos = self.meta_data[self.meta_data['FieldName'] == c_name].FieldLength.values[0]
                end_pos = start_pos + int(round(temp_end_pos))
                # check for decimal multiplier
                if round(temp_end_pos % 1.0, 1) > 0.0:
                    multi = 0.1 ** (round(temp_end_pos % 1.0, 1) * 10)
                    if line[start_pos:end_pos].strip() != '.':
                        ahrf_data.loc[ctr, c_name] = int(line[start_pos:end_pos]) * multi
                    else:
                        ahrf_data.loc[ctr, c_name] = line[start_pos:end_pos]
                else:
                    ahrf_data.loc[ctr, c_name] = line[start_pos:end_pos]
            ctr += 1
        return ahrf_data

    def parse_ahrf_file_multicore(self, ahrf_columns=[]):
        """parses the county level ascii AHRF and returns information
        as a dataframe. 
        input : columns to extract (look at meta_data.csv)
        output: data frame with the column and the fields size = (3230,len(columns))
        """
        self.ahrf_columns = ahrf_columns
        print('Loading variables to a DataFrame...')
        start_time = time.time()
        p = multiprocessing.Pool(self.num_cores)
        with open(self.file_path, 'rb') as ahrf_file:
            ahrf_lines = ahrf_file.readlines()
            slices = self._divide_data_set()
            ahrf_blocks = [ahrf_lines[sl] for sl in slices]
            frames = p.map(unwrap_self_f, zip([self] * len(ahrf_blocks), ahrf_blocks))

        ahrf_data = pd.concat(frames, ignore_index=True)
        # Ensure that the total number of records is 3230 as per the 
        # technical documentation
        assert ahrf_data.shape[0] == 3230
        if not os.path.exists('DATA/'):
            os.mkdir('DATA/')
        ahrf_data.to_csv('DATA/ahrf_data.csv', index=False)
        print('Data frame saved at ' + 'DATA/ahrf_data.csv')
        end_time = time.time()
        print('Total time taken %.4f s' % (end_time - start_time))
        return ahrf_data


def main():
    employment_columns = ["UnemploymentRate,16+2014", "MedcreBenefHospReadmissRateFeeforService2014"]
    ahrf_parser = parse_AHRF_ascii(num_cores=6,
                                   ascii_file_path="DATA/ahrf2016.asc",
                                   sas_file_path="DOC/ahrf2015-16.sas")
    data_frame = ahrf_parser.parse_ahrf_file_multicore(employment_columns)

    print(data_frame)


if __name__ == '__main__':
    main()
