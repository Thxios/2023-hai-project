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

    | field   | value        | description       |
    |---------|--------------|-------------------|
    | `recipes` | array of json | retrieved recipes |
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
        "과일", 
        "사과", 
        "배"
      ]
    }
    ```

- response sample
    ```json
    {
      "recipes": [
        {
          "title": "가지볶음보다 맛있는 가지 스테이크 맛보면 멈출 수 없어요.",
          "ingredient": [
            "가지 1개",
            ...
            "버터 2Ts"
          ],
          "url": "https://www.10000recipe.com/recipe/6963110"
        },
        {
          "title": "돼지고기 김치찌개 달인이 되는 황금레시피",
          "ingredient": [
            "돼지고기 앞다리살 500g",
            ...
            "후추 2꼬집"
          ],
          "url": "https://www.10000recipe.com/recipe/6961294"
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


