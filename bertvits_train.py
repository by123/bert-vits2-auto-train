import os
import argparse
import subprocess

workDir = '/root/autodl-tmp/workdir/'
bertDir = f'{workDir}Bert-VITS2/'
sliceDir = f'{workDir}audio-slicer/'
dataLabelDir = f'{workDir}auto-VITS-DataLabeling/'

def train(speaker):
    
    os.system(f'rm -r {bertDir}dataset/{speaker}/')
    os.system(f'rm -r {bertDir}Data/{speaker}/')
    os.system(f'rm -r {bertDir}dataset_raw/{speaker}/')
    print('..........初始化准备.........')
    prepare(speaker)
    print('..........样本集切割/标注.........')
    audio_slice(speaker)
    print('..........标注划分 bert与clap文件生成.........')
    bertclap(speaker)
    print('..........开始训练.........')
    start(speaker)


def prepare(speaker):
    print('#设置说话者名称')
    os.system('speaker=' + speaker)

    print('#在dataset_raw和Data内创建你的说话人文件夹')
    os.system(f'mkdir -p {bertDir}dataset_raw/{speaker}')
    os.system(f'mkdir -p {bertDir}Data/{speaker}/models')
    os.system(f'mkdir -p {bertDir}dataset/{speaker}')

    print('#移动底模到数据集文件夹')
    os.system(f'cp {bertDir}pre_train_models/*.pth {bertDir}Data/{speaker}/models')


def audio_slice(speaker):

    print('样本集切割')
    os.system(f'bash {sliceDir}slice.sh')

    print('移动数据集到标注目录')
    os.system(f'mv {sliceDir}output/* {dataLabelDir}raw_audio/')

    print('对音频进行重命名')
    os.system(f'python {workDir}rename.py -n ' + speaker)

    print('进行数据集的标注')
    os.system(f'python {dataLabelDir}labeling_whisper_CJE.py')
    # 仅中文
    # os.system('python auto_DataLabeling_ZH.py')

    print('移动音频到workdir/Bert_VITS2/raw_audio文件夹')
    os.system(f'rm -rf {dataLabelDir}long_character_anno.txt')
    os.system(f'mv {dataLabelDir}raw_audio/* {bertDir}dataset_raw/{speaker}/')

    print('移动标注文件到workdir/Bert_VITS2/filelist文件夹')
    os.system(f'mv {workDir}*.list {bertDir}filelists/')


def bertclap(speaker):
    os.chdir(bertDir)
    print('音频重采样')
    resample_shell = f'python resample.py --in_dir dataset_raw/{speaker} --out_dir dataset/{speaker} --sr 44100'
    os.system(resample_shell)

    print('划分标注数据训练集和验证集')
    preprocess_shell = 'python preprocess_text.py'
    os.system(preprocess_shell)

    print('生成 bert 文件')
    bert_shell = 'python bert_gen.py'
    os.system(bert_shell)
    
def start(speaker):
    os.chdir(bertDir)
    print('复制一份配置文件到模型文件夹')
    os.system(f'cp ./configs/config.json Data/{speaker}/models/')

    print('开始训练')
    os.system(f'torchrun train_ms.py -c ./configs/config.json  -m ./Data/{speaker}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train similar voice according bertvits')
    parser.add_argument('--name', '-n', type = str, default = '' , help = '说话人名称')
    args = parser.parse_args()
    if args.name == '':
        print('请使用 python bertvits_train.py -n 「说话者名称」')
    else:
        train(args.name)