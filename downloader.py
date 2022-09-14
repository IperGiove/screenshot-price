from omegaconf import OmegaConf
from typing import Any, Awaitable
import pandas as pd
import httpx
import asyncio
import os


DIR = os.getcwd()#.replace("/build/exe.linux-x86_64-3.9/", "")
CFG = OmegaConf.load(f'{DIR}/config/host.yaml')


async def run_parallel(*functions: Awaitable[Any]) -> None:
    return await asyncio.gather(*functions)


async def requests_and_parse(
    url: str, 
    params: dict = {}, 
    header: dict = {"Content-Type": "application/json"},
    http_method: str = "GET"
    ) -> dict:

    async with httpx.AsyncClient() as client:
        r = await client.request(
            method=http_method, url=url, params=params, headers=header
    )
    return r.json()


def params_for_request(
    exchange:str, 
    quote:str, 
    base:str
    ) -> tuple[str, dict or None]:

    pair = quote + CFG[exchange]["pairs_merge"] + base

    if CFG[exchange]["query"] == None:
        query = None
        url = CFG[exchange]["host"] + CFG[exchange]["price"]["endpoint"] + pair
    else:
        query = {CFG[exchange]["query"]: pair}
        url = CFG[exchange]["host"] + CFG[exchange]["price"]["endpoint"]

    return url, query


def data_for_request():
    return [
        params_for_request(exchange, quote, base)
        for exchange in CFG["exchanges"]
            for quote in CFG["pairs"]["quote"]
                for base in CFG["pairs"]["base"]
    ]


def preprocessing(exchange: str, row_data: dict or list) -> tuple[float, str]:
    if CFG[exchange]["where_data"] == None:
        return (
            round(
                float(row_data[CFG[exchange]["price"]["price_data"]]),
                ndigits = 2),
            row_data[CFG[exchange]["price"]["pair_definition"]].replace(
                CFG[exchange]["pairs_merge"], "")
        )
    else:
        return (
            round(
                float(row_data[CFG[exchange]["where_data"]][CFG[exchange]["price"]["price_data"]]), 
                ndigits = 2),
            row_data[CFG[exchange]["where_data"]][CFG[exchange]["price"]["pair_definition"]].replace(
                CFG[exchange]["pairs_merge"], "")
        )


async def batch_of_request(urls_params: list) -> dict:
    return await run_parallel(
        *[requests_and_parse(*url_param) for url_param in urls_params]
    )
    

def cleaning_data(row_datas: list) -> pd.DataFrame:
    data = pd.DataFrame({
            "exchange": [],
            "pair": [],
            "price": []
        })

    for exchange, row_data in zip(CFG["exchanges"], row_datas):
        price, pair = preprocessing(exchange, row_data)
        data.loc[len(data.index)] = [exchange, pair, price]
    
    return data.sort_values(by=["price"])


async def main() -> pd.DataFrame:
    urls_params = data_for_request()
    row_datas = await batch_of_request(urls_params)
    return cleaning_data(row_datas)
    

if __name__ == "__main__":
    data = asyncio.run(main())
    print(data)