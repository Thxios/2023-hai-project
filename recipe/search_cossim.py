
from base import BaseRecipeRetriever
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



class FindRecipeCosSim(BaseRecipeRetriever):
    def __init__(self, recipes, classes):
        super().__init__(recipes, classes)

        seen = set()
        for recipe in self.recipes:
            for ing in recipe['mapped']:
                if ing is not None:
                    seen.add(ing)

        self.support = [ing for ing in self.classes if ing in seen]
        self.one_hot_vectors = np.array([
            self.make_one_hot(recipe['mapped']) for recipe in self.recipes
        ])


    def make_one_hot(self, mapped):
        ings = set(filter(lambda x: x is not None, mapped))
        return np.array([1 if ig in ings else 0 for ig in self.support])


    def find(self, having_ings, k=5):
        having_ings = self.filter_ingredients(having_ings)
        query = self.make_one_hot(having_ings).reshape((1, -1))
        if np.sum(query) == 0:
            return []

        sim = cosine_similarity(self.one_hot_vectors, query).reshape(-1)
        sim_idx = sorted(zip(sim, range(len(self.recipes))), key=lambda x: x[0], reverse=True)[:k]

        found = [self.recipes[idx]['recipe'] for _, idx in sim_idx]
        return found


if __name__ == '__main__':
    finder = FindRecipeCosSim.load_from_file(
        'recipe_ingredient_mapped.jsonl',
        'detection_ingredient_class.json'
    )

    sample = ['mayonnaise', 'mozzarella_cheese', 'bread']

    out = finder.find(sample)
    print(*out, sep='\n')


