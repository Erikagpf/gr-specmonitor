#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Francisco Paisana.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import pickle

class WaveformPklReader:
    def __init__(self,fname):
        with open(fname,'r') as f:
            self.wavdata = pickle.load(f)

    def number_samples(self):
        return self.wavdata['IQsamples'].size

    def parameters(self):
        return self.wavdata['parameters']

    def data(self):
        return self.wavdata

    def read_section(self,startidx=0,endidx=None):
        if endidx is None:
            return self.wavdata['IQsamples'][startidx::]
        else:
            return self.wavdata['IQsamples'][startidx:endidx]

    def is_framed(self):
        if 'section_bounds' in self.wavdata:
            return True
        return False
