# Calligraphy Distinguish

> 相关**说明**和**数据集**见[[TinyMind 汉字书法识别]](https://www.tinymind.cn/competitions/41#dataDescription)

## tfrecord
相关代码

- [download_and_convert_data.py](download_and_convert_data.py)
- [datasets/convert_quiz.py](datasets/convert_quiz.py)
- [datasets/dataset_utils.py](datasets/dataset_utils.py)

以上代码修改部分来源见 [https://gitee.com/ai100/quiz-w7-code](https://gitee.com/ai100/quiz-w7-code)

根目录下运行命令
```Bash
# DATASET_DIR 是数据所在目录，需要下载和指定
DATASET_DIR=~/tmp/CalligraphyDistinguish/DATASET/train
python download_and_convert_data.py \
  --dataset_name=quiz \
  --dataset_dir=${DATASET_DIR}
```
## 数据预处理
相关代码

- [preprocessing/preprocessing_factory.py](preprocessing/preprocessing_factory.py)
- [preprocessing/inceptionv4_preprocessing.py](preprocessing/inceptionv4_preprocessing.py)

inception网络的预处理比较全面，采用此网络的预处理过程对数据进行处理，但是需要注意几点：

- 去除翻转处理,汉字的翻转等会影响文字的识别（翻转后的字有可能不是原字）
- 去除裁切处理,图片的裁切很可能得到无意义的局部信息(因为图片汉字周围有留白,可进行适当的裁切)

> 注意在预处理的工厂方法里增加修改后的预处理代码定义

## finetune inception v4
train_image_classifier.py