from cgitb import reset
from ObjectDetector import Detector
import io
import os
import cv2
import numpy
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from flask import send_file

basedir = os.path.dirname(os.path.abspath(__file__))
inputdir = os.path.join(basedir, 'static/input')
outptudir = os.path.join(basedir, 'static/output')
exts = ['.jpeg','.jpg','.png']

app = Flask(__name__)
detector = Detector()

@app.route("/", methods=['GET', 'POST'])
def index():

    result = []
    infilename = ''
    oufilename = ''
    filelist = os.listdir(inputdir)
    #获取制定文件
    for item in filelist:
        file_ext = os.path.splitext(item)[1]  #获取文件后缀名
        if file_ext.lower() in exts:
            result.append(item)

    if request.method == 'POST':
        # file = Image.open(request.files['file'].stream)
        infilename = request.form.get('filename')
        inputfile = os.path.join(inputdir, infilename)
        file = Image.open(inputfile)
        img = detector.detectObject(file)
        
        oufilename = 'output_{}.png'.format(datetime.now().strftime('%Y%m%d-%H%M%S')) #根据日期创建文件名
        filepath = os.path.join(outptudir,oufilename)
        ostream = io.BytesIO(img)
        oimg = Image.open(ostream)
        oimg.save(filepath) #保存返回图片 
        return render_template('index.html', result = result, infilename = infilename, oufilename = oufilename)

    else:
        return render_template('index.html', result = result, oufilename = oufilename)


# @app.route("/", methods=['POST'])
# def upload():
#     if request.method == 'POST':
#         file = Image.open(request.files['file'].stream)
#         img = detector.detectObject(file)
        
#         # return send_file(
#         # io.BytesIO(img),
#         # mimetype='image/png',
#         # as_attachment=True
#         # )
#         return send_file(io.BytesIO(img),attachment_filename='image.jpg',mimetype='image/jpg')


if __name__ == "__main__":
    app.run()
