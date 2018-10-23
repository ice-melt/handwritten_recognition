# Calligraphy Distinguish

> 相关**说明**和**数据集**见[[TinyMind 汉字书法识别]](https://www.tinymind.cn/competitions/41#dataDescription)

## tfrecord
相关代码

- [download_and_convert_data.py](download_and_convert_data.py)
- [datasets/convert_quiz.py](datasets/convert_quiz.py)
- [datasets/dataset_utils.py](datasets/dataset_utils.py)

以上代码修改部分来源[https://gitee.com/ai100/quiz-w7-code](https://gitee.com/ai100/quiz-w7-code)

根目录下运行命令
```Bash
# DATASET_DIR 是数据所在目录，需要下载和指定
DATASET_DIR=~tmp/CalligraphyDistinguish/DATASET/train
python download_and_convert_data.py \
  --dataset_name=quiz \
  --dataset_dir=${DATASET_DIR}
```