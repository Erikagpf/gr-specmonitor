#!/usr/bin/env python

import numpy as np
import sys

num_sections = 1
section_size = 1100000 #500000#100000
toffset_range = [50]#[int(i) for i in np.linspace(50,10000,10)]#[50,60,70,80,90,100]
frequency_offset = [0]#[('uniform',(-0.325,-0.125,0,0.125,0.325))] #[-0.5,0.5]
skip_samps = 0
wf_gen_samps = section_size*num_sections + toffset_range[-1] + skip_samps + 50

tags = ['lte']
ssh_hosts = ['USRPRx']

Tx_params = [
    ('frequency_offset',frequency_offset),
    ('time_offset',toffset_range),
    ('section_size',section_size),
    ('num_sections',num_sections),
    ('soft_gain',[1.0]),
    ('noise_voltage',[0])
]

RF_params = [
    ('tx_gain_norm', [0.4,0.5,0.6,0.7,0.8,0.9,0.99,0.2,0.3]),#10.0**np.arange(-20,0,5)),#range(0, 21, 10)),  #range(0,30,15)),
    ('settle_time', 0.25),
    ('rx_gaindB', [20.0]),#range(0, 21, 10)),
    ('rf_frequency', 2.35e9)
]

Rx_params = [
    ('n_fft_averages',100),
    ('img_row_offset',[0]),
    ('img_n_rows',104),
]

RFVOCFormat_params = [
    ('img_size',[(104,104)])
]
# RFVOCFormat_params = {
#     'img_size': [(104,104)]
# }

spectrogram_representation = {
    'format_type':'spectrogram',
    'boxlabel':'waveform',
    'fftsize':104,
    'cancel_DC_offset':True,
    'dB':True
}

stage_params = {
   
    'lte':
    {
        'waveform':
        [
            ('waveform',['lte_dl']),
            ('sample_rate',20e6),
            ('n_samples',wf_gen_samps),
            ('n_prbs',[50,25]),
            ('pad_interval',[('uniform',(100000,200000))]),
            ('signal_representation',[spectrogram_representation]),
            ('n_offset_samples',[('uniform',(0,500000))]),
            ('runs',range(2))
        ],
        'Tx': Tx_params,
        'RF': RF_params,
        'Rx': Rx_params,
        'RFVOCFormat': RFVOCFormat_params
    }
}
