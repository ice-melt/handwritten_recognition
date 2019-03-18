# 汉字书法识别

![汉字书法识别](https://file.ai100.com.cn/files/competition-logo/m494x356/33bec86a-338a-4efe-9640-e6b17cc8de73/%E6%9C%AA%E6%A0%87%E9%A2%98-1.jpg)

时间：2018/10/20-2018/10/21

地点：CSDN总部

[https://www.tinymind.cn/competitions/41](https://www.tinymind.cn/competitions/41)

## 数据集
竞赛数据提供100个汉字书法单字，包括碑帖，手写书法，古汉字等等。图片全部为单通道灰度jpg，宽高不定。

### 训练集：
训练集每个汉字400张图片，共计40000张图片，供参赛人员测试和开发参赛算法模型，训练集是标注好的数据，图片按照图片上的文字分类到不同的文件夹中，也就是说文件夹的名字就是文件夹里所有图片的标签。

### 测试集分两部分：
第一部分每汉字100张图片共10000张图片，在竞赛过程中，开放数据下载但不提供标签。比赛中第一阶段的排行榜对应参赛队伍第一部分数据的评测得分，这部分得分和排名不影响比赛的最终成绩，其目的是供参赛人员测试算法模型。

第二部分测试数据每汉字50张以上图片（单字图片数不固定）共16343张图片，比赛的最后阶段公开下载，不提供标签。

### 自由练习赛数据下载地址：
__训练集__: https://pan.baidu.com/s/1UxvN7nVpa0cuY1A-0B8gjg 密码: aujd

__测试集__: https://pan.baidu.com/s/1tzMYlrNY4XeMadipLCPzTw 密码: 4y9k

## 项目流程：

1. 生成tfrecord数据；


1. 加载预训练模型进行训练模型，保存ckpt文件；


1. 模型调参；


1. 校验集预测，生成csv文件。

## 代码说明

1. __tfrecord__ 相关代码

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

2. __数据预处理__ 相关代码

	- [preprocessing/preprocessing_factory.py](preprocessing/preprocessing_factory.py)
	- [preprocessing/inceptionv4_preprocessing.py](preprocessing/inceptionv4_preprocessing.py)

	inception网络的预处理比较全面，采用此网络的预处理过程对数据进行处理，但是需要注意几点：

	- 去除翻转处理,汉字的翻转等会影响文字的识别（翻转后的字有可能不是原字）
	- 去除裁切处理,图片的裁切很可能得到无意义的局部信息(因为图片汉字周围有留白,可进行适当的裁切)

	> 注意在预处理的工厂方法里增加修改后的预处理代码定义

3. __finetune inception v4__
	
	train_image_classifier.py


4. __展示__ 相关代码

	- [upload_pictures.py](upload_pictures.py)
	- [templates/upload.html](templates/upload.html)
	- [templates/upload_ok.html](templates/upload_ok.html)
	
	> 使用 `Flask` 做一个简单的展示页面,参考代码见[参考的博客找不到了,后面找到了在记录把]()

## 项目中出现的问题汇总：
1. 数据预处理时使用`inception_processing.py`，并将其文件中的数据裁切和随机翻转去掉，因为汉字经过此过程后可能变成其他字体；

1. 模型训练时`loss`值偏大，达到50左右，其原因为`weightdecay`（0.004）偏大，默认值为0.00004，修改后loss值正常；

1. 训练模型时，`validation`结果曾出现非常差，正确率仅为`0.01`，其原因可能为获取`checkpoint`文件失败；重新生成`tfrecord`文件运行后得到了正常的结果；

1. 生成提交的`CSV`文件时的3种思路：

	1. 使用test数据生成`tfrecord`文件，利用原有框架生成识别结果文件；

	1. 参考`eval_image_classifier.py`文件进行修改，读取test图片，预处理，进行预测，最终生成预测文件；

	1. 利用`ckpt`文件生成`pb`文件，进而生成预测文件；

5. 对`test`数据进行预测时，获取`checkpoint`时出现问题，因为指定的路径内没有`checkpoint`文件，无法获取最近的运行结果，修改后直接`restore`即可

6. 提交数据的格式出现问题，`label`按列表的格式进行了保存，与比赛的要求不符，修改后正常。

## 体会：
1. 项目中遇到问题时，先独立思考，再执行666法则，及时与同学及老师交流；

2. 队员之间相互分享遇到的问题及解决办法。

