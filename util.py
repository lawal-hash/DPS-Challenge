import pandas as pd

def load_data(path):
    Alkoholunfalle_df = pd.read_csv(path, parse_dates=['MONAT'])
    Alkoholunfalle_df['MONAT'] = pd.to_datetime(Alkoholunfalle_df['MONAT'], errors='coerce', format='%Y%m')
    Alkoholunfalle_df = Alkoholunfalle_df.reindex(index=Alkoholunfalle_df.index[::-1])
    Alkoholunfalle_df.reset_index(inplace=True, drop=True)
    Alkoholunfalle_df = Alkoholunfalle_df.set_index(['MONAT'])
    Alkoholunfalle_df.sort_index(ascending=True, inplace=True)
    return Alkoholunfalle_df


