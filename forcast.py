import pandas as pd
import statsmodels.api as sm


def preprocess(path):
    insgesamt_df = pd.read_csv(path)
    insgesamt_df = insgesamt_df.reindex(index=insgesamt_df.index[::-1])
    insgesamt_df.reset_index(inplace=True, drop=True)
    insgesamt_df = insgesamt_df.set_index(["MONAT"])
    return insgesamt_df
