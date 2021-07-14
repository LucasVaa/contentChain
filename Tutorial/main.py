from fastapi import FastAPI, Header, Response
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from pydantic.errors import NotDigitError

appForQueryParameters = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@appForQueryParameters.get("/")
async def root():
    return {"message": "Hello World"}

@appForQueryParameters.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 路径操作是按顺序依次运行的
@appForQueryParameters.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@appForQueryParameters.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# 如果你有一个接收路径参数的路径操作，但你希望预先设定可能的有效参数值，则可以使用标准的 Python Enum 类型。 
@appForQueryParameters.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if (model_name == ModelName.alexnet):
        return {"model_name": model_name}
    if (model_name.value == "lenet"):
        return {"model_name": model_name}
    return {"model_name": model_name}

# 包含路径的路径参数
@appForQueryParameters.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# 声明不属于路径参数的其他函数参数时，它们将被自动解释为"查询字符串"参数
# 查询字符串是键值对的集合，这些键值对位于 URL 的 ？ 之后，并以 & 符号分隔。
# http://127.0.0.1:8000/items/?skip=0&limit=10
# 由于它们是 URL 的一部分，因此它们的"原始值"是字符串。
# 但是，当你为它们声明了 Python 类型（在上面的示例中为 int）时，它们将转换为该类型并针对该类型进行校验。
@appForQueryParameters.get("/items/")
async def read_item(skip :int = 0, limit :int = 10):
    return skip + limit

# 你可以将它们的默认值设置为 None 来声明可选查询参数
@appForQueryParameters.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# 查询参数类型转换
# 声明 bool 类型，它们将被自动转换 True = 1 = true = on = yes = 任何其他的变体形式（大写，首字母大写等等）
@appForQueryParameters.get("/items_1/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

# 当你为非路径参数声明了默认值时（目前而言，我们所知道的仅有查询参数），则该参数不是必需的。

# 如果你不想添加一个特定的值，而只是想使该参数成为可选的，则将默认值设置为 None。

# 但当你想让一个查询参数成为必需的，不声明任何默认值就可以：

# 同时声明多个路径参数和查询参数
# http://127.0.0.1:8000/users/3/items/3?q=123&short=F
@appForQueryParameters.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


appForRequestBody = FastAPI()

# 创建数据模型
class Item(BaseModel):
    name: str
    des: Optional[str] = None
    price: float
    tax: Optional[float] = None

@appForRequestBody.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    item_dict.update({"up": "123"})
    return item_dict

# 请求体 + 路径参数 + 查询参数
# 如果在路径中也声明了该参数，它将被用作路径参数。
# 如果参数属于单一类型（比如 int、float、str、bool 等）它将被解释为查询参数。
# 如果参数的类型被声明为一个 Pydantic 模型，它将被解释为请求体。

@appForRequestBody.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

## Header 参数

appForHeaderParameters = FastAPI()

# 你可以使用定义 Query, Path 和 Cookie 参数一样的方法定义 Header 参数。
@appForHeaderParameters.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

