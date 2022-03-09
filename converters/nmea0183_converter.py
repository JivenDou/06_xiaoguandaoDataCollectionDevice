"""
@Date  :2021/5/21/00219:10:57
@Desc  :
"""
from sanic.log import logger
import binascii

from converter import Converter


class NEMA0183Converter(Converter):

    def convert(self, config, data):
        data = data.decode()
        if self.checksum(data):
            res = self.check_type(config, data)
            return res
        return "error"

    def make_checksum(self, data):
        '''
        Calculates a checksum from a NMEA sentence.
        
        Keyword arguments:
        data -- the NMEA sentence to create
        
        '''
        csum = 0
        i = 0
        # Remove ! or $ and *xx in the sentence
        data = data[1:data.rfind('*')]
        while (i < len(data)):
            input = binascii.b2a_hex(data[i].encode("utf8"))
            input = int(input, 16)
            # xor
            csum = csum ^ input
            i += 1
        return csum

    def checksum(self, data):
        '''
        Reads the checksum of an NMEA sentence.
        
        Keyword arguments:
        data -- the NMEA sentence to check
        
        '''
        try:
            # Create an integer of the two characters after the *, to the right
            supplied_csum = int(data[data.rfind('*') + 1:data.rfind('*') + 3], 16)
        except:
            return ''
        # Create the checksum
        csum = self.make_checksum(data)
        # Compare and return
        if csum == supplied_csum:
            return True
        else:
            return False

    def check_type(self, config, data):
        dict = {}
        data = data.split('*')
        # Splits up the NMEA data by comma
        data = data[0].split(',')
        logger.debug('len:', len(data), 'data:', data)
        if data[0] == '$PMIRWM':
            for index in config:
                name = 'c' + str(index['serial_number'])
                i = int(index['address'])
                dict[name] = data[i]
            logger.debug(dict)
            return dict

        # return data[0]

    def nmea2utc(self, data):
        '''
        Converts NMEA utc format to more standardized format.
        '''
        time = data[1][0:2] + ':' + data[1][2:4] + ':' + data[1][4:6]
        date = '20' + data[9][4:6] + '-' + data[9][2:4] + '-' + data[9][0:2]
        return date + 'T' + time + 'Z'


'''        
data = "$PMIRR,20210325,033351.719,0.000,0.000,V,0.00*0F" 

data2 = data.split('*')
data2 = data2[0].split(',')

logger.debug(data2[0][3:6])

c = NEMA0183Converter(None)
d = c.checksum(data)  
logger.debug(d)

logger.debug(c.nmea2utc(data2[1]))
'''
