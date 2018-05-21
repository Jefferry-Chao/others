# -*- coding: utf-8 -*-
#*************************************************************************
#***File Name: hdf_class.py
#***Author: Zhonghai Zhao
#***Mail: zhaozhonghi@126.com 
#***Created Time: 2018年03月25日 星期日 14时39分05秒
#*************************************************************************
class hdf_class(object):
    '''
    This class contain some functions to visualize hdf data file.
    '''
#initialization
    def __init__(self):
        pass
#get data from a hdf file
    def get_data(self,filename):
        '''
        This function is used to get data dictionary from a hdf file.
        parameters:
        filename----a hdf file's name,such as '***.h5'.
        '''
        import h5py
        data_dict = h5py.File(filename)
        return data_dict
#test if the input field contained in the hdf file.
    def get_field(self,field='bx',keys=["BX"]):
        '''
        This function is used to test if the field contained in hdf file.
        parameters:
        field-------the input field name, default:'bx'
        keys--------the keys get from hdf file, default:'BX'
        '''
        import sys
        ifcontain = False
        for eachone in keys:
            if(field.upper() in eachone.upper()):
                ifcontain = True
                field = eachone.upper()
                break
        if(ifcontain == False):
            print "There is not such a field named %s."%(field)
            sys.exit(0)
        else:
            return str(field)
#use this function to chose a proper normalization constant,
    def get_constant(self,field='BX'):
        '''
        This function is used to chose a proper constant.
        parameter:
        field-------field name, default:'BX'
        '''
        from constants import Constants as const
        normal1 = {"bxbybz":const.B0,"exeyez":const.E0,\
                  "jxjyjz":const.J0,"ekbar":const.T0,"axis":const.D0}
        normal2 = {"density":const.N0,"temperature":const.T0,"xz_u":const.V0,\
                   "xz_t":(const.N0)*(const.T0)}
        normal1_s = normal1.keys()
        normal2_s = normal2.keys()
        for eachone in normal1_s:
            if((field[:2]).upper() in eachone.upper()):
                factor = normal1[eachone]
                break
        for eachone in normal2_s:
            if(eachone.upper() in field.upper()):
                factor = normal2[eachone]
        return factor
#use this function todelete grid and time
    def del_str(self,keys):
        '''
        This function is used to delete grid and time keys.
        parameters:
        keys--------keys from hdf file
        '''
        todel = ["X","Y","TIME"]
        for i in range(3):
            n = len(keys)
            for j in range(n):
                if(todel[i] == keys[j]):
                    del keys[j]
                    break
        return keys
#if magnitude is True, this function will return a vector;s module.
    def get_module(self,data_dict,field='magnetic',nrange=[1,1,2]):
        '''
        This function is used to calculate a vector's module,
        parameters:
        data_dict---a data dictionary get from a hdf file.
        field-------a vector field, default:'magnetic'
        number------file number
        '''
        import sys
        import numpy as np
        convert = {"magnetic":'BXBYBZ',"electric":'EXEYEZ',\
                   "current":'JXJYJZ'}
        keys = data_dict.keys()
        #delete grid and time
        keys = hdf_class.del_str(self,keys)
        s = convert.keys()
        #test if field is a vector.
        if(field in s):
            vector = convert[field]
        else:
            print "The input %s is not a vector!"%(field)
            sys.exit(0)
        #if True, calculate the vector's module.
        mode = 0
        const = 0
        for eachone in keys:
            if(eachone.upper() in vector):
                const += 1
                array = data_dict[eachone.upper()]
                array = np.array(array)
                if(len(array.shape) == 2):
                    array = array
                if(len(array.shape) == 3):
                    array = array[nrange[0]-nrange[1],:,:]
                mode = mode + array*array
        #test if there are enough components.
        if(const < 3):
            print "Warning! There is not enough components in vector!"
        array = np.sqrt(mode)
        return array
#if magnitudeis 'True', then convert field
    def convert_field(sefl,field='magnetic'):
        '''
        This function is used to convert field when magnitude is True.
        parameters:
        field-------field to be converted, defualt:'magnetic'
        '''
        import sys
        convert = {"magnetic":'BX',"electric":'EX',"current":'JX'}
        keys = convert.keys()
        if(field not in keys):
            print "There is not a vector named %s."%(field)
            sys.exit(0)
        else:
            return convert[field]
#use this function to print time information and chose one of them.
    def get_time(self,data_dict,field='BX'):
        '''
        This function is to print time information of the field.
        One can chose one of the to contonue.
        parameters:
        data_dict---data dictionary
        field-------the field, default:'BX'
        '''
        time = data_dict['TIME']
        for i in range(len(time)):
            if(field == time[i,0]):
                start = int(time[i,1])
                end = int(time[i,2])
                break
        print "The range of files in %d to %d, \
 please chose one between them"%(start,end)
        number = int(raw_input("Enter:"))
        if(number in range(start,end+1)):
            return [number,start,end]
        else:
            print "Not invalid input, out of range!"
            return None
#input line plot index
    def get_line(self,data_dict,field='BX',axes='x',nrange=[1,2,1]):
        '''
        This function is used to input index.
        parameters:
        data_dict---data dictionary.
        field-------field, defautl:'BX'.
        axes--------axes, default:'x'
        '''
        import numpy as np
        data = np.array(data_dict[field])
        shape = data.shape
        print "There are %d rows and %d columns in this array."%(shape[1],shape[2])
        index = raw_input("Please input proper one:")
        index = int(index)
        if(axes == 'x'):
            vector = data[nrange[0]-nrange[1],index,:]
        if(axes == 'y'):
            vector = data[nrange[0]-nrange[1],:,index]
        return vector
#get axes cordinate
    def get_axes(self,data_dict,axes='x'):
        '''
        This function is used to get axes.
        parameters:
        data_dict---data dictionary.
        axes--------axes, default:'x'
        '''
        import numpy as np
       #from constants import Constants as const
        cordinate = np.array(data_dict[axes.upper()])
        return cordinate
#use this function to get picture's extent.
    def get_extent(self,data_dict):
        '''
        This function will return picture's extent.
        parameters:
        data_dict---data dictionary get from hdf file.
        '''
        import numpy as np
        keys = data_dict.keys()
        extent = []
        #get constant
        dx = hdf_class.get_constant(self,field='axis')
        for eachone in "XYZ":
            if(eachone in keys):
                axis = data_dict[eachone]
                axis_min = np.min(axis)/dx
                axis_max = np.max(axis)/dx
                extent = extent + [axis_min,axis_max]
        return extent
#use this function to get the array to be plot.
    def get_array(self,data_dict,field='BX',nrange=[1,1,2]):
        '''
        This function is used to get the needed array fron data dictionary,
        parameters:
        data_dict---data dictionary
        field-------input physical field, default:'BX'
        number------file number, represent time.
        '''
        import numpy as np
        data = data_dict[field]
        dimen = data.shape
        if(len(dimen) == 2):
            array = np.array(data)
        if(len(dimen) == 3):
            #number = hdf_class.get_time(self,data_dict,field=field)
            array = data[nrange[0]-nrange[1],:,:]
        return array
#use this function to get magnetic flux along x or y axes.
    def get_flux(self,data_dict,axes="x"):
        '''
        This function is used to calculate magnetic flux.
        data_dict---data dictionary get from hdf file.
        axes--------axes,'x' or 'y', default:'x'
        '''
        import numpy as np
        import string
        from constants import Constants as const
        #find field
        s = 'xy'
        index = s.find(axes)
        field = ('b'+s[1-index]).upper()
        data = np.array(data_dict[field])
        dimen = data.shape
        n = dimen[0]
        a = dimen[1]
        b = dimen[2]
        #get dx
        x = np.array(data_dict["X"])
        dx = x[1]-x[0]
        if(axes == 'x'):
            array = (data[:,a/2-1,(b/2):]+data[:,a/2,(b/2):])/2.0
        else:
            array = (data[:,(a/2):,b/2-1]+data[:,(a/2):,b/2])/2.0
        flux = np.sum(array,axis=1)
        return -flux*dx/(const.B0)/(const.D0)
