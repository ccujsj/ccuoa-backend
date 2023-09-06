from pydantic import BaseModel

from .BaseTimestampMixin import TimestampMixin
from tortoise import fields


class QuickLink(TimestampMixin):
    id = fields.IntField(pk=True,description="Primary key")
    link_name = fields.CharField(null=False,max_length=255,description="链接名称")
    link_url = fields.CharField(null=True,max_length=1022,description="链接url")


    class Meta:
        table_description = "快速链接表"
        table = "quick_link"

class LinkSchema(BaseModel):
    link_name:str
    link_url:str
class Text(TimestampMixin):
    id = fields.IntField(pk=True,description="Primary key")
    text_type = fields.IntField(null=False,default=0,description="类型")
    text_key = fields.CharField(null=False,max_length=255,unique=True,description="键")
    text_value = fields.CharField(null=False,max_length=255,unique=True,description="值")

    class Meta:
        table_description = "文本kv值"
        table = "text_kv"

class TextSchema(BaseModel):
    text_type:int
    text_key:str
    text_value:str
