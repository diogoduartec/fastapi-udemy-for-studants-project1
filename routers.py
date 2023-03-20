from asyncio import gather
from fastapi import APIRouter, Query, Path
from converter import sync_converter, async_converter
from schemas import ConverterInput, ConverterOutput


router = APIRouter(prefix='/converter')

# path parameter
# query parameter

# /converter/BRL?to=USD,EUR

@router.get('/{from_currency}')
def converter(from_currency: str, to_currencies: str, price: float):
    to_currencies = to_currencies.split(',')
    
    result = []

    for currency in to_currencies:
        response = sync_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        result.append(response)
    
    return result


@router.get('/async/{from_currency}')
async def converter(
    from_currency: str = Path(max_length=50, regex='^[A-Z]{3}$'),
    to_currencies: str = Query(max_length=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'),
    price: float = Query(gt=0)
):
    to_currencies = to_currencies.split(',')
    
    corotines = []
    
    for currency in to_currencies:
        response = async_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        corotines.append(response)

    result = await gather(*corotines)
    
    return result


@router.get('/async/v2/{from_currency}',response_model=ConverterOutput)
async def converter(
    body: ConverterInput,
    from_currency: str = Path(max_length=50, regex='^[A-Z]{3}$'),
):    
    corotines = []
    
    to_currencies = body.to_currencies
    price = body.price

    for currency in to_currencies:
        response = async_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        corotines.append(response)

    result = await gather(*corotines)
    
    return ConverterOutput(
        response_message='Successfully converted',
        converted_prices=result
    )