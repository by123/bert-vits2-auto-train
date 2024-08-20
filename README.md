# Bert_Vits2 自动训练脚本说明


### 准备工作
* bertvits_train.py rename.py 放在 workdir 目录
* slice.sh 放在 audio_slice 目录
* 待训练音频放在 audio_slice/input/
* 替换 labeling_whisper_CJE.py 文件，在 auto_VITS-DataLabeling 下


### 开始训练
* python bertvits_train.py -n '说话人名称'
