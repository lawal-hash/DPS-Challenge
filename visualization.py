import pandas as pd
import seaborn as sns


def load_dataset(path):
    """

    param path:
    :return:
    """
    data = pd.read_csv(path, parse_dates=['MONAT'])
    data['MONAT'] = pd.to_datetime(data['MONAT'], errors='coerce', format='%Y%m')
    data = data.dropna()
    unique_class = data['MONATSZAHL'].unique()
    return data, unique_class


def category(data, unique_class):
    """
    :param data:
    :param unique_class:
    :return:
    """
    dict_category = {}
    dict_category_unique = {}
    for class_name in unique_class:
        category_df = data[data['MONATSZAHL'] == class_name]
        accident_type = category_df['AUSPRAEGUNG'].unique()
        dict_category_unique[f'{class_name}'] = accident_type
        accident_dict = {}
        for accident_name in accident_type:
            accident_name_df = category_df[category_df['AUSPRAEGUNG'] == accident_name]
            accident_dict[f'{accident_name}'] = accident_name_df
        dict_category[f'{class_name}'] = accident_dict
    return dict_category, dict_category_unique


def visualization(dict_category, dict_category_unique, unique_class_name, axs):
    """

    :param dict_category:
    :param dict_category_unique:
    :param unique_class_name:
    :param axs:
    :return:
    """
    for name in dict_category_unique[unique_class_name]:
        df = dict_category[unique_class_name][name]
        sns.lineplot(data=df, x='MONAT', y='WERT', ax=axs, legend='auto', label=f'{name}')
        axs.set(xlabel='TIME', ylabel='WERT')
        axs.set_title(f'{unique_class_name}')
        axs.legend()
