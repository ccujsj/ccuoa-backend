from fastapi import APIRouter, Security
from pydantic import BaseModel
from core.authorize import check_permissions
from datasource.redis import info_cache
from model.Info import Text, TextSchema
from response.resexception import E500
from response.stdresp import StdResp
import pickle

info_router = APIRouter()

@info_router.on_event("startup")
async def startup_event():
    info_router.lifespan_context.redis = await info_cache()


@info_router.on_event("shutdown")
async def shutdown_event():
    cache = await info_router.lifespan_context.redis
    await cache.close()


async def flush_redis():
    try:
        texts = await Text.all()
        ret = []
        for i in texts:
            ret.append(i.__dict__)
        await info_router.lifespan_context.redis.delete(name="info")
        await info_router.lifespan_context.redis.set(name="info", value=pickle.dumps(ret))
        return True
    except:
        return False


class InfoResponseSchema(BaseModel):
    id: int
    text_type: str
    text_key: str
    text_value: str


@info_router.get("/get/info/all",
                 description="获取全部信息",
                 name="获取信息")
async def get_all_info_list():
    ret = []
    try:
        res = info_router.lifespan_context.redis.get('info')
        texts = pickle.loads(res)  # list
        for i in texts:
            ret.append(InfoResponseSchema(**i.__dict__))
        return ret
    except:
        texts = await Text.all()
        for i in texts:
            ret.append(InfoResponseSchema(**i.__dict__))
        return ret


@info_router.post("/put/info/text",
                  description="上传一个信息",
                  name="上传信息", dependencies=[Security(check_permissions, scopes=["staff"])])
async def put_single_text(txt: TextSchema):
    await flush_redis()
    await Text.create(**txt.dict())
    return StdResp(data=str(txt.dict()))


@info_router.get("/delete/info/byKey",
                 description="通过键来删除一个信息",
                 name="删除信息", dependencies=[Security(check_permissions, scopes=["staff"])])
async def delete_info_by_textKey(key: str):
    target = await Text.filter(text_key=key).first()
    await target.delete()
    await flush_redis()
    return StdResp(data=key)


@info_router.get("/flush/redis",
                 description="手动刷新Redis缓存",
                 name="刷新Redis", dependencies=[Security(check_permissions, scopes=["staff"])])
async def GET_Info_Flush_Redis():
    ret = await flush_redis()
    if ret:
        return StdResp(data="Flush Successful")
    else:
        return E500("Error on Redis Server")
