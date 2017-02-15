import os
from datetime import datetime

version = 0
save_dir = os.path.expanduser("~") + "/notebooks/saves/V{}/".format(version)


def save_model_and_df(model, df, size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part):
    name = get_save_name(size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    model.save(save_dir + name + ".model")
    df.to_hdf(save_dir + name + ".hdf5", 'name', complevel=9, complib='blosc')


def get_save_name(size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part):
    name = "size-"
    name += str(size)
    name += "-gamma-"
    name += '{:.2f}'.format(gamma)
    name += "-start_epoch-"
    name += str(start_epoch)
    name += "-end_epoch-"
    name += str(end_epoch)
    name += "-random_epochs-"
    name += str(random_epochs)
    name += "-batch_size-"
    name += str(batch_size)
    name += "-part-"
    name += str(part)
    name += "-date-"
    name += datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return name


def get_parameters(name: str):
    s = name.split("/")[-1].split("\\")[-1].rsplit(".", 1)[0]
    l = s.split("-")
    return int(l[l.index("size") + 1]), \
           float(l[l.index("gamma") + 1]), \
           int(l[l.index("start_epoch") + 1]), \
           int(l[l.index("end_epoch") + 1]), \
           int(l[l.index("random_epochs") + 1]), \
           int(l[l.index("batch_size") + 1]), \
           int(l[l.index("part") + 1])
