import easygui
import h5py

path = easygui.fileopenbox(default="/home/victor/Hex/")

with h5py.File(path, 'a') as f:
    if 'optimizer_weights' in f.keys():
        del f['optimizer_weights']
