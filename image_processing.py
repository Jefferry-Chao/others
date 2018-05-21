# -*- coding: utf-8 -*-
#*************************************************************************
#***File Name: figure.py
#***Author: Zhonghai Zhao
#***Mail: zhaozhonghi@126.com 
#***Created Time: 2018年03月25日 星期日 14时39分05秒
#*************************************************************************
# add line
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
    # make movie
    def make_movie(self, info = 'Current_jx', filename = 'default', path = 'current', \
                   formats='GIF', duration=0.5, imagform='PNG', fps=4):
        '''
        This function is used to convert pictures to movie.
        Parameters:
            info          - key word about pictures to read from path.
            filename      - the movie filename to be saved.
            path          - path for pictures to read from.
            formats       - movie formats to save, as, 'GIF', 'AVI', 'MP4' etc.
            duration      - float or int, duration for gif save.
            fps           - int, fps for movie save.
            imagform      - image' format which to be read.
        Returns:
            None.
        Raises:
            KeyError.
        '''
        import os
        import imageio
        # get file path
        if(path == 'current'):
            path = os.getcwd() + '/'
        else:
            path = path + '/'
        # read file list in path
        filelist = os.listdir(path)
        files = []
        for each in filelist:
            extension = os.path.splitext(each)[1][1:]
            if((info.upper() in each.upper()) and (extension.upper() == imagform.upper())):
                files.append(each)
        files = sorted(files)
        # read images in files
        images = []
        try:
            for each in files:
                images.append(imageio.imread(path + each))
        except IOError, ValueError:
            print 'Error: No such file!'
        else:
            print 'Read images, done!'
        # save movie
        if(filename == 'default'):
            filename = path + info + '.' + formats.lower()
        else:
            filename = path + filename + '.' + formats.lower()
        # for different formats
        if(formats.upper() == 'GIF'):
            imageio.mimsave(filename, images, formats.upper(), duration=duration)
        elif(formats.upper() == 'AVI'):
            imageio.mimsave(filename, images, formats.upper(), fps=fps)
        elif(formats.upper() == 'MP4'):
            imageio.mimsave(filename, images, formats.upper(), fps=fps)
        else:
            print 'Nothing to be done, format error!'
        #return none

