
import json
import schema


class FindRecipe:
    recipes_schema = schema.Schema(
        [
            {
                'recipe': {
                    'title': str,
                    'ingredient': [str],
                    'url': str
                },
                'mapped': [
                    lambda x: isinstance(x, str) or x is None
                ]
            }
        ]
    )

    classes_schema = schema.Schema(
        [
            str
        ]
    )


    def __init__(self, recipes, classes):
        self.recipes = self.recipes_schema.validate(recipes)
        self.classes = self.classes_schema.validate(classes)

    def find(self, having_ings, k=5):
        known = []
        for ing in having_ings:
            if ing in self.classes:
                known.append(ing)
            else:
                print(f'unknown ingredient {ing}')
        having_ings = known

        # 레시피 리스트 초기화
        recipe_list = []

        # 모든 레시피에 대해 가지고 있는 재료 중 포함된 재료의 개수 계산
        for recipe in self.recipes:
            recipe_mapped = recipe.get('mapped', [])
            count = sum(ingredient in having_ings for ingredient in recipe_mapped)
            recipe_list.append({'count': count, 'recipe': recipe['recipe']})

        # 가지고 있는 재료 중 레시피에 포함된 재료의 개수가 가장 많은 레시피 5개 찾기
        top_k_recipes = sorted(recipe_list, key=lambda x: x['count'], reverse=True)[:k]

        found = [x['recipe'] for x in top_k_recipes]
        return found

    @staticmethod
    def load_from_file(
            recipes_jsonl_path,
            classes_json_path,
    ):
        recipes = load_recipes(recipes_jsonl_path)
        classes = load_classes(classes_json_path)
        return FindRecipe(recipes, classes)



def load_recipes(recipes_jsonl_path):
    with open(recipes_jsonl_path, 'r', encoding='utf-8') as f:
        recipes = [json.loads(line) for line in f.readlines()]

    recipes = FindRecipe.recipes_schema.validate(recipes)
    return recipes


def load_classes(classes_json_path):
    with open(classes_json_path, 'r', encoding='utf-8') as f:
        classes = json.load(f)

    classes = FindRecipe.classes_schema.validate(classes)
    return classes


