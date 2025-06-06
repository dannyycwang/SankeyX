import pandas as pd
import ast

def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except:
        return val

def load_and_preprocess(filepath):
    df = pd.read_csv(filepath)
    df['truncated_sequence'] = df['truncated_sequence'].apply(safe_eval)
    return df

