# -*- coding:UTF-8 -*-
def _init():
    #Initialize a global dictionary
    global _global_dict
    _global_dict = {}
    _global_dict['root'] = "10.10.1.104"
    _global_dict['ca'] = "10.10.1.105"
    _global_dict['test'] = "10.10.1.106"
def set_value(key,value):
    _global_dict[key] = value
    
def get_value(key):
    try:
        return _global_dict[key]
    except KeyError as e:
        print(e)