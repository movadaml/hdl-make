#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 - 2015 CERN
# Author: Pawel Szostek (pawel.szostek@cern.ch)
# Multi-tool support by Javier D. Garcia-Lasheras (javier@garcialasheras.com)
#
# This file is part of Hdlmake.
#
# Hdlmake is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hdlmake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hdlmake.  If not, see <http://www.gnu.org/licenses/>.
#

"""Module providing support for Mentor Modelsim simulation"""

from __future__ import print_function
from __future__ import absolute_import
import os

import logging
from .makefilevsim import MakefileVsim


class ToolModelsim(MakefileVsim):

    """Class providing the interface for Mentor Modelsim simulator"""

    TOOL_INFO = {'name': 'Modelsim',
                 'id': 'modelsim',
                 'windows_bin': 'vsim.exe',
                 'linux_bin': 'vsim'}

    STANDARD_LIBS = ['ieee', 'std', 'altera_mf']

    CLEAN_TARGETS = {'clean': ["modelsim.ini", "transcript"],
                     'mrproper': ["*.vcd", "*.wlf"]}

    def __init__(self):
        super(ToolModelsim, self).__init__()
        self.copy_rules["modelsim.ini"] = os.path.join(
            "$(MODELSIM_INI_PATH)", "modelsim.ini")
        self.additional_deps.append("modelsim.ini")

    def _makefile_sim_options(self):
        """Print the Modelsim options to the Makefile"""
        modelsim_ini_path = self.manifest_dict.get("modelsim_ini_path")
        if modelsim_ini_path == None:
            # 1: standard modelsim override
            if "MODELSIM" in os.environ:
                modelsim_ini_path = os.path.dirname(os.environ["MODELSIM"])
                logging.info("%s found %s: %s", "modelsim.ini", "from MODELSIM envvar", modelsim_ini_path)
            # 2: use modelsim from install found by hdlmake (first vsim in path)
            elif self.manifest_dict['sim_path']:
                modelsim_ini_path = os.path.join(
                    self.manifest_dict["sim_path"], "..")
                logging.info("%s found %s: %s", "modelsim.ini", "from binary location", modelsim_ini_path)
            # 3: use cocotb override, when sim bin is set manually and sim_path is none
            else:
                modelsim_ini_path = os.path.join(
                    "$(HDLMAKE_MODELSIM_PATH)", "..")
                logging.info("%s found %s: %s", "modelsim.ini", "from HDLMAKE_MODELSIM_PATH", modelsim_ini_path)
        else:
            logging.info("%s found %s: %s", "modelsim.ini", "from manifest", modelsim_ini_path)
        self.custom_variables["MODELSIM_INI_PATH"] = modelsim_ini_path
        modelsim_ini = "-modelsimini modelsim.ini "
        vcom_opt = self.manifest_dict.get("vcom_opt", '')
        self.manifest_dict["vcom_opt"] = modelsim_ini + vcom_opt
        vlog_opt = self.manifest_dict.get("vlog_opt", '')
        self.manifest_dict["vlog_opt"] = modelsim_ini + vlog_opt
        vmap_opt = self.manifest_dict.get("vmap_opt", '')
        self.manifest_dict["vmap_opt"] = modelsim_ini + vmap_opt
        super(ToolModelsim, self)._makefile_sim_options()
