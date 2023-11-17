
import requests
import base64


def detect_send():
    with open('img.jpg', 'rb') as f:
        img_content = f.read()

    resp = requests.post('http://127.0.0.1:8000/detect', json={
        'image': base64.b64encode(img_content).decode('utf-8')
    })

    print(resp.json())


def recipe_send():

    resp = requests.post('http://127.0.0.1:8000/recipe', json={
        'ingredient': ['과일', '사과', '배'],
    })
    print(resp.json())



recipe_send()



