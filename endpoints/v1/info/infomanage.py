from fastapi import APIRouter, Security
from pydantic import BaseModel
from starlette.requests import Request

from core.authorize import check_permissions
from core.utils import get_header_username
from curd.moral import DL_Moral_Update_Record, MoralRecordPostSchema, DL_StudentMoral_Retrieve_By_status
from model.Info import QuickLink, Text, TextSchema, LinkSchema
from response.resexception import E500
from response.stdresp import StdResp

info_router = APIRouter()


@info_router.get("/get/info/all")
async def get_all_info_list():
    texts = await Text.all()
    ret = []
    for i in texts:
        ret.append(i.__dict__)
    return ret


@info_router.post("/put/info/text", dependencies=[Security(check_permissions, scopes=["staff"])])
async def put_single_text(txt: TextSchema):
    await Text.create(**txt.dict())
    return StdResp(data=str(txt.dict()))


@info_router.get("/delete/info/byKey", dependencies=[Security(check_permissions, scopes=["staff"])])
async def delete_info_by_textKey(key: str):
    target = await Text.filter(text_key=key).first()
    await target.delete()
    return StdResp(data=key)
