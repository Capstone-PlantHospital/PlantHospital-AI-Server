import os
import torch


class DiagnoseService:
    def predict(self, crop, file):
        file.save('./temp/' + file.filename)
        predict_img = './temp/' + file.filename

        if crop == 'pepper' or crop == 'bean' or crop == 'napa_cabbage':
            model = torch.hub.load('ultralytics/yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt')
            # model = torch.hub.load('./yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt', source='local')
        else:
            # TODO:모델 변경하기
            model = torch.hub.load('./yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt', source='local')

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

        res = {
            'diseases': diseases,
            'img': file.filename
        }

        os.remove('./temp/' + file.filename)

        return res

