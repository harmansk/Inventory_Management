import os
import pandas as pd
import openpyxl

def load_inventory_from_excel(file_name, output_dataframe = False):
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
        print("Number Existing Records in Inventory:",df.shape)
        if output_dataframe:
            return df
        return df.to_dict(orient="records")
    return []

def save_inventory_to_excel(inventory_array, file_name):
    df = pd.DataFrame([item.dict() for item in inventory_array])
    df.insert(0, 'record_id', range(1, len(df) + 1))  # Add record_id column starting from 1
    print(df)
    df.to_excel(file_name, index=False)