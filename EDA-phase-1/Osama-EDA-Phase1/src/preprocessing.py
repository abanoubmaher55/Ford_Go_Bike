import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_file(path:str):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def Check_data_type(df):
    y = []
    for x in df.columns:
        if df[x].nunique()<=3:
            y.append("like categorical")
        else:
            y.append("not like categorical")
    Uni_col = df.nunique()
    dtype = df.dtypes
    infoo = pd.DataFrame({"num_uni": Uni_col,"types":dtype,"stat":y}).T
    return infoo     

def view(df):
    Uni_col = df.nunique()
    dtype = df.dtypes
    infoo = pd.DataFrame({"num_uni": Uni_col,"types":dtype}).T
    return infoo     

def Ratio(df):
    null= df.isnull().sum()
    ratio = null / df.shape[0] *100
    return pd.DataFrame({"Null_sum":null,"Ratio":ratio})


def handle_outliers(df):
    col_name = df.select_dtypes("number").columns
    for col in col_name:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        # print(IQR)
        Lower_Fence = Q1 - 1.5*IQR
        Upper_Fence = Q3 + 1.5*IQR
        
        df[col] = df[col].clip(Lower_Fence, Upper_Fence)
    return df



def check_outliers(df):
    num_cols = df.select_dtypes('number').columns
    plt.figure(figsize=(8,1))
    for i , col in enumerate(num_cols):
        plt.subplot(1,len(num_cols), i+1)
        sns.boxplot(df[col], orient="h")
        plt.title(f"{col} Boxplot")
        
        
def drop_outliers(df,col):
    for c in col:
        Q1 = df[c].quantile(0.25)
        Q3 = df[c].quantile(0.75)
        IQR = Q3 - Q1

        Lower_Fence = Q1 - 1.5 * IQR
        Upper_Fence = Q3 + 1.5 * IQR

        df = df[(df[c] >= Lower_Fence) & (df[c] <= Upper_Fence)]
    return df