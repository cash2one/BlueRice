from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from watson_developer_cloud import VisualRecognitionV3
import subprocess
from flask import Flask,request,send_file
import os

app = Flask('Show Text')
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='this_is_a_dev_key'
))

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='YOUR IBM APT KEY')

def textDetection(file_path):
    '''text detection'''
    with open(file_path, 'rb') as image_file:    
        text_results = visual_recognition.recognize_text(images_file=image_file)
        try:
            words = text_results['images'][0]['text']
            symbols = ['[',']']
            for sym in symbols:               
                words = words.replace(sym,'')
            words = words.replace('\n',' ')
        except:
            words = []
    return words

mywords = ''

@app.route('/post/<id>', methods=['POST'])
def get_cap(id):
    print('ID: ', id)
    type=1
    img = request.files['file']   
    img.save('/home/teno/Internship/BlueHack/input.jpg')
    print('saved!!!!')
    words = textDetection('/home/teno/Internship/BlueHack/input.jpg')
    print(words)
    global mywords
    mywords = words
    if type == 0:
        if words == 'turtle':
            num=35
        elif words == 'bird':
            num=13
        elif words == 'elephant':
            num=101
        elif words == 'crab':
            num=118
        elif words == 'dog':
            num=152
        elif words == 'lipstick':
            num=629
        elif words == 'tent':
            num=672
        elif words == 'guitar':
            num=546
        elif words == 'backpack':
            num=414
        elif words == 'beer':
            num=440
        elif words == 'broom':
            num=462
        elif words == 'jean':
            num=608
        elif words == 'iron':
            num=606
        elif words == 'lamp':
            num=619
        elif words == 'ship':
            num=625
        elif words == 'tent':
            num=672
        elif words == 'bridge':
            num=718
        else:
            print("Not supported.")

    if type==0:
        os.chdir("/home/teno/Internship/image_generation/PPGN")
        cap = num
        subprocess.call("chmod +x /home/teno/Internship/image_generation/PPGN/1_class_conditional_sampling.sh", shell=True)
        subprocess.call("/home/teno/Internship/image_generation/PPGN/1_class_conditional_sampling.sh {}".format(cap), shell=True)
        return send_file('/home/teno/Internship/image_generation/PPGN/output/output.jpg', mimetype='image/jpg')
    elif type==1:
        os.chdir("/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN")
        with open('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/birds/caption.txt', 'w') as f:
            f.write(words)
        subprocess.call("chmod +x /home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/demo/birds_demo.sh", shell=True)   
        subprocess.call("/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/demo/birds_demo.sh", shell=True)
        return send_file('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/birds/caption/sentence0.jpg', mimetype='image/jpg')
    elif type==2:
        os.chdir("/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN")
        print(os.getcwd())
        with open('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/flowers/caption.txt', 'w') as f:
            f.write(words)
        subprocess.call("chmod +x /home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/demo/flowers_demo.sh", shell=True) 
        subprocess.call("/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/demo/flowers_demo.sh", shell=True)   
        return send_file('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/flowers/caption/sentence0.jpg', mimetype='image/jpg')
    else:
        print("Input type not supported")
    return 'Success!'


@app.route('/getimg/', methods=['POST'])
def get_img():   
    print('get_img!!!!!!!!!!!!!!')
    type=1
    if type==0:
        os.chdir("/home/teno/Internship/image_generation/PPGN")
        global mywords
        return mywords
        return send_file('/home/teno/Internship/image_generation/PPGN/output/output.jpg', mimetype='image/jpg')
    elif type==1:
        os.chdir("/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN")
        global mywords
        return mywords
        return send_file('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/birds/caption/sentence0.jpg', mimetype='image/jpg')
    elif type==2:
        os.chdir("/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN")
        global mywords
        return mywords
        return send_file('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/flowers/caption/sentence0.jpg', mimetype='image/jpg')
    else:
        print("Input type not supported")
    return 'Success!'

@app.route('/post_test/', methods=['POST'])
def post_test():
    return send_file('./bird.png', mimetype='image/png')
    return send_file('/home/teno/Internship/Cond_Img_WGAN/T2I/StackGAN/Data/birds/caption/sentence0.jpg', mimetype='image/jpg')

if __name__ == "__main__":
    app.run(debug=True)
