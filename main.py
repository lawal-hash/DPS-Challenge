import visualization as vs
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    dataset, categories = vs.preprocess_dataset('monatszahlen2112_verkehrsunfaelle.csv')
    category_dict, unique_category_dict = vs.category(dataset, categories)
    fig, axs = plt.subplots(len(categories), sharex=True)
    fig.set_size_inches(18.5, 10.5)
    plt.suptitle('Visualisation of the Number of Accidents Per Category')
    for i in range(len(categories)):
        vs.visualization(category_dict, unique_category_dict, categories[i], axs[i])
    # plt.show()
    copy = np.random.randint(100, size=1)
    plt.savefig(f'Images/MONATSZAHL_{int(copy)}.png')
