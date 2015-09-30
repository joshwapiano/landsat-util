from os.path import join

import rasterio
import numpy

from decorators import rasterio_decorator
from image import BaseProcess


class NDVI(BaseProcess):

    def __init__(self, path, bands=None, **kwargs):
        bands = [4, 5]
        self.cmap = {0: (255, 255, 255, 0),
                     1: (250, 250, 250, 255),
                     2: (246, 246, 246, 255),
                     3: (242, 242, 242, 255),
                     4: (238, 238, 238, 255),
                     5: (233, 233, 233, 255),
                     6: (229, 229, 229, 255),
                     7:  (225, 225, 225, 255),
                     8:  (221, 221, 221, 255),
                     9:  (216, 216, 216, 255),
                     10: (212, 212, 212, 255),
                     11: (208, 208, 208, 255),
                     12: (204, 204, 204, 255),
                     13: (200, 200, 200, 255),
                     14: (195, 195, 195, 255),
                     15: (191, 191, 191, 255),
                     16: (187, 187, 187, 255),
                     17: (183, 183, 183, 255),
                     18: (178, 178, 178, 255),
                     19: (174, 174, 174, 255),
                     20: (170, 170, 170, 255),
                     21: (166, 166, 166, 255),
                     22: (161, 161, 161, 255),
                     23: (157, 157, 157, 255),
                     24: (153, 153, 153, 255),
                     25: (149, 149, 149, 255),
                     26: (145, 145, 145, 255),
                     27: (140, 140, 140, 255),
                     28: (136, 136, 136, 255),
                     29: (132, 132, 132, 255),
                     30: (128, 128, 128, 255),
                     31: (123, 123, 123, 255),
                     32: (119, 119, 119, 255),
                     33: (115, 115, 115, 255),
                     34: (111, 111, 111, 255),
                     35: (106, 106, 106, 255),
                     36: (102, 102, 102, 255),
                     37: (98, 98, 98, 255),
                     38: (94, 94, 94, 255),
                     39: (90, 90, 90, 255),
                     40: (85, 85, 85, 255),
                     41: (81, 81, 81, 255),
                     42: (77, 77, 77, 255),
                     43: (73, 73, 73, 255),
                     44: (68, 68, 68, 255),
                     45: (64, 64, 64, 255),
                     46: (60, 60, 60, 255),
                     47: (56, 56, 56, 255),
                     48: (52, 52, 52, 255),
                     49: (56, 56, 56, 255),
                     50: (60, 60, 60, 255),
                     51: (64, 64, 64, 255),
                     52: (68, 68, 68, 255),
                     53: (73, 73, 73, 255),
                     54: (77, 77, 77, 255),
                     55: (81, 81, 81, 255),
                     56: (85, 85, 85, 255),
                     57: (90, 90, 90, 255),
                     58: (94, 94, 94, 255),
                     59: (98, 98, 98, 255),
                     60: (102, 102, 102, 255),
                     61: (106, 106, 106, 255),
                     62: (111, 111, 111, 255),
                     63: (115, 115, 115, 255),
                     64: (119, 119, 119, 255),
                     65: (123, 123, 123, 255),
                     66: (128, 128, 128, 255),
                     67: (132, 132, 132, 255),
                     68: (136, 136, 136, 255),
                     69: (140, 140, 140, 255),
                     70: (145, 145, 145, 255),
                     71: (149, 149, 149, 255),
                     72: (153, 153, 153, 255),
                     73: (157, 157, 157, 255),
                     74: (161, 161, 161, 255),
                     75: (166, 166, 166, 255),
                     76: (170, 170, 170, 255),
                     77: (174, 174, 174, 255),
                     78: (178, 178, 178, 255),
                     79: (183, 183, 183, 255),
                     80: (187, 187, 187, 255),
                     81: (191, 191, 191, 255),
                     82: (195, 195, 195, 255),
                     83: (200, 200, 200, 255),
                     84: (204, 204, 204, 255),
                     85: (208, 208, 208, 255),
                     86: (212, 212, 212, 255),
                     87: (216, 216, 216, 255),
                     88: (221, 221, 221, 255),
                     89: (225, 225, 225, 255),
                     90: (229, 229, 229, 255),
                     91: (233, 233, 233, 255),
                     92: (238, 238, 238, 255),
                     93: (242, 242, 242, 255),
                     94: (246, 246, 246, 255),
                     95: (250, 250, 250, 255),
                     96: (255, 255, 255, 255),
                     97: (250, 250, 250, 255),
                     98: (245, 245, 245, 255),
                     99: (240, 240, 240, 255),
                     100: (235, 235, 235, 255),
                     101: (230, 230, 230, 255),
                     102: (225, 225, 225, 255),
                     103: (220, 220, 220, 255),
                     104: (215, 215, 215, 255),
                     105: (210, 210, 210, 255),
                     106: (205, 205, 205, 255),
                     107: (200, 200, 200, 255),
                     108: (195, 195, 195, 255),
                     109: (190, 190, 190, 255),
                     110: (185, 185, 185, 255),
                     111: (180, 180, 180, 255),
                     112: (175, 175, 175, 255),
                     113: (170, 170, 170, 255),
                     114: (165, 165, 165, 255),
                     115: (160, 160, 160, 255),
                     116: (155, 155, 155, 255),
                     117: (151, 151, 151, 255),
                     118: (146, 146, 146, 255),
                     119: (141, 141, 141, 255),
                     120: (136, 136, 136, 255),
                     121: (131, 131, 131, 255),
                     122: (126, 126, 126, 255),
                     123: (121, 121, 121, 255),
                     124: (116, 116, 116, 255),
                     125: (111, 111, 111, 255),
                     126: (106, 106, 106, 255),
                     127: (101, 101, 101, 255),
                     128: (96, 96, 96, 255),
                     129: (91, 91, 91, 255),
                     130: (86, 86, 86, 255),
                     131: (81, 81, 81, 255),
                     132: (76, 76, 76, 255),
                     133: (71, 71, 71, 255),
                     134: (66, 66, 66, 255),
                     135: (61, 61, 61, 255),
                     136: (56, 56, 56, 255),
                     137: (66, 66, 80, 255),
                     138: (77, 77, 105, 255),
                     139: (87, 87, 130, 255),
                     140: (98, 98, 155, 255),
                     141: (108, 108, 180, 255),
                     142: (119, 119, 205, 255),
                     143: (129, 129, 230, 255),
                     144: (140, 140, 255, 255),
                     145: (131, 147, 239, 255),
                     146: (122, 154, 223, 255),
                     147: (113, 161, 207, 255),
                     148: (105, 168, 191, 255),
                     149: (96, 175, 175, 255),
                     150: (87, 183, 159, 255),
                     151: (78, 190, 143, 255),
                     152: (70, 197, 127, 255),
                     153: (61, 204, 111, 255),
                     154: (52, 211, 95, 255),
                     155: (43, 219, 79, 255),
                     156: (35, 226, 63, 255),
                     157: (26, 233, 47, 255),
                     158: (17, 240, 31, 255),
                     159: (8, 247, 15, 255),
                     160: (0, 255, 0, 255),
                     161: (7, 255, 0, 255),
                     162: (15, 255, 0, 255),
                     163: (23, 255, 0, 255),
                     164: (31, 255, 0, 255),
                     165: (39, 255, 0, 255),
                     166: (47, 255, 0, 255),
                     167: (55, 255, 0, 255),
                     168: (63, 255, 0, 255),
                     169: (71, 255, 0, 255),
                     170: (79, 255, 0, 255),
                     171: (87, 255, 0, 255),
                     172: (95, 255, 0, 255),
                     173: (103, 255, 0, 255),
                     174: (111, 255, 0, 255),
                     175: (119, 255, 0, 255),
                     176: (127, 255, 0, 255),
                     177: (135, 255, 0, 255),
                     178: (143, 255, 0, 255),
                     179: (151, 255, 0, 255),
                     180: (159, 255, 0, 255),
                     181: (167, 255, 0, 255),
                     182: (175, 255, 0, 255),
                     183: (183, 255, 0, 255),
                     184: (191, 255, 0, 255),
                     185: (199, 255, 0, 255),
                     186: (207, 255, 0, 255),
                     187: (215, 255, 0, 255),
                     188: (223, 255, 0, 255),
                     189: (231, 255, 0, 255),
                     190: (239, 255, 0, 255),
                     191: (247, 255, 0, 255),
                     192: (255, 255, 0, 255),
                     193: (255, 249, 0, 255),
                     194: (255, 244, 0, 255),
                     195: (255, 239, 0, 255),
                     196: (255, 233, 0, 255),
                     197: (255, 228, 0, 255),
                     198: (255, 223, 0, 255),
                     199: (255, 217, 0, 255),
                     200: (255, 212, 0, 255),
                     201: (255, 207, 0, 255),
                     202: (255, 201, 0, 255),
                     203: (255, 196, 0, 255),
                     204: (255, 191, 0, 255),
                     205: (255, 185, 0, 255),
                     206: (255, 180, 0, 255),
                     207: (255, 175, 0, 255),
                     208: (255, 170, 0, 255),
                     209: (255, 164, 0, 255),
                     210: (255, 159, 0, 255),
                     211: (255, 154, 0, 255),
                     212: (255, 148, 0, 255),
                     213: (255, 143, 0, 255),
                     214: (255, 138, 0, 255),
                     215: (255, 132, 0, 255),
                     216: (255, 127, 0, 255),
                     217: (255, 122, 0, 255),
                     218: (255, 116, 0, 255),
                     219: (255, 111, 0, 255),
                     220: (255, 106, 0, 255),
                     221: (255, 100, 0, 255),
                     222: (255, 95, 0, 255),
                     223: (255, 90, 0, 255),
                     224: (255, 85, 0, 255),
                     225: (255, 79, 0, 255),
                     226: (255, 74, 0, 255),
                     227: (255, 69, 0, 255),
                     228: (255, 63, 0, 255),
                     229: (255, 58, 0, 255),
                     230: (255, 53, 0, 255),
                     231: (255, 47, 0, 255),
                     232: (255, 42, 0, 255),
                     233: (255, 37, 0, 255),
                     234: (255, 31, 0, 255),
                     235: (255, 26, 0, 255),
                     236: (255, 21, 0, 255),
                     237: (255, 15, 0, 255),
                     238: (255, 10, 0, 255),
                     239: (255, 5, 0, 255),
                     240: (255, 0, 0, 255),
                     241: (255, 0, 15, 255),
                     242: (255, 0, 31, 255),
                     243: (255, 0, 47, 255),
                     244: (255, 0, 63, 255),
                     245: (255, 0, 79, 255),
                     246: (255, 0, 95, 255),
                     247: (255, 0, 111, 255),
                     248: (255, 0, 127, 255),
                     249: (255, 0, 143, 255),
                     250: (255, 0, 159, 255),
                     251: (255, 0, 175, 255),
                     252: (255, 0, 191, 255),
                     253: (255, 0, 207, 255),
                     254: (255, 0, 223, 255),
                     255: (255, 0, 239, 255)}
        super(NDVI, self).__init__(path, bands, **kwargs)

    @rasterio_decorator
    def run(self):
        """
        Executes NDVI processing
        """
        self.output("* NDVI processing started.", normal=True)

        bands = self._read_bands()
        image_data = self._get_image_data()

        new_bands = []
        for i in range(0, 2):
            new_bands.append(numpy.empty(image_data['shape'], dtype=numpy.float32))

        self._warp(image_data, bands, new_bands)

        # Bands are no longer needed
        del bands

        calc_band = numpy.true_divide((new_bands[1] - new_bands[0]), (new_bands[1] + new_bands[0]))

        output_band = numpy.rint((calc_band + 1) * 255 / 2).astype(numpy.uint8)

        output_file = '%s_NDVI.TIF' % (self.scene)
        output_file = join(self.dst_path, output_file)

        return self.write_band(output_band, output_file, image_data)

    def write_band(self, output_band, output_file, image_data):

        # from http://publiclab.org/notes/cfastie/08-26-2014/new-ndvi-colormap
        with rasterio.open(output_file, 'w', driver='GTiff',
                           width=image_data['shape'][1],
                           height=image_data['shape'][0],
                           count=1,
                           dtype=numpy.uint8,
                           nodata=0,
                           transform=image_data['dst_transform'],
                           crs=self.dst_crs) as output:

            output.write_band(1, output_band)

            cmap = {k: v[:3] for k, v in self.cmap.iteritems()}
            output.write_colormap(1, cmap)
            self.output("Writing to file", normal=True, color='green', indent=1)
        return output_file


class NDVIWithManualColorMap(NDVI):

    def manual_colormap(self, n, i):
        return self.cmap[n][i]

    def write_band(self, output_band, output_file, image_data):
        # colormaps will overwrite our transparency masks so we will manually
        # create three RGB bands

        self.output("Creating Manual ColorMap", normal=True, arrow=True)
        self.cmap[0] = (0, 0, 0, 255)

        v_manual_colormap = numpy.vectorize(self.manual_colormap, otypes=[numpy.uint8])
        rgb_bands = []
        for i in range(3):
            rgb_bands.append(v_manual_colormap(output_band, i))

        with rasterio.drivers(GDAL_TIFF_INTERNAL_MASK=True):
            with rasterio.open(output_file, 'w', driver='GTiff',
                               width=image_data['shape'][1],
                               height=image_data['shape'][0],
                               count=3,
                               dtype=numpy.uint8,
                               nodata=0,
                               photometric='RGB',
                               transform=image_data['dst_transform'],
                               crs=self.dst_crs) as output:

                for i in range(3):
                    output.write_band(i+1, rgb_bands[i])
                # output.write_colormap(1, cmap)
                # output.write_mask(no_data_mask)

            self.output("Writing to file", normal=True, color='green', indent=1)
        return output_file
