# coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask import url_for
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import cv2
import math
import tensorflow as tf
import numpy as np
import pandas as pd
from preprocessing import inception_preprocessing
from nets import inception


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


## 常量
BASE_PATH = '/media/ice-melt/Disk-D1/Github/CalligraphyDistinguish'
TRAIN_DIR = 'static/train' # TRAIN DIR

CKPT_FILE = '/model.ckpt-10000'
LABELS_TXT = os.path.join(BASE_PATH + '/DATASET/labels.txt')
checkpoint_path = os.path.join(BASE_PATH + '/DATASET/train_ckpt'+ CKPT_FILE)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 获取字典图
def getMaps(labels_txt):
    return {line.rstrip().split(":")[0]: line.rstrip().split(":")[1] for line in open(labels_txt, encoding="utf8")}


# 获取结果labels
def getResult(photo_filenames):
    labels = []
    maps = getMaps(LABELS_TXT)
    with tf.Graph().as_default():
        tf.logging.set_verbosity(tf.logging.INFO)
        input_x = tf.placeholder(dtype=tf.string)

        image_raw = tf.image.decode_jpeg(input_x, channels=3)
        processed_image = inception_preprocessing.preprocess_image(image_raw, 320, 320,
                                                                   is_training=False)
        processed_images = tf.expand_dims(processed_image, 0)

        with slim.arg_scope(inception.inception_v4_arg_scope()):
            logits, _ = inception.inception_v4(processed_images, num_classes=100, is_training=False)

        probabilities = tf.nn.softmax(logits)

        init_fn = slim.assign_from_checkpoint_fn(checkpoint_path, slim.get_model_variables('InceptionV4'))

        with tf.Session() as sess:
            init_fn(sess)
            with open(photo_filenames, 'rb') as g:
                content = g.read()
            probabilities_val = sess.run([probabilities], feed_dict={input_x: content})
            p_val = np.squeeze(probabilities_val)
            #top_k = p_val.argsort()[-5:][::-1]
            #print(top_k)
            sorted_inds = [i[0] for i in sorted(enumerate(p_val), key=lambda x: x[1], reverse=True)][:5]

            label = ''
            for indx in sorted_inds:
                label += maps[str(indx)]

            labels.append(label)
    return labels,labels[0]

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
# 将 DATASET 目录添加到URL方便静态文件访问
app.add_url_rule('/DATASET/<path:filename>',endpoint='DATASET',build_only=True)
# 引入slim
slim = tf.contrib.slim

# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        user_input,maybe_code = getResult(upload_path)
        print("===" ,user_input,maybe_code[0])
        maybe_path = os.path.join(basepath, TRAIN_DIR,maybe_code[0])

        print("=maybe_path==", maybe_path)
        maybe_files = os.listdir(maybe_path)
        maybe_file1 = "/"+TRAIN_DIR+"/"+maybe_code[0]+ "/"+maybe_files[0]
        maybe_file2 = "/"+TRAIN_DIR+"/"+maybe_code[0]+ "/"+maybe_files[1]
        maybe_file3 = "/"+TRAIN_DIR+"/"+maybe_code[0]+ "/"+maybe_files[2]
        print(maybe_file1,maybe_file2,maybe_file3)
        return render_template('upload_ok.html', userinput=user_input,f1=maybe_file1,f2=maybe_file2,f3=maybe_file3)

    return render_template('upload.html')



if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)