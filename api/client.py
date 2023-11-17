
import requests
import base64
import json


def detect_send():
    with open('img.jpg', 'rb') as f:
        img_content = f.read()

    req = {
        'image': base64.b64encode(img_content).decode('utf-8')
    }
    resp = requests.post('http://127.0.0.1:8000/detect', json=req)

    # print(json.dumps(req, indent=2, ensure_ascii=False))
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


def recipe_send():

    req = {
        'ingredient': ['과일', '사과', '배'],
    }
    resp = requests.post('http://127.0.0.1:8000/recipe', json=req)
    # print(json.dumps(req, indent=2, ensure_ascii=False))
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


# detect_send()
recipe_send()



