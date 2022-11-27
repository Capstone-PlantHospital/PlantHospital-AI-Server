import os
import shutil
import cv2
import torch
from efficientnet_pytorch import EfficientNet
from ..util.image import upload_file


class DiagnoseService:
    BUCKET = "planthospital"

    def predict(self, crop, file):
        file.save('./temp/' + file.filename)
        predict_img = './temp/' + file.filename

        if crop == 'pepper' or crop == 'bean' or crop == 'napa_cabbage':
            # model = torch.hub.load('ultralytics/yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt', device='cpu')
            model = torch.hub.load('./yolov5', 'custom', './models/pepper_bean_napacabbage/best.pt',
                                   source='local', device='cpu')

            diseases, img_url = self.yolov5_model(model, file, predict_img)
        else:
            model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=7)
            device = torch.device('cpu')
            model.load_state_dict(torch.load('./models/radish_greenonion/crop_model.pt', map_location=device))
            model.eval()

            diseases, img_url = self.efficientnet_model(model, file, predict_img)

        res = {
            'diseases': diseases,
            'img_url': img_url
        }

        os.remove('./temp/' + file.filename)
        if os.path.isdir('./runs/detect'):
            shutil.rmtree('./runs/detect')

        return res

    def yolov5_model(self, model, file, predict_img):
        output = model(predict_img, size=320)
        output.save()
        result = output.pandas().xyxy[0]

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

        img_url = upload_file(file.filename, self.BUCKET)

        return diseases, img_url

    def efficientnet_model(self, model, file, predict_img):
        crop_disease = {
            0: 'green_onion_normal', 1: 'green_onion_purple_blotch', 2: 'green_onion_downy_mildew',
            3: 'green_onion_rust', 4: 'radish_normal', 5: 'radish_black_spot', 6: 'radish_downy_mildew'
        }
        diseases = []

        img = cv2.imread(predict_img)
        img = cv2.resize(img, (224, 224))
        img = img[:, :, ::-1].transpose((2, 0, 1)).copy()
        img = torch.from_numpy(img).float().div(255.0).unsqueeze(0)

        output = model(img)
        _, predict = torch.max(output, 1)

        diseases.append({
            'name': crop_disease[predict.item()], 'confidence': -1
        })

        img_url = upload_file(file.filename, self.BUCKET, 2)

        return diseases, img_url
