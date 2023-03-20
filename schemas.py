import re
from pydantic import BaseModel, Field, validator
from typing import List


class ConverterInput(BaseModel):
    price: float = Field(gt=0)
    to_currencies: List[str]

    @validator('to_currencies')
    def validate_to_currencies(cls, value):
        for currency in value:
            if not re.match('^[A-Z]{3}$', currency):
                raise ValueError(f'Invalid currency {currency}')
        return value


class ConverterOutput(BaseModel):
    response_message: str
    converted_prices: List[dict]
