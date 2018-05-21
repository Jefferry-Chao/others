# -*- coding: utf-8 -*-
#*************************************************************************
#***File Name: figure.py
#***Author: Zhonghai Zhao
#***Mail: zhaozhonghi@126.com 
#***Created Time: 2018年03月25日 星期日 14时39分05秒
#*************************************************************************
class image_processing(object):
    '''
    This class contains some image processing function.
    '''
    # initialization
    def __init__(self):
        pass
    # add number
    def add_number(self, filename='04-16.png', word='a)', dpix=8, dpiy=6, ifdisplay=True):
        '''
        This function is used to ordering figure.
        Parameters:
            filename      - figure name.
            word          - number word.
            dpix          - dpi x.
            dpiy          - dpi y.
            ifdisplay     - if display figure.
        Returns:
            None.
        Raises:
            KeyError.
        '''
        import os
        import matplotlib.pyplot as plt
        import matplotlib.image as image
        figure = image.imread(filename)
        plt.figure(figsize=(dpix, dpiy))
        plt.imshow(figure)
        plt.text(20, 80, word, fontsize=30)
        plt.axis('off')
        if (ifdisplay == True):
            plt.show()
        else:
            name = os.path.splitext(filename)
            os.rename(filename, name[0] + '_old' + name[1])
            plt.savefig(filename, dpi=120)

