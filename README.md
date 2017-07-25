## Summary

TextImager converts text from printed media or hand written ones to an image that describes the meaning of the given sentence. We use TJbot as user interaction platform, which has multiple input and output interfaces such as USB microphone, Bluetooth speaker and a display. We also leverage a high performance computer (IBM Minsky GPU DevBox with PowerAI) as a server for text to image generation process. [Video for demo and business pitch](https://youtu.be/lMJXau7v89s )

## What's included

The main program includes two parts: “textImager.py” that runs on TJbot, and “server.py” which runs on the high performance server computer. “textImager.py” starts with waiting for a speech command for taking image through its camera. This is done by using IBM Bluemix's speech to text API. Once the image is taken, it will be sent to the server for text recognition and image generation based on the recognized text. Once the image is generated it will be sent from the server to TJbot for display. The text recognition is also accomplished with IBM Bluemix Visual Recognition API. The text to image generation process uses Generative Adversarial Networks (GAN). GAN is a deep neural network built with Caffe and TensorFlow open source library. The "NeuralNet" folder includes two types of deep neural networks. The "Word2Image" generates image from a single word and "Sentence2Image" generates image from a sentence. 

## How to run

Run the “server.py” on server computer first, when it starts and wait for response, run “textImager.py” on TJbot and follow the voice guidance.

## Prerequisite packages (Python 2.7)

On the TJbot:

**Pyaudio**

**Speech-recognition**

**Pillow**

**Tkinter**

On the server:

**Watson developer cloud** 

**TensorFlow**

**Caffe**

**Flask**
