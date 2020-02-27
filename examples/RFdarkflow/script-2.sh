#!/bin/bash
python run_darkflow.py --config  yolo_train_real.yaml --mode train --gpu 1 --load -1
python run_darkflow.py --config  yolo_train_real-200.yaml --mode train --gpu 1 --load -1

        
