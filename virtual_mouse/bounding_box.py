import numpy as np

def get_valid_box(bbox: tuple, centers: tuple)->tuple:
    x, y, w, h = bbox
    c_x, c_y = centers
    
    #basically use half upper of bbox
    
    width_ratio = 0.35
    height_ratio = 0.35
    
    adap_x = x + width_ratio * w
    adap_y = y + (1-height_ratio) * h
    
    adap_w = (1-width_ratio) * w
    adap_h = (1-height_ratio) * h
    
    return (adap_x, adap_y, adap_w, adap_h)