#对音频进行重命名
#在运行这步之前，请确保你已经在准备部分进行过一次说话人的修改
#重命名后的音频位于workdir/auto-vits-DataLabeling/raw_audio文件夹中
import os.path
import argparse

def run(speaker):
  root = "/root/autodl-tmp/workdir/auto-VITS-DataLabeling/raw_audio"
  #过滤隐藏文件夹
  files = os.listdir(root)
  i = 0
  for file in files:
     if not file.startswith('.'):
        yield file
     else:
         portion = os.path.splitext(file)
         i += 1
         new_name = speaker + "_" + str(i).zfill(4) + portion[1]
         print(root + "/" + file)
         print(root + "/" + new_name)
         os.rename(root + "/" + file, "root" + "/" + new_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rename')
    parser.add_argument('--name', '-n', type = str, default = '' , help = '说话人名称')
    args = parser.parse_args()
    run(args.name)

