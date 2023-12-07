import pandas as pd

class DataHandler:

    @staticmethod
    def load_data(file_name):

        return pd.read_json(file_name, lines=True)

    @staticmethod
    def filter_data(file_name,doc_uuid):

        df = pd.read_json(file_name, lines=True)
        df = df[df['subject_doc_id'] == doc_uuid] if doc_uuid else df
        return df
