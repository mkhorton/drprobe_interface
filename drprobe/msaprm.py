# -*- coding: utf-8 -*-
#from __future__ import print_function

"""
Created on Mon Apr  4 15:00:02 2016

@author: fwinkler
"""

import numpy as np
import re
import os


class MsaPrm(object):
    """
    Msa object that can be used to load, modify and save a msa parameter file for the Dr. Probe
    software package.

    Attributes
    ----------
    conv_semi_angle : float
        Semi angle of convergence [mrad]
    inner_radius_ann_det : float
        Inner radius of the annular detector [mrad]
    outer_radius_ann_det : float
        Outer radius of the annular detector [mrad]
    detector : (int, string)
        Detector definition file, switch and file name
    wavelength : float
        Electron wavelength [nm]
    source_radius : float
        De-magnified source radius (1/e half width) [nm]
    focus_spread : float
        Focus spread [nm]
    focus_spread_kernel_hw : float
        Focus-spread kernel half-width w.r.t. the focus spread
    focus_spread_kernel_size :float
        Focus-spread kernel size
    number_of_aber : int
        Number of aberration definitions following
    tilt_x : float
        Object tilt X [deg]. Approximative approach. Do not use for tilts larger than 5 degrees.
    tilt_y : float
        Object tilt Y [deg]. Approximative approach. Do not use for tilts larger than 5 degrees.
    h_scan_offset : float
        Horizontal scan frame offset [nm]. X coordinate of the lower left scan frame corner.
    v_scan_offset : float
        Vertical scan frame offset [nm]. X coordinate of the lower left scan frame corner.
    h_scan_frame_size : float
        Horizontal scan frame size [nm]
    v_scan_frame_size : float
        Vertical scan frame size [nm]
    scan_frame_rot : float
        Scan frame rotation [deg] w.r.t. the slice data.
    scan_columns : int
        Number of scan columns = number of pixels on horizontal scan image axis.
    scan_rows : int
        Number of scan rows = number of pixels on vertical scan image axis.
    temp_coherence_flag : int
        Switch for partial temporal coherence calculation. Drastic increase of calculation time
        if activated
    spat_coherence_flag : int
        Switch for partial spatial coherence calculation. Is only applied in combination with an
        input image file.
    super_cell_x : int
        Supercell repeat factor in horizontal direction, x
    super_cell_y : int
        Supercell repeat factor in vertical direction, y
    super_cell_z : int
        Supercell repeat factor in Z-direction, obsolete
    slice_files : string
        Slice file series name [SFN]. Expected file names are [SFN]+'_###.sli' where ### is a
        three digit number.
    number_of_slices : int
        Number of slice files to load
    number_frozen_lattice : int
        Number of frozen lattice variants per slice.
    min_num_frozen : int
        Minimum number of frozen lattice variations averaged per scan pixel in STEM mode.
    det_readout_period : int
        Detector readout period in slices.
    tot_number_of_slices : int
        Number of slices in the object.

    Parameters
    ----------
    msa_dict : dictionary
        A dictionary with all attributes written to the parameter file. Can be loaded from an
        existing parameter file.

    Methods
    -------
    load_msa_prm(prm_filename)
        Creates a MsaPrm object with all attributes taken from the parameterfile 'prm_filename'.
    save_wavimg_prm(prm_filename)
        Saves a MsaPrm object to a parameterfile. The path and name of the parameterfile is
        defined by prm_filename.
    """

    def __init__(self, msa_dict=None):
        if msa_dict is None:
            msa_dict = {}

        self.conv_semi_angle = msa_dict.get('conv_semi_angle', 30)
        self.inner_radius_ann_det = msa_dict.get('inner_radius_ann_det', 0)
        self.outer_radius_ann_det = msa_dict.get('outer_radius_ann_det', 30)
        self.detector = msa_dict.get('detector', (0, "prm/msa_det.prm"))
        self.wavelength = msa_dict.get('wavelength', 0.00417571)
        self.source_radius = msa_dict.get('source_radius', 0.01)
        self.focus_spread = msa_dict.get('focus_spread', 3)
        self.focus_spread_kernel_hw = msa_dict.get('focus_spread_kernel_hw', 2)
        self.focus_spread_kernel_size = msa_dict.get('focus_spread_kernel_size', 7)
        self.number_of_aber = msa_dict.get('number_of_aber', 0)
        self.tilt_x = msa_dict.get('tilt_x', 0)
        self.tilt_y = msa_dict.get('tilt_y', 0)
        self.h_scan_offset = msa_dict.get('h_scan_offset', 0)
        self.v_scan_offset = msa_dict.get('v_scan_offset', 0)
        self.h_scan_frame_size = msa_dict.get('h_scan_frame_size', 1)
        self.v_scan_frame_size = msa_dict.get('v_scan_frame_size', 1)
        self.scan_frame_rot = msa_dict.get('scan_frame_rot', 0)
        self.scan_columns = msa_dict.get('scan_columns', 0)
        self.scan_rows = msa_dict.get('scan_rows', 0)
        self.temp_coherence_flag = msa_dict.get('temp_coherence_flag', 0)
        self.spat_coherence_flag = msa_dict.get('spat_coherence_flag', 1)
        self.super_cell_x = msa_dict.get('super_cell_x', 1)
        self.super_cell_y = msa_dict.get('super_cell_y', 1)
        self.super_cell_z = msa_dict.get('super_cell_z', 1)
        self.slice_files = msa_dict.get('slice_files', "slc/slices")
        self.number_of_slices = msa_dict.get('number_of_slices', 5)
        self.number_frozen_lattice = msa_dict.get('number_frozen_lattice', 1)
        self.min_num_frozen = msa_dict.get('min_num_frozen', 1)
        self.det_readout_period = msa_dict.get('det_readout_period', 1)
        self.tot_number_of_slices = msa_dict.get('tot_number_of_slices', 10)

    def load_msa_prm(self, prm_filename, output=False):
        """
        Loads the parameterfile 'prm_filename'.

        Parameters
        ----------
        prm_filename : str
            The path and name of the parameterfile.
        output : bool, optional
            Flag for terminal output
        """
        with open(prm_filename, 'r') as prm:
            content = prm.readlines()
            content = [re.split(r'[,\s]\s*', line) for line in content]
            self.conv_semi_angle = float(content[1][0])
            self.inner_radius_ann_det = float(content[2][0])
            self.outer_radius_ann_det = float(content[3][0])
            self.detector = (int(content[4][0]), content[4][1])
            self.wavelength = float(content[5][0])
            self.source_radius = float(content[6][0])
            self.focus_spread = float(content[7][0])
            self.focus_spread_kernel_hw = float(content[8][0])
            self.focus_spread_kernel_size = float(content[9][0])
            self.number_of_aber = int(content[10][0])
            self.tilt_x = float(content[12][0])
            self.tilt_y = float(content[13][0])
            self.h_scan_offset = float(content[14][0])
            self.v_scan_offset = float(content[15][0])
            self.h_scan_frame_size = float(content[16][0])
            self.v_scan_frame_size = float(content[17][0])
            self.scan_frame_rot = float(content[18][0])
            self.scan_columns = int(content[19][0])
            self.scan_rows = int(content[20][0])
            self.temp_coherence_flag = int(content[21][0])
            self.spat_coherence_flag = int(content[22][0])
            self.super_cell_x = int(content[23][0])
            self.super_cell_y = int(content[24][0])
            self.super_cell_z = int(content[25][0])
            self.slice_files = content[26][0]
            self.number_of_slices = int(content[27][0])
            self.number_frozen_lattice = int(content[28][0])
            self.min_num_frozen = int(content[29][0])
            self.det_readout_period = int(content[30][0])
            self.tot_number_of_slices = int(content[31][0])

        if output:
            print("Parameters successfully loaded from file '{}'!".format(prm_filename))

    def save_msa_prm(self, prm_filename, output=False):
        """
        Saves the MsaPrm object in the parameterfile 'prm_filename'.

        Parameters
        ----------
        prm_filename : str
            The name of the parameterfile. Will be saved into the subfolder 'prm/'
        output : bool, optional
            Flag for terminal output.
        """

        directory = os.path.split(prm_filename)[0]
        if directory:
            if not os.path.isdir(directory):
                os.makedirs(directory)

        with open(prm_filename, 'w') as prm:
            prm.write("'[Microscope Parameters]'\n")
            string_0 = "Semi angle of convergence [mrad]"
            prm.write("{} ! {}\n".format(self.conv_semi_angle, string_0))
            string_1 = "Inner radius of the annular detector [mrad]"
            prm.write("{} ! {}\n".format(self.inner_radius_ann_det, string_1))
            string_2 = "Outer radius of the annular detector [mrad]"
            prm.write("{} ! {}\n".format(self.outer_radius_ann_det, string_2))
            string_3 = "Detector definition file, switch and file name"
            prm.write("{}, '{}'! {}\n".format(self.detector[0], self.detector[1], string_3))
            string_4 = "Electron wavelength [nm]"
            prm.write("{} ! {}\n".format(self.wavelength, string_4))
            string_5 = "De-magnified source radius (1/e half width) [nm]"
            prm.write("{} ! {}\n".format(self.source_radius, string_5))
            string_6 = "Focus spread [nm]"
            prm.write("{} ! {}\n".format(self.focus_spread, string_6))
            string_7 = "Focus-spread kernel half-width w.r.t. the focus spread"
            prm.write("{} ! {}\n".format(self.focus_spread_kernel_hw, string_7))
            string_8 = "Focus-spread kernel size"
            prm.write("{} ! {}\n".format(self.focus_spread_kernel_size, string_8))
            string_9 = "Number of aberration definitions following"
            prm.write("{} ! {}\n".format(self.number_of_aber, string_9))
            prm.write("'[Multislice Parameters]'\n")
            string_10 = "Object tilt X [deg]. Approximative approach. Do not use for tilts " \
                        "larger than 5 degrees."
            prm.write("{} ! {}\n".format(self.tilt_x, string_10))
            string_11 = "Object tilt Y [deg]. Approximative approach. Do not use for tilts " \
                        "larger than 5 degrees."
            prm.write("{} ! {}\n".format(self.tilt_y, string_11))
            string_12 = "Horizontal scan frame offset [nm]."
            prm.write("{} ! {}\n".format(self.h_scan_offset, string_12))
            string_13 = "Vertical scan frame offset [nm]."
            prm.write("{} ! {}\n".format(self.v_scan_offset, string_13))
            string_14 = "Horizontal scan frame size [nm]."
            prm.write("{} ! {}\n".format(self.h_scan_frame_size, string_14))
            string_15 = "Vertical scan frame size [nm]."
            prm.write("{} ! {}\n".format(self.v_scan_frame_size, string_15))
            string_16 = "Scan frame rotation [deg] w.r.t. the slice data."
            prm.write("{} ! {}\n".format(self.scan_frame_rot, string_16))
            string_17 = "Number of scan columns = number of pixels on horizontal scan image axis."
            prm.write("{} ! {}\n".format(self.scan_columns, string_17))
            string_18 = "Number of scan rows = number of pixels on vertical scan image axis."
            prm.write("{} ! {}\n".format(self.scan_rows, string_18))
            string_19 = "Switch for partial temporal coherence calculation. Drastic increase of " \
                        "calculation time if activated."
            prm.write("{} ! {}\n".format(self.temp_coherence_flag, string_19))
            string_20 = "Switch for partial spatial coherence calculation. Is only applied in " \
                        "combination with an input image file."
            prm.write("{} ! {}\n".format(self.spat_coherence_flag, string_20))
            string_21 = "Supercell repeat factor in horizontal direction, x."
            prm.write("{} ! {}\n".format(self.super_cell_x, string_21))
            string_22 = "Supercell repeat factor in vertical direction, y."
            prm.write("{} ! {}\n".format(self.super_cell_y, string_22))
            string_23 = "Supercell repeat factor in Z-direction, obsolete."
            prm.write("{} ! {}\n".format(self.super_cell_z, string_23))
            string_24 = "Slice file series name [SFN]. Expected file names are [SFN]+'_###.sli' " \
                        "where ### is a three digit number."
            prm.write("'{}' ! {}\n".format(self.slice_files, string_24))
            string_25 = "Number of slice files to load."
            prm.write("{} ! {}\n".format(self.number_of_slices, string_25))
            string_26 = "Number of frozen lattice variants per slice."
            prm.write("{} ! {}\n".format(self.number_frozen_lattice, string_26))
            string_27 = "Minimum number of frozen lattice variations averaged per scan pixel in " \
                        "STEM mode."
            prm.write("{} ! {}\n".format(self.min_num_frozen, string_27))
            string_28 = "Detector readout period in slices."
            prm.write("{} ! {}\n".format(self.det_readout_period, string_28))
            string_29 = "Number of slices in the object."
            prm.write("{} ! {}\n".format(self.tot_number_of_slices, string_29))

            for i in range(self.tot_number_of_slices):
                prm.write("{} ! Slice ID\n".format(i % self.number_of_slices))
            prm.write("End of parameter file.")

        # Sort prm file
        with open(prm_filename, 'r+') as prm:
            content = prm.readlines()

            length = []
            for line in content:
                length.append(len(line.split('!')[0]))

            spacer = np.max(length)
            prm.seek(0)
            prm.truncate()
            for line in content:
                if '!' in line:
                    line = line.split('!')[0].ljust(spacer) + ' !' + line.split('!')[1]
                prm.write(line)

        if output:
            print("Parameters successfully saved to file '{}'!".format(prm_filename))
