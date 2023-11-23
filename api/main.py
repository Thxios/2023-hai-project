import os
import base64
import json
import io
from fastapi import FastAPI, UploadFile
from PIL import Image, ImageDraw
from typing import List, Optional
import pydantic
from uuid import uuid4
from detect.detect_ingredients import detect_ingredients

from recipe.search import FindRecipe

# class TestDetector:
#     def __init__(self, model_path):
#         self.model = load_model(model_path)

#     def process(self, image_name):
#         detect_ingredients(image_name)
#         # output = 
#         # image = image.convert('RGB')
#         # draw = ImageDraw.Draw(image)
#         # w, h = image.size
#         # draw.rectangle((w // 4, h // 4, 3*w // 4, 3*h // 4), outline=(255, 0, 0), width=3)
#         return {
#             'bbox': image,
#             'ingredient': ['김치', '간장', '밥', '참치']
#         }

class TestRecipeRetriever:
    sample1 = json.loads('''
    {"title":"가지볶음보다 맛있는 가지 스테이크 맛보면 멈출 수 없어요.","url":"https://www.10000recipe.com/recipe/6963110","author":"요알남Mingstar","description":"가지로 만드는 스테이크입니다. 덮밥으로 만들어도 맛있어요~ 단짠 소스가 아주 좋습니다. 꼭 만들어 보세요.","servings":1,"ingredients":["가지 1개","간장 2Ts","설탕 1.5Ts","식초 1Ts","다진 마늘 1/2Ts","버터 2Ts"],"totalTime":"PT20M","reviewCount":195,"instructions":[{"text":"가지의 꼭지 부분은 자르고 통으로 두께 1~2cm 크기로 자른다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/08/09/4d8afc1abf4c2b0c33be016df99b984a1.jpg"},{"text":"자른 가지는 그릇에 담아 전자레인지에 4~5분 정도 돌린다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/08/09/4c1cffdba978944341614f69c2177b651.jpg"},{"text":"간장, 설탕, 식초, 다진 마늘을 넣고 양념을 만든다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/08/09/97aafe77cbd010035ec88dc29641e0651.jpg"},{"text":"팬에 버터를 넣고 가지를 약불에서 앞뒤로 굽는다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/08/09/8f0de34b09d6ea57d286c9409db387a41.jpg"},{"text":"가지의 수분이 빠지고 노릇해지면 양념을 바른다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/08/09/c09faa9b50be6684b18c03e041f1eeaf1.jpg"},{"text":"양념을 바른 가지는 약불에서 앞뒤로 굽는다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/08/09/efc68708c267d6b415bbc279430fd1f21.jpg"}]}
    ''')
    sample2 = json.loads('''
    {"title":"돼지고기 김치찌개 달인이 되는 황금레시피","url":"https://www.10000recipe.com/recipe/6961294","author":"수필집밥","description":"나만 알고싶은 돼지고기김치찌개 레시피","servings":4,"ingredients":["돼지고기 앞다리살 500g","배추김치 1쪽","대파 1개","청양고추 2개","물 800ml","된장 1수저","들기름 or 참기름 2수저","설탕 1/2수저","다진마늘 1수저","후추 2꼬집"],"totalTime":"PT30M","reviewCount":311,"instructions":[{"text":"키친타올로 고기 핏물을 제거하고 먹기 좋은 크기로 숭덩숭덩 잘라주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/f6e1d124d4c3c10c6205c5b5c49527381.jpg"},{"text":"김치도 먹기 좋은 크기로 쫑쫑 썹니다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/5b44a7849cc30e27c92b7a8a74c8ea371.jpg"},{"text":"냄비에 들기름 2수저와 된장 1수저 넣고 수저로 섞어주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/5d3d04eed38be8dbfd74550cc9cf70bc1.jpg"},{"text":"섞은 양념은 약불에서 짙은 갈색이 될때까지 볶아줍니다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/635cb9edb465662669f01b7943fbcd1a1.jpg"},{"text":"썰어놓은 고기와 설탕 1/2수저 넣고 중불로 올려 볶아주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/4d9277c9639d8169301880f5429e42281.jpg"},{"text":"고기 겉면이 익을 때까지 잘 볶아주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/e0294c8837b6e1016ac6bd187cfbe1a71.jpg"},{"text":"썰어놓은 김치를 넣고 열심히 볶아주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/9eafebb734199de16886ed20bbe288e41.jpg"},{"text":"양념과 수분이 다 졸아들 때까지만 볶으시면 됩니다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/c8371ede348ea411ac274ce97d9624261.jpg"},{"text":"물 800ml를 넣고 강불로 끓여주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/23b90e8cc5bb8f7952e32495bfbde6a91.jpg"},{"text":"강불에서 팔팔 끓으면 뚜껑 덮고 약불로 줄여 20분간 끓여주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/e24045201a7bfef3837c9469623dea761.jpg"},{"text":"그동안 대파는 어슷썰고 청양고추는 송송 썰어주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/2791a952f3a6697752d9319af22c52e31.jpg"},{"text":"20분 뒤 불을 중불로 올린 뒤 다진마늘 1수저와 후추 2꼬집을 넣고 저어주세요.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/477e1eb74124d080a77ec78794c1f6181.jpg"},{"text":"다시 팔팔 끓어오르기 시작하면 대파와 청양고추를 넣고 5분 더 끓여줍니다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/beb34e66acd580c40c70dbe4f4bb02d61.jpg"},{"text":"모든 재료가 푹 익으면 완성입니다. 김치찌개는 오래 끓여먹어도 맛있으니 취향대로 더 끓여서 드셔도 됩니다.","image":"https://recipe1.ezmember.co.kr/cache/recipe/2021/07/06/b0f950b497d6d5b15d13afefcf7138d71.jpg"}]}
    ''')

    def process(self, ingredients: List[str]):
        return [
            {
                'title': self.sample1['title'],
                'ingredient': self.sample1['ingredients'],
                'url': self.sample1['url'],
            },
            {
                'title': self.sample2['title'],
                'ingredient': self.sample2['ingredients'],
                'url': self.sample2['url'],
            }
        ]



# detector = TestDetector()
# recipe_retriever = TestRecipeRetriever()
recipe_retriever = FindRecipe.load_from_file(
    'recipe/recipe_ingredient_mapped.jsonl',
    'recipe/detection_ingredient_class.json'
)

app = FastAPI()

@app.get('/')
def get_root_test():
    return {
        'running': True
    }

@app.get('/list_ingredient')
def get_all_possible_ingredients_list():
    return {
        'ingredient': recipe_retriever.classes
    }

@app.post('/detect')
async def detect(file: UploadFile):
    content = await file.read()
    filename = f"{uuid4()}"
    input_image = f"{filename}.jpg"

    with open(os.path.join("input_image", input_image), "wb") as fp:
        fp.write(content)

    detect_ingredients(input_image)
    # detector.process(filename)

    response_data = {
        'bbox': None,
        'ingredient': []
    }

    # bbox가 그려진 이미지 : bbox_(image_name).jpg
    # 식재료 리스트 : ingredients_(image_name).json
    with open(os.path.join("outputs", f"bbox_{filename}.jpg"), "rb") as fp:
        img_ = fp.read()
        response_data['bbox'] = base64.b64encode(img_).decode('utf-8')

    with open(os.path.join("outputs", f"ingredients_{filename}.json"), "r") as fp:
        ingredient_list = fp.read()
        response_data['ingredient'] = json.loads(ingredient_list)        

    return response_data
        # return {"filename":filename}

# class DetectQuery(pydantic.BaseModel):
#     image: str

# @app.post('/detect')
# async def post_detect(req: DetectQuery):
#     img = Image.open(io.BytesIO(base64.b64decode(req.image)))
#     ret = detector.process(img)
#     bbox_img = io.BytesIO()
#     ret['bbox'].save(bbox_img, format='png')
#     return {
#         'bbox': base64.b64encode(bbox_img.getvalue()).decode('utf-8'),
#         'ingredient': ret['ingredient']
#     }


class RecipeQuery(pydantic.BaseModel):
    ingredient: List[str]
    k: Optional[int] = 3


@app.post('/recipe')
async def post_recipe(req: RecipeQuery):
    # ret = recipe_retriever.process(req.ingredient)
    ret = recipe_retriever.find(req.ingredient, req.k)
    return {
        'recipes': ret
    }
