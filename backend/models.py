from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Annotated, Any
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    google_id: str
    email: EmailStr
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Category(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    icon: str = "💰"
    user_id: Optional[str] = None

class Expense(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    amount: float = Field(..., ge=0)
    category_id: str
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    description: Optional[str] = None
    date: datetime
    currency: str = Field(default="USD")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
