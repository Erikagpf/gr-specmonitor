#!/usr/bin/env python

import numpy as np
from specmonitor.labeling_framework import random_generator

num_sections = 1
section_size = 3000000
toffset_range = [50]
frequency_offset = 0
skip_samps = 0
wf_gen_samps = section_size*num_sections + toffset_range[-1] + skip_samps + 50
n_repeats = 10
sample_rate = 23.04e6
ch1_interval = (30000,50000) #1.5-2.5ms
ch2_interval = (1000000,1500000) # 50-100ms
N_fft_avg = 150

tags = ['wifi','lte']

spectrogram_representation = {
    'format_type':'spectrogram',
    'boxlabel':'waveform',
    'fftsize':256,
    'cancel_DC_offset':True,
    'dB':True
}
Tx_params = {
    'frequency_offset': frequency_offset,
    'time_offset': toffset_range,
    'section_size': section_size,
    'num_sections': num_sections,
    'soft_gain': 1.0,
    'noise_voltage':0
}

stage_params = {
    'wifi':
    {
        'waveform':
        {
            'waveform': 'wifi',
            'number_samples': wf_gen_samps,
            'sample_rate': sample_rate,
            'encoding': 0,
            'pdu_length': 1500,
            'pad_interval': [('uniform',ch1_interval)],
            'signal_representation': [spectrogram_representation],
            'frame_mag2': 0.99,
            'runs': range(n_repeats)
        },
        'Tx': Tx_params
    },
    'lte':
    {
        'waveform':
        {
            'waveform': 'lte_dl',
            'n_samples': wf_gen_samps,
            'sample_rate': sample_rate,
            'n_prbs': 100,
            'pad_interval': random_generator('randint',ch2_interval),
            'signal_representation':[spectrogram_representation],
            'n_offset_samples': [('uniform',(0,500000))],
            'runs': range(n_repeats)
        },
        'Tx': Tx_params
    }
}
