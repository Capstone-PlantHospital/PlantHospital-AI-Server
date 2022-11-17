import os
import shutil
import torch
from ..util.image import upload_file


class DiagnoseService:
    def predict(self, crop, file):
        BUCKET = "planthospital"

        file.save('./temp/' + file.filename)
        predict_img = './temp/' + file.filename

        if crop == 'pepper' or crop == 'bean' or crop == 'napa_cabbage':
            # model = torch.hub.load('ultralytics/yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt', device='cpu')
            model = torch.hub.load('./yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt',
                                   source='local', device='cpu')
        else:
            # TODO:모델 변경하기
            model = torch.hub.load('./yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt',
                                   source='local', device='cpu')

        temp = model(predict_img, size=320)
        temp.save()
        result = temp.pandas().xyxy[0]

        diseases = []
        disease_kind = {}
        for i in range(len(result)):
            if result['name'][i] not in disease_kind:
                disease_kind[result['name'][i]] = result['confidence'][i]
            else:
                disease_kind[result['name'][i]] = max(result['confidence'][i], disease_kind[result['name'][i]])

        for disease in disease_kind:
            diseases.append({
                'name': disease, 'confidence': disease_kind[disease]
            })

        img_url = upload_file(file.filename, BUCKET)

        res = {
            'diseases': diseases,
            'img_url': img_url
        }

        os.remove('./temp/' + file.filename)
        shutil.rmtree('./runs/detect')

        return res

