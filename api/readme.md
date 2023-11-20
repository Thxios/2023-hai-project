# API

---

## Run

### requirements
```shell
pip3 install fastapi uvicorn pillow
```

### run
```shell
uvicorn main:app
```

---

## API Document

### Detect

- Method : `POST`
- Path : `/detect`
- request json

    | field | value                |description|
    |-------|----------------------|---|
    | `image` | base64 encoded image |query image|

- response json

    | field | value               |description|
    |-------|---------------------|--|
    | `bbox` | base64 encoded image|query image with bounding box|
    | `ingredient`| array of strings|detected ingredients|

- request sample
    ```json
    {
      "image": "/9j/4AAQS ... +0Jkf//Z"
    }
    ```

- response sample
    ```json
    {
      "bbox": "iVBORw0KGgoAAAA ... ASUVORK5CYII=", 
      "ingredient": [
        "김치", 
        "간장", 
        "밥", 
        "참치"
      ]
    }
    ```

### Recipe Retrieve


- Method : `POST`
- Path : `/recipe`
- request json

    | field      | value           | description         |
    |------------|-----------------|---------------------|
    | `ingredient` | array of strings | list of ingredients |

- response json

    | field     | value          | description               |
    |-----------|----------------|---------------------------|
    | `recipes` | array of json  | retrieved recipes         |
    |  `k`        | int (optional) | maximum number of recipes |
  - recipe json

    | field | value            | description        |
    |-------|------------------|--------------------|
    | `title` | string           | recipe title       |
    | `ingredient` | array of strings | list of ingredients         |
    | `url`   | string           | recipe article url |
    


- request sample
    ```json
    {
      "ingredient": [
        "mayonnaise", 
        "mozzarella_cheese", 
        "bread"
      ],
      "k": 2
    }
    ```

- response sample
    ```json
    {
      "recipes": [
        {
          "title": "모닝빵콘치즈 간단간식 ",
          "ingredient": [
            "모닝빵 6개",
            "옥수수 콘 1컵",
            "마요네즈 1스푼",
            "허니 머스터드 1스푼",
            "후춧가루 약간",
            "피자치즈 70g"
          ],
          "url": "https://www.10000recipe.com/recipe/6881806"
        },
        {
          "title": "참치롤샌드위치 만들기 ",
          "ingredient": [
            "식빵 6장",
            "참치캔 1/2통",
            "오이 1/2개",
            "햄 약간",
            "양파 약간",
            "마요네즈 1+1/2숟갈",
            "백후추 약간",
            "마요네즈 1숟갈",
            "머스터드 소스 1/2숟갈"
          ],
          "url": "https://www.10000recipe.com/recipe/3687411"
        }
      ]
    }
    ```


### List all Ingredients

- Method : `GET`
- Path : `/list_ingredient`
- response json

    | field   | value            | description                      |
    |---------|------------------|----------------------------------|
    | `ingredient` | array of strings | list of all possible ingredients |

- response sample

    ```json
    {
      "ingredient": [
        "apple",
        "avocado",
        ...
        "lemon_juice",
        "red_wine"
      ]
    }
    ```


