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
import sys
# import pickle
import cPickle as pickle
import numpy as np

from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import channels

from ..data_representation import image_representation as imgrep
from ..data_representation import timefreq_box as tfbox
from ..labeling_tools import preamble_utils
from ..sig_format import stage_signal_data as ssa
from ..utils import logging_utils
logger = logging_utils.DynamicLogger(__name__)

def generate_section_partitions(section_size,guard_band,num_sections):
    return ((i*section_size,(i+1)*section_size) for i in range(num_sections))

# this function returns the boxes intersected with the section of interest. It also
# offsets the boxes time stamp to be relative with the section start.
def compute_new_bounding_boxes(time_offset,section_size,freq_offset,box_list):
    boi = tfbox.intersect_boxes_with_section(box_list,(time_offset,time_offset+section_size))
    boi_offset = tfbox.add_offset(boi,-time_offset,freq_offset)
    return list(boi_offset)

# this function picks the boxes within the window (toffset:toffset+num_samples) that were offset by -toffset
# and breaks them into sections. It also offsets the box start to coincide with the section
def partition_boxes_into_sections(box_list,section_size,guard_band,num_sections):
    section_ranges = generate_section_partitions(section_size,guard_band,num_sections)
    return [list(tfbox.intersect_and_offset_box(box_list,s)) for s in section_ranges]

def apply_framing_and_offsets(args):
    params = args['parameters']

    ### get dependency file, and create a new stage_data object
    multi_stage_data = ssa.MultiStageSignalData.load_pkl(args)

    ### Read parameters
    time_offset = params['time_offset']
    section_size = params['section_size']
    num_sections = params['num_sections']
    noise_voltage = 0#params.get('noise_voltage',0)
    freq_offset = params.get('frequency_offset',0)
    soft_gain = params.get('soft_gain',1)
    num_samples = int(num_sections*section_size)
    hist_len = 3 # compensate for block history# channel is hier block with taps in it

    ### Create preamble and frame structure
    # TODO: Make this happen in another part of the code
    multi_stage_data.session_data['frame_params'] = {'section_size':section_size,
                                                     'num_sections':num_sections}
    fparams = preamble_utils.get_session_frame_params(multi_stage_data) #filedata.get_frame_params(stage_data)
    sframer = preamble_utils.SignalFramer(fparams)

    ### Read IQsamples
    twin = (time_offset-fparams.guard_len-hist_len,time_offset+num_samples+fparams.guard_len)
    assert twin[0]>=0
    xsections_with_hist = multi_stage_data.read_stage_samples()[twin[0]:twin[1]]

    ### Create GR flowgraph that picks read samples, applies freq_offset, scaling, and stores in a vector_sink
    tb = gr.top_block()
    source = blocks.vector_source_c(xsections_with_hist, True)
    soft_amp = blocks.multiply_const_cc(np.sqrt(soft_gain)+0*1j)
    channel = channels.channel_model(noise_voltage,freq_offset)
    assert len(channel.taps())+1==hist_len
    head = blocks.head(gr.sizeof_gr_complex,xsections_with_hist.size-hist_len)
    dst = blocks.vector_sink_c()

    tb.connect(source,soft_amp)
    tb.connect(soft_amp,channel)
    tb.connect(channel,head)
    tb.connect(head,dst)

    logger.info('Starting Tx parameter transformation script')
    tb.run()
    logger.info('GR script finished successfully')

    gen_data = np.array(dst.data())
    xsections = xsections_with_hist[hist_len::]
    # plt.plot(np.abs(gen_data))
    # plt.plot(np.abs(xsections),'r')
    # plt.show()
    assert gen_data.size==xsections.size

    ### Create preamble structure and frame the signal
    y,section_bounds = sframer.frame_signal(gen_data,num_sections)
    num_samples_with_framing = preamble_utils.get_num_samples_with_framing(fparams,num_sections)
    assert y.size==num_samples_with_framing

    prev_stage_metadata = multi_stage_data.get_stage_derived_params('spectrogram_img')
    prev_boxes = prev_stage_metadata.tfreq_boxes

    # intersect the boxes with the section boundaries
    try:
        box_list = compute_new_bounding_boxes(time_offset,num_samples,freq_offset,prev_boxes)
    except AssertionError:
        err_msg = 'These were the original stage params {}'.format(params)
        logger.error(err_msg)
        raise
    section_boxes = partition_boxes_into_sections(box_list,section_size,fparams.guard_len,num_sections)
    # print 'these are the boxes divided by section:',[[b.__str__() for b in s] for s in section_boxes]

    # fill new file
    # stage_data['IQsamples'] = y # overwrites the generated samples
    l = []
    sig2img_params = multi_stage_data.get_stage_args('signal_representation')
    signalimgmetadata = imgrep.get_signal_to_img_converter(sig2img_params)
    for i in range(len(section_bounds)):
        assert section_bounds[i][1]-section_bounds[i][0] == section_size
        assert all(s.label() is not None for s in section_boxes[i])
        l.append(signalimgmetadata(section_boxes[i],section_bounds[i],prev_stage_metadata.input_params))#specimgmetadata.input_params))

    assert y.size >= np.max([s[1] for s in section_bounds])
    for i in range(num_sections):
        # plt.plot(y[section_bounds[i][0]:section_bounds[i][1]])
        # plt.plot(gen_data[guard_band+i*section_size:guard_band+(i+1)*section_size],'r:')
        # plt.show()
        assert np.max(np.abs(y[section_bounds[i][0]:section_bounds[i][1]]-gen_data[(fparams.guard_len+i*section_size):fparams.guard_len+(i+1)*section_size]))<0.0001

    new_stage_data = ssa.StageSignalData(args,{'spectrogram_img':l},y)
    multi_stage_data.set_stage_data(new_stage_data)
    multi_stage_data.save_pkl()
