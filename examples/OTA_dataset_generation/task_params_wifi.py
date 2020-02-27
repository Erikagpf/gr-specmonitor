#!/usr/bin/env python

import numpy as np
import sys

num_sections = 1
section_size = 1100000 #500000#100000
toffset_range = [50]#[int(i) for i in np.linspace(50,10000,10)]#[50,60,70,80,90,100]
frequency_offset =[0]# [('uniform',(-0.325,-0.125,0,0.125,0.325))]#[('uniform',(-0.325,-0.125,0.125,0.325))] #[-0.5,0.5]
skip_samps = 0
wf_gen_samps = section_size*num_sections + toffset_range[-1] + skip_samps + 50

tags = ['wifi']
ssh_hosts = ['USRPRx']

Tx_params = [
    ('frequency_offset',frequency_offset),
    ('time_offset',toffset_range),
    ('section_size',section_size),
    ('num_sections',num_sections),
    ('soft_gain',[1.0]),
    ('noise_voltage',[0])
]
Tx_params_wifi = list(Tx_params)
for i,e in enumerate(Tx_params_wifi):
    if e[0]=='frequency_offset':
        Tx_params_wifi[i] = ('frequency_offset',0)

RF_params = [
    ('tx_gain_norm', [0.9]),#[0.4,0.5,0.6,0.7,0.8,0.9,0.99,0.2,0.3]),#10.0**np.arange(-20,0,5)),#range(0, 21, 10)),  #range(0,30,15)),[0.2])
    ('settle_time', 0.25),
    ('rx_gaindB', [20.0]),#range(0, 21, 10)),
    ('rf_frequency', 2.3e9)
]

Rx_params = [
    ('n_fft_averages',100),
    ('img_row_offset',[0]),
    ('img_n_rows',104),
]

RFVOCFormat_params = [
    ('img_size',[(104,104)])
]

spectrogram_representation = {
    'format_type':'spectrogram',
    'boxlabel':'waveform',
    'fftsize':104,
    'cancel_DC_offset':True,
    'dB':True
}

stage_params = {
    'wifi':
    {
        'waveform':
        [
            ('waveform',['wifi']),
            ('number_samples',wf_gen_samps),
            ('sample_rate',[10e6,15e6,20e6,25e6,30e6,35e6,50e6]),
            ('encoding',[0]),
            ('pdu_length',[1500]),
            ('pad_interval',[('uniform',(150000,200000))]),
            ('signal_representation',[spectrogram_representation]),
            ('repeats',np.arange(10))
        ],
        'Tx': Tx_params_wifi,
        'RF': RF_params,
        'Rx': Rx_params,
        'RFVOCFormat': RFVOCFormat_params
    },

   
   
}
