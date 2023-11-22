

import json
import schema


class BaseRecipeRetriever:
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

    def process(self, ingredients, k):
        raise NotImplementedError

    def filter_ingredients(self, ingredients):
        known = []
        for ing in ingredients:
            if ing in self.classes:
                known.append(ing)
            else:
                print(f'unknown ingredient {ing}')
        return known

    @classmethod
    def load_from_file(
            cls,
            recipes_jsonl_path,
            classes_json_path,
    ):
        recipes = cls.load_recipes(recipes_jsonl_path)
        classes = cls.load_classes(classes_json_path)
        return cls(recipes, classes)

    @classmethod
    def load_recipes(cls, recipes_jsonl_path):
        with open(recipes_jsonl_path, 'r', encoding='utf-8') as f:
            recipes = [json.loads(line) for line in f.readlines()]

        recipes = cls.recipes_schema.validate(recipes)
        return recipes

    @classmethod
    def load_classes(cls, classes_json_path):
        with open(classes_json_path, 'r', encoding='utf-8') as f:
            classes = json.load(f)

        classes = cls.classes_schema.validate(classes)
        return classes




