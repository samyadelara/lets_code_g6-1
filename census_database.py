# census_database class - projeto pandas - Santander Coders 2021 - G6 (by Samya)
import os
import pandas as pd

class Database():
    
    def __init__(self):
        self.data = self._readmerge_files() #create database
        self.quanti = self._quanti_vars() #create attribute QUANTITATIVE var
        self.quali = self._quali_vars() #create attribute QUANLITATIVE var
        print('Census data READY!')
    
    ## methods for object initialization ###################
    def _list_files(self):
        file_list = sorted([i for i in os.listdir('input_files') if i[-3:] == 'csv']) #check files in local dir   
        return file_list
    
    def _readmerge_files(self):
        self.file_list = self._list_files() #list of files with census data
        
        data = pd.DataFrame()
        for file in self.file_list:
            columns_data = set(data.columns)
            file_path = os.path.join('input_files', file)
            
            file_content = pd.read_csv(file_path, delimiter = ';') #read file content
            file_columns = set(file_content.columns) #columns in read file
            
            #check for common columns data & file
            common_columns = columns_data.intersection(file_columns)
            are_commun_columns = len(common_columns) > 0
            
            if not are_commun_columns:
                data = pd.concat([data, file_content], axis = 1) #If not = concat by columns
            else:
                data = data.merge(file_content, on = list(common_columns)) #If does = merge on those
        
        return data
    
    def _quanti_vars(self): #check quantitative variables in columns
        data = self.data
        quanti = data._get_numeric_data().columns
        quanti = quanti.drop(['ID', 'Electricity'])
        return set(quanti)
    
    def _quali_vars(self): #check qualitative variables in columns
        data = self.data
        columns = set(data.columns)
        quali = columns - self.quanti - {'ID'}
        return quali