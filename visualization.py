import pandas as pd
import seaborn as sns


def preprocess_dataset(path):
    """
     Preprocess Monatszahlen Verkehrsunfälle dataset

    param path: string
    referencing the location of the Monatszahlen Verkehrsunfälle dataset
    :return: tuple
    dataframe and unique categories in MONATSZAHL column
    """
    data = pd.read_csv(path, parse_dates=['MONAT'])
    data['MONAT'] = pd.to_datetime(data['MONAT'], errors='coerce', format='%Y%m')
    data = data.dropna()
    unique_category = data['MONATSZAHL'].unique()
    return data, unique_category


def category(data, unique_category):
    """
    Get the different accident types in each categories

    :param data: dataframe
    :param unique_category: ndarray
    :return: tuple
    """
    category_accident_type_dataset = {}
    category_accident_type_names = {}
    for category_name in unique_category:
        category_name_df = data[data['MONATSZAHL'] == category_name]
        unique_accident_type = category_name_df['AUSPRAEGUNG'].unique()
        category_accident_type_names[f'{category_name}'] = unique_accident_type
        accident_type = {}
        for accident_name in unique_accident_type:
            accident_name_df = category_name_df[category_name_df['AUSPRAEGUNG'] == accident_name]
            accident_type[f'{accident_name}'] = accident_name_df
        category_accident_type_dataset[f'{category_name}'] = accident_type
    return category_accident_type_dataset, category_accident_type_names


def visualization(dataset, category_accident_type_names, category_name, axs):
    """
        Plot  Accident Type per Category Name
    :param dataset: nested dictionary
    :param category_accident_type_names: dictionary
    :param category_name: string
    :param axs:
    :return: None
    """
    for name in category_accident_type_names[category_name]:
        df = dataset[category_name][name]
        sns.lineplot(data=df, x='MONAT', y='WERT', ax=axs, legend='auto', label=f'{name}')
        axs.set(xlabel='TIME', ylabel='WERT')
        axs.set_title(f'{category_name}')
        axs.legend()
