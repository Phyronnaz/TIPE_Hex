import os
from datetime import datetime

version = 4
save_dir = os.path.expanduser("~") + "/Hex/V{}/".format(version)


def save_model_and_df(model, df, size, epochs, memory_size, batch_size, comment):
    """
    Save a model and a dataframe
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save model
    name = get_save_name(size, epochs, memory_size, batch_size, comment)
    model.save(save_dir + name + ".model")

    # Save dataframe
    name = get_save_name(size, epochs, memory_size, batch_size, comment)
    df.to_hdf(save_dir + name + ".hdf5", 'name', complevel=9, complib='blosc')


def get_save_name(size, epochs, memory_size, batch_size, comment):
    """
    Get the save name corresponding to the arguments
    :return: name
    """
    name = "size-"
    name += str(size)
    name += "-epochs-"
    name += str(epochs)
    name += "-memory_size-"
    name += str(memory_size)
    name += "-batch_size-"
    name += str(batch_size)
    name += "-comment-"
    name += str(comment).replace("-", "_")
    name += "-date-"
    name += datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return name


def get_parameters(name: str):
    """
    Return the parameters of a name
    :param name: can be a path
    :return: size, epochs, memory_size, batch_size, comment
    """
    s = name.split("/")[-1].split("\\")[-1].rsplit(".", 1)[0]
    l = s.split("-")

    return int(l[l.index("size") + 1]), \
           float(l[l.index("epochs") + 1]), \
           int(l[l.index("memory_size") + 1]), \
           int(l[l.index("batch_size") + 1]), \
           l[l.index("comment") + 1]

def get_parameters_dict(name: str):
    size, epochs, memory_size, batch_size, comment = get_parameters(name)
    return {"size": size, "epochs": epochs,"memory_size": memory_size,  "batch_size": batch_size, "comment": comment}


def get_pretty_name(*parameters):
    """
    Return pretty name
    :param: parameters: size, epochs, memory_size, batch_size, comment
    """
    return "Size {}; Epochs {}; Memory Size {}; Batch Size {}; Comment {}".format(*parameters)
