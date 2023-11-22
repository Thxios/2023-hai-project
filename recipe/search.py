
from recipe.base import BaseRecipeRetriever


class FindRecipe(BaseRecipeRetriever):

    def find(self, having_ings, k=5):
        having_ings = self.filter_ingredients(having_ings)

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
