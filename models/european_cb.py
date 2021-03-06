import aiohttp
import xml.etree.ElementTree as ET
from .fetcher import Fetcher


class EuropeanCBAPI(Fetcher):

    _URL = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'

    async def get_eur_usd_exchange_rate(self, loop, callback=None):
        async with aiohttp.ClientSession(loop=loop) as session:
            response = await self._fetch(session, self._URL)
            tree = ET.fromstring(response)
            for rate in tree[2][0]:
                if rate.get('currency') == 'USD':
                    if callback is not None:
                        callback(rate.get('rate'))
                    return rate.get('rate')
