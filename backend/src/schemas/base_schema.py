from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace = True,
        str_min_length = 1,
        extra = "forbid"
    )