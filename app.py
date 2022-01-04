from flask import Flask, render_template, request
# importing the required libraries
from flask import Flask
from torchvision import transforms
import torch
import PIL
import numpy as np

app = Flask(__name__)

# Use the trained model (Resnet50) with 80% Accuracy
model = torch.load('./trained_model/resnet_model.py')
classes = np.load('classes.npz')['arr_0']


@app.route('/')
def home():
    return render_template('./home.html')


@app.route('/image-upload', methods=["POST"])
def get_data():
    print("Hello World")
    image = request.files['file']
    print("Image", image)
    tp, ps = predict(image, model, topk=5)
    print("Top Prediction: ", classes[ps[0]])
    top_pred = classes[ps[0]]
    pred1 = classes[ps[1]]
    pred2 = classes[ps[2]]
    pred3 = classes[ps[3]]
    pred4 = classes[ps[4]]
    array = np.array([top_pred, pred1, pred2, pred3, pred4])
    d = dict(enumerate(array.flatten(), 1))
    return d


# Define the function to get the images from the url and predicted the class
def predict(image, model, topk=5):
    pil_in = PIL.Image.open(image)
    transform = transforms.Compose([transforms.Resize((244, 244)),
                                    transforms.CenterCrop(224),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406],
                                                         [0.229, 0.224, 0.225])])
    pilTrans = transform(pil_in)
    img = np.array(pilTrans)
    # np to tensor
    img_tensor = torch.from_numpy(img).type(torch.FloatTensor)
    dimen = img_tensor.unsqueeze_(0)
    model.eval()
    with torch.no_grad():
        output = model.forward(dimen)
    top_prediction = output.topk(topk)[1]
    p = np.array(top_prediction)[0]
    o_guesses = np.array(top_prediction)[0]
    return p, o_guesses


if __name__ == '__main__':
    app.run()
