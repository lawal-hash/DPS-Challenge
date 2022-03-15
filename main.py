import visualization as vs
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dataset, categories = vs.load_dataset('monatszahlen2112_verkehrsunfaelle.csv')
    category_dict, unique_category_dict = vs.category(dataset, categories)
    fig, axs = plt.subplots(len(categories), sharex=True)
    fig.set_size_inches(18.5, 10.5)
    for i in range(len(categories)):
        vs.visualization(category_dict, unique_category_dict, categories[i], axs[i])
    # plt.show()
    plt.savefig('Images/MONATSZAHL.png')