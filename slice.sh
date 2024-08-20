#!/bin/bash

echo ====================
echo 正在切割
rm -rf ./input/.ipynb_checkpoints
# python audio-slicer.py --output output --input input 10
python audio-slicer/audio-slicer.py --output audio-slicer/output --input audio-slicer/input 10

echo 切割完成...请查看output文件夹...