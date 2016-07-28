#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, 2014 CERN
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

import logging
import os
import sys
import importlib

from hdlmake.srcfile import SourceFileFactory

from .action import Action


class GenerateRemoteSynthesisMakefile(Action):

    def _check_manifest(self):
        if not self.top_module.action == "synthesis":
            logging.error("action must be equal to \"synthesis\"")
            sys.exit("Exiting")

        if not self.top_module.syn_project:
            logging.error("syn_project must be set in the manifest.")
            sys.exit("Exiting")


    def run(self):
        self._check_all_fetched_or_quit()
        self._check_manifest()
        tool_name = self.modules_pool.get_top_module().syn_tool
        try:
            tool_module = importlib.import_module("hdlmake.tools.%s.%s" % (tool_name, tool_name))
        except Exception as e:
            logging.error(e)
            quit()
        tool_object = tool_module.ToolControls()
        self._generate_remote_synthesis_makefile(tool_object)


    def _generate_remote_synthesis_makefile(self, tool_object):

        logging.info("Generating makefile for remote synthesis.")

        top_mod = self.modules_pool.get_top_module()

        self.env.check_remote_tool(tool_object)
        self.env.check_general()

        files = self.modules_pool.build_file_set()

        sff = SourceFileFactory()
        files.add(sff.new(top_mod.syn_project, module=self.top_module))

        tool_object.generate_remote_synthesis_makefile(files=files, name=top_mod.syn_project[:-5],
                                                            cwd=top_mod.url, user=self.env["rsynth_user"],
                                                            server=self.env["rsynth_server"])
        logging.info("Remote synthesis makefile generated.")



