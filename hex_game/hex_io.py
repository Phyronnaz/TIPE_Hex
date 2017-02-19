import os
from datetime import datetime

version = 0
save_dir = os.path.expanduser("~") + "/notebooks/saves/V{}/".format(version)


def save_model_and_df(model, df, size, gamma, batch_size, initial_epsilon, final_epsilon, random_opponent,
                      exploration_epochs, train_epochs, memory_size):
    """
    Save a model and a dataframe
    :param model: model
    :param df: dataframe
    """
    name = get_save_name(size, gamma, batch_size, initial_epsilon, final_epsilon, random_opponent, exploration_epochs,
                         train_epochs, memory_size)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    model.save(save_dir + name + ".model")
    df.to_hdf(save_dir + name + ".hdf5", 'name', complevel=9, complib='blosc')
    del model
    del df


def get_save_name(size, gamma, batch_size, initial_epsilon, final_epsilon, random_opponent, exploration_epochs,
                  train_epochs, memory_size):
    """
    Get the save name corresponding to the arguments
    :return: name
    """
    name = "size-"
    name += str(size)
    name += "-gamma-"
    name += '{:.2f}'.format(gamma)
    name += "-batch_size-"
    name += str(batch_size)
    name += "-initial_epsilon-"
    name += '{:.5f}'.format(initial_epsilon)
    name += "-final_epsilon-"
    name += '{:.5f}'.format(final_epsilon)
    name += "-random_opponent-"
    name += str(random_opponent)
    name += "-exploration_epochs-"
    name += str(exploration_epochs)
    name += "-train_epochs-"
    name += str(train_epochs)
    name += "-memory_size-"
    name += str(memory_size)
    name += "-date-"
    name += datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return name


def get_parameters(name: str):
    """
    Return the parameters of a name
    :param name: can be a path
    :return: size, gamma, batch_size, initial_epsilon, final_epsilon, random_opponent, exploration_epochs, train_epochs, memory_size
    """
    s = name.split("/")[-1].split("\\")[-1].rsplit(".", 1)[0]
    l = s.split("-")
    return int(l[l.index("size") + 1]), \
           float(l[l.index("gamma") + 1]), \
           int(l[l.index("batch_size") + 1]), \
           float(l[l.index("initial_epsilon") + 1]), \
           float(l[l.index("final_epsilon") + 1]), \
           bool(l[l.index("random_opponent") + 1]), \
           int(l[l.index("exploration_epochs") + 1]), \
           int(l[l.index("train_epochs") + 1]), \
           int(l[l.index("memory_size") + 1])


def get_pretty_name(*parameters):
    """
    Return pretty name
    :param: parameters: size, gamma, batch_size, initial_epsilon, final_epsilon, random_opponent, exploration_epochs, train_epochs, memory_size
    """
    return "Size {}; Gamma {}; Batch Size {}; Epsilon {}-{}; Random opponent: {}; Exploration epochs {}; Train epochs {}; Memory Size {}".format(*parameters)
