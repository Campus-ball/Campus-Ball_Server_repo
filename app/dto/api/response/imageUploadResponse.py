from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class ImageUploadData(BaseModel):
    imgUrl: str


class ImageUploadResponse(BaseResponse[ImageUploadData]):
    pass


