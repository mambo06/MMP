# data_operations/data_loader.py
import pandas as pd
import numpy as np
from typing import Tuple, List, Union, Dict, Any
from sklearn.preprocessing import OneHotEncoder
import os
from io import StringIO
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_calls.getData import find_node_by_name as getNode

from analytics.sklearnpredictor import train_model

class DataLoader:
    def __init__(self, trainme=True):
        """
        Initialize DataLoader with empty mappings.
        Data sources will be added incrementally using add_data_source method.
        """
        self.data_paths = {}  # Store file paths
        self.data_aliases = {}  # Store aliases for data sources
        self.loaded_data = {}  # Store loaded data
        self.data = None
        self.trainme = trainme
        # self.query = query
        # load initial testing
        self.load_and_process_data(query= 'sample_data')
        
        

    def train_data(self):
        temp = train_model(self.data)
        return temp

    def load_and_process_data(self, query ) -> Union[Tuple[np.ndarray, List[str]], str]:
        self.graph = getNode(query)
        self.load_data()
        tmp = train_model(self.data) if self.trainme else self.data
        # yield str(tmp)
        print(tmp)
        return tmp

    def load_data(self) -> Union[Tuple[np.ndarray, List[str]], str]:
        # Check if input is a known shape ID or alias
        shape_config = self.graph.copy()

        if shape_config.get('type') != 'file':
            return False
            
        shape_id = shape_config.get('name')
        import_path = shape_config.get('importPath', {})
        file_path = import_path.get('module', '')
        aliases = import_path.get('aliases', '')
        # self.data_paths[shape_id] = file_path

        # if input_identifier in self.data_paths:
        #     file_path = self.data_paths[input_identifier]
        # elif input_identifier in self.data_aliases:
        #     shape_id = self.data_aliases[input_identifier]
        #     file_path = self.data_paths[shape_id]
        # else:
        #     file_path = input_identifier
            
        # Check if input is a file path
        # is_file = os.path.isfile(file_path if isinstance(file_path, str) else input_identifier)
        
        # Get content
        # if is_file:
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filepath = '/'.join(filepath.split(os.sep)) + '/'
        filepath +=  file_path
        with open(filepath if isinstance(file_path, str) else input_identifier, 'r', encoding='utf-8') as file:
            content = file.read()
        # else:
        #     content = input_identifier
            
        # Store in loaded_data if it's from a known shape
        # if input_identifier in self.data_paths or input_identifier in self.data_aliases:
        #     self.loaded_data[input_identifier] = content

        # Process content
        self.data = self._process_content(content)
        # return self.data
    
    def _process_content(self, content: str) -> Union[Tuple[np.ndarray, List[str]], str]:
        """
        Process the content and determine if it's CSV or text.
        
        Args:
            content: String content to process
            
        Returns:
            Processed data or original text
        """
        lines = content.strip().split('\n')
        if len(lines) > 1:
            potential_delimiters = [',', ';', '\t', '|']
            has_delimiters = any(
                any(delim in line for delim in potential_delimiters)
                for line in lines[:5]
            )
            if not has_delimiters: 
                return content, 'text'

        try:
            df = pd.read_csv(StringIO(content))
            return self._process_dataframe(df)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            return content, 'error'
    
    def _process_dataframe(self, df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
        """
        Process a DataFrame with one-hot encoding for categorical columns.
        
        Args:
            df: pandas DataFrame to process
            
        Returns:
            tuple: (processed numpy array, list of column names)
        """
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        processed_data = []
        final_columns = []
        
        if len(numeric_cols) > 0:
            numeric_data = df[numeric_cols].values
            if len(numeric_data.shape) == 1:
                numeric_data = numeric_data.reshape(-1, 1)
            processed_data.append(numeric_data)
            final_columns.extend(numeric_cols.tolist())
        
        if len(categorical_cols) > 0:
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            categorical_data = df[categorical_cols].values
            if len(categorical_data.shape) == 1:
                categorical_data = categorical_data.reshape(-1, 1)
            categorical_data = encoder.fit_transform(categorical_data)
            
            for i, col in enumerate(categorical_cols):
                categories = encoder.categories_[i]
                encoded_cols = [f"{col}_{cat}" for cat in categories]
                final_columns.extend(encoded_cols)
            
            processed_data.append(categorical_data)
        
        if processed_data:
            processed_data = [arr if len(arr.shape) == 2 else arr.reshape(-1, 1) 
                             for arr in processed_data]
            final_data = np.hstack(processed_data)
        else:
            final_data = np.array([])
            
        if len(final_data.shape) == 1:
            final_data = final_data.reshape(-1, 1)
        # print(final_data, final_columns)
        
        return final_data, final_columns

    
    


if __name__ == "__main__":
    DataLoader()
