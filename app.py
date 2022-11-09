from flask import Flask, request
import torch
import os

app = Flask(__name__)

model = torch.hub.load('./yolov5', 'custom', './models/pepper_napacabbage_bean/best.pt', source='local')


@app.route('/diagnose', methods=['POST'])
def predict():
    file = request.files['file']
    file.save('./temp/' + file.filename)
    predict_img = './temp/' + file.filename

    temp = model(predict_img)
    temp.save()
    result = temp.pandas().xyxy[0]

    diseases = []
    for i in range(len(result)):
        diseases.append({
            'name': result['name'][i], 'confidence': result['confidence'][i]
        })

    res = {
        'diseases': diseases,
        'img': file.filename
    }

    os.remove('./temp/' + file.filename)

    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
