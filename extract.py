from ast import main
import asyncio
import streamlit as st
from datetime import datetime,timedelta
import requests
import aiohttp

 
    
gecko_url = 'https://api.geckoterminal.com/api/v2/networks'

class networkPool:
    def __init__(self,id):
       self.network_id = id


    def send_request(self,to_fetch):
        response =  requests.get(gecko_url + to_fetch)
        if response.status_code == 200:
            result = response.json()
            return result
         

    def fetch_pools(self,to_type):
        result = self.send_request(to_type)
        #print(result['data'])
        pool_results = result['data']
        pool_datas = self.process_pools(pool_results)
        return pool_datas

    def process_pools(self,pool_results):
        pools_datas = []
        for pool in pool_results:
            pool_info  = { }
            pool_info['pool_name'] = pool['attributes']['name']
            pool_info['price'] = pool['attributes']['base_token_price_usd']
            pool_info['age'] = pool['attributes']['pool_created_at']
            pool_info['FDV'] = pool['attributes']['fdv_usd']
            pool_info['24H'] = pool['attributes']['price_change_percentage']['h24'] + '%'
            pool_info['pair'] = pool['attributes']['address']
            pools_datas.append(pool_info)
        return pools_datas


class infopage:
    def __init__(self):
        pass

    
    def fetchAll(self):
        
        async def fetchTokenDetail(session):
            current_time = datetime.now()
            new_time = current_time + timedelta(minutes=5)
            timestamp = int(new_time.timestamp())
            
            network_id = st.session_state['network_id']
            pool = st.session_state['pool']
            url = f"https://api.geckoterminal.com/api/v2/networks/{network_id}/pools/{pool}/ohlcv/minute?aggregate=1&before_timestamp={timestamp}&limit=1&currency=usd&token=base&include_empty_intervals=true"
            
            async with session.get(url) as response:
            # response = requests.get(url)
            # if response.status_code == 200:
                results = await response.json()
                address = results['meta']['base']['address'] # update this address on session
                tokenSymbol = results['meta']['base']['symbol']
                pairedToken = f"{results['meta']['base']['symbol']}/{results['meta']['quote']['symbol']}"

                st.session_state['token_address'] = address
                st.session_state['tokenSymbol'] = tokenSymbol
                st.session_state['pairedToken'] = pairedToken
                
        async def fetchtokenInfo(session):
            token_address = st.session_state['token_address']
            network_id = st.session_state['network_id']

            url = f"https://api.geckoterminal.com/api/v2/networks/{network_id}/tokens/{token_address}?include=top_pools"
            async with session.get(url) as response:
                # response = requests.get(url)
                results =  await response.json()
                data = results['data']['attributes']
                decimal = data['decimals']
                supply = data['normalized_total_supply']
                price = data['price_usd']
                volume_24 = data['volume_usd']['h24']
                market_cap = data['market_cap_usd']
                fdv = data['fdv_usd']
                liquidity = data['total_reserve_in_usd']
                image_url = data['image_url']

                st.session_state['decimal'] = decimal
                st.session_state['supply'] = supply
                st.session_state['price'] = price
                st.session_state['volume'] = volume_24
                st.session_state['market_cap'] = market_cap
                st.session_state['fdv'] = fdv
                st.session_state['liquidity'] = liquidity
                st.session_state['image_url'] = image_url

                pooldata = results['included'][0]['attributes']
                poolCreated = pooldata['pool_created_at'] # minus it from toda and showhour orminuts
                priceChanges = pooldata['price_change_percentage']
                m5 = priceChanges['m5']
                m15 = priceChanges['m15']
                m30 = priceChanges['m30']
                h1 = priceChanges['h1']
                h6 = priceChanges['h6']
                h24 = priceChanges['h24']

                st.session_state['poolCreated'] = poolCreated
                st.session_state['m5'] = m5
                st.session_state['m15'] = m15
                st.session_state['m30'] = m30
                st.session_state['h1'] = h1
                st.session_state['h6'] = h6
                st.session_state['h24'] = h24

        async def holders(session):
            # 426CEm43Pr4XeNqfmS3XVaKCKRjnwvkAuMLMxcf4pump
            token_address = st.session_state['token_address']
            network_id = st.session_state['network_id']
            url = f"https://api.geckoterminal.com/api/v2/networks/{network_id}/tokens/{token_address}/info"
            async with session.get(url) as response:
                # response = requests.get(url)
                results = await response.json()
                holders = results['data']['attributes']['holders']['count']
                # st.write(results)
                st.session_state['holders'] = holders

        async def main():
            async with aiohttp.ClientSession() as session:
                task1 = asyncio.create_task(fetchTokenDetail(session))
                await task1
                tasks2 = [fetchtokenInfo(session),holders(session)]
                fetch = asyncio.gather(*tasks2)
                await fetch
        
        asyncio.run(main())

