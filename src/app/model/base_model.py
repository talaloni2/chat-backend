from pydantic import BaseModel


def to_camel(string: str) -> str:
    split_string = string.split('_')
    return '{}{}'.format(split_string[0], ''.join(word.capitalize() for word in split_string[1:]))


class JsonBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
