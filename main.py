

import base64
import json
import io
from fastapi import FastAPI
from PIL import Image, ImageDraw
from typing import List, Optional, Type
import pydantic

from recipe.base import BaseRecipeRetriever
from recipe.search import FindRecipe
from recipe.search_cossim import FindRecipeCosSim



class TestDetector:
    def process(self, image: Image.Image):
        image = image.convert('RGB')
        draw = ImageDraw.Draw(image)
        w, h = image.size
        draw.rectangle((w // 4, h // 4, 3*w // 4, 3*h // 4), outline=(255, 0, 0), width=3)
        return {
            'bbox': image,
            'ingredient': ['김치', '간장', '밥', '참치']
        }



detector = TestDetector()
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


class DetectQuery(pydantic.BaseModel):
    image: str


@app.post('/detect')
async def post_detect(req: DetectQuery):
    img = Image.open(io.BytesIO(base64.b64decode(req.image)))
    ret = detector.process(img)
    bbox_img = io.BytesIO()
    ret['bbox'].save(bbox_img, format='png')
    return {
        'bbox': base64.b64encode(bbox_img.getvalue()).decode('utf-8'),
        'ingredient': ret['ingredient']
    }


class RecipeQuery(pydantic.BaseModel):
    ingredient: List[str]
    k: Optional[int] = 3


@app.post('/recipe')
async def post_recipe(req: RecipeQuery):
    ret = recipe_retriever.process(req.ingredient, req.k)
    return {
        'recipes': ret
    }
