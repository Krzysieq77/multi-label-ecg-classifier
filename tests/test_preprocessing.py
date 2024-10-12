import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
from preprocessing import scale_age, load_raw_data, preprocess_data

class TestPreprocessing(unittest.TestCase):

    def test_scale_age(self):
        # Test case where age is greater than 89
        self.assertEqual(scale_age(90), -210)
        # Test case where age is less than 89
        self.assertEqual(scale_age(50), 50)

    @patch('preprocessing.wfdb.rdsamp')
    def test_load_raw_data(self, mock_rdsamp):
        # Mocking wfdb.rdsamp to return dummy data for test
        mock_rdsamp.return_value = (np.random.rand(5000, 12), {})
        
        # Create a mock DataFrame for testing the raw data loading function
        df = pd.DataFrame({'filename_lr': ['00001_lr'], 'filename_hr': ['00001_hr']})
        path = 'path_to_test_data/'  # Test data path

        # Simulate loading data with sampling rate of 500 Hz
        result_500 = load_raw_data(df, sampling_rate=500, path=path)
        self.assertIsInstance(result_500, np.ndarray)
        self.assertEqual(result_500.shape[1], 12)  # Assuming 12 leads in the ECG data

    @patch('preprocessing.pd.read_csv')
    def test_preprocess_data(self, mock_read_csv):
        # Mocking pd.read_csv to return dummy DataFrame for test
        mock_read_csv.return_value = pd.DataFrame({
            'ecg_id': [1],
            'scp_codes': [{'NORM': 1}],
            'age': [60],
            'sex': [1],
            'strat_fold': [1],
            'filename_lr': ['00001_lr'],
            'filename_hr': ['00001_hr']
        })
        
        # Simulate paths to dataset and scp_statements.csv for testing
        data_path = 'path_to_test_data/ptbxl_database.csv'
        scp_statements_path = 'path_to_test_data/scp_statements.csv'
        output_path = 'output_test_data.csv'
        sampling_rate = 500
        path = 'path_to_test_data/'

        # Preprocess the data
        X_ecg, X_features, data, Y = preprocess_data(data_path, scp_statements_path, output_path, sampling_rate, path)

        # Check that X_ecg and X_features are NumPy arrays and DataFrames
        self.assertIsInstance(X_ecg, np.ndarray)
        self.assertIsInstance(X_features, pd.DataFrame)
        self.assertEqual(X_ecg.shape[1], 12)  # 12 leads in ECG data
        self.assertTrue('age' in X_features.columns)  # Ensure 'age' is included

if __name__ == '__main__':
    unittest.main()
