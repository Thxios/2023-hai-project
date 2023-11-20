
import requests
import base64
import json
from PIL import Image
import io


def detect_send():
    with open('img.jpg', 'rb') as f:
        img_content = f.read()

    req = {
        'image': base64.b64encode(img_content).decode('utf-8')
    }
    resp = requests.post('http://127.0.0.1:8000/detect', json=req).json()

    img = Image.open(io.BytesIO(base64.b64decode(resp['bbox'])))
    img.save('resp.png')

    # print(json.dumps(req, indent=2, ensure_ascii=False))
    print(json.dumps(resp, indent=2, ensure_ascii=False))


def recipe_send():

    req = {
        'ingredient': ['mayonnaise', 'mozzarella_cheese', 'bread'],
        'k': 3,
    }
    resp = requests.post('http://127.0.0.1:8000/recipe', json=req).json()
    # print(json.dumps(req, indent=2, ensure_ascii=False))
    print(json.dumps(resp, indent=2, ensure_ascii=False))


def get_list_all():

    resp = requests.get('http://127.0.0.1:8000/list_ingredient').json()
    print(json.dumps(resp, indent=2, ensure_ascii=False))


# detect_send()
# recipe_send()
get_list_all()



