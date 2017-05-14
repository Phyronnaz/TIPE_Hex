import os
from datetime import datetime

version = 4
save_dir = os.path.expanduser("~") + "/Hex/V{}/".format(version)


def save_models_and_df(models, df, size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs,
                       train_epochs, memory_size, q_players, comment):
    """
    Save a model and a dataframe
    :param models: models
    :param df: dataframe
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save models
    for i in range(2):
        if models[i] is not None:
            name = get_save_name(size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs,
                                 train_epochs, memory_size, q_players, comment, i)
            models[i].save(save_dir + name + ".model")

    # Save dataframe
    name = get_save_name(size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs,
                         memory_size, q_players, comment)
    df.to_hdf(save_dir + name + ".hdf5", 'name', complevel=9, complib='blosc')


def get_save_name(size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs,
                  memory_size, q_players, comment, player="all"):
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
    name += "-exploration_epochs-"
    name += str(exploration_epochs)
    name += "-train_epochs-"
    name += str(train_epochs)
    name += "-memory_size-"
    name += str(memory_size)
    name += "-q_players-"
    name += str(q_players)
    name += "-comment-"
    name += str(comment).replace("-", "_")
    name += "-player-"
    name += str(player)
    name += "-date-"
    name += datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return name


def get_parameters(name: str):
    """
    Return the parameters of a name
    :param name: can be a path
    :return: size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size, q_players, comment, player
    """
    s = name.split("/")[-1].split("\\")[-1].rsplit(".", 1)[0]
    l = s.split("-")

    return int(l[l.index("size") + 1]), \
           float(l[l.index("gamma") + 1]), \
           int(l[l.index("batch_size") + 1]), \
           float(l[l.index("initial_epsilon") + 1]), \
           float(l[l.index("final_epsilon") + 1]), \
           int(l[l.index("exploration_epochs") + 1]), \
           int(l[l.index("train_epochs") + 1]), \
           int(l[l.index("memory_size") + 1]), \
           [0, 1] if len(l[l.index("q_players") + 1]) == 6 else [int(l[l.index("q_players") + 1][1])], \
           l[l.index("comment") + 1], \
           l[l.index("player") + 1]


def get_parameters_dict(name: str):
    s, g, bs, ie, fe, ee, te, ms, qp, com, p = get_parameters(name)
    return {"size": s, "gamma": g, "batch_size": bs, "initial_epsilon": ie, "final_epsilon": fe,
            "exploration_epochs": ee, "train_epochs": te, "memory_size": ms, "q_players": qp, "comment": com,
            "player": p}


def get_pretty_name(*parameters):
    """
    Return pretty name
    :param: parameters: size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size, q_players, player
    """
    return "Size {}; Gamma {}; Batch Size {}; Epsilon {}-{}; Exploration epochs {}; Train epochs {}; Memory Size {}; Q Players: {}; Comment: {}; Player {}".format(
        *parameters)
