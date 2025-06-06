import asyncio,aiohttp
import time
import streamlit as st
import requests
from datetime import datetime,timezone
import  streamlit.components.v1 as components
from extract import infopage 

import streamlit as st

# st.set_page_config(
#     page_title="TokenInfo",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state='auto',
#     menu_items={
#         'Get Help':None, #'https://www.extremelycoolapp.com/help',
#         'Report a bug': None,# "https://www.extremelycoolapp.com/bug",
#         'About': None #" This is a header. This is an *extremely* cool app!"
#     }
# )

if 'pool' in st.session_state:
    pool = st.session_state['pool']
    network_id = st.session_state['network_id']
else:
    # pool = '2VzfCX2SFeXL6RhE941SNYRhaEtUt4PectubG8wrdtEa'
    # network_id = 'solana'
    pass

pageInfo = infopage()



def format_number(number):

    if not isinstance(number, (int,float,str)):
        return str(number)
    
    abs_num = abs(float(number))
    if abs_num >= 1_000_000_000:
        return f"{abs_num/1_000_000_000:.1f}B"
    elif abs_num >= 1_000_000:
        return f"{abs_num/1_000_000:.1f}M"
    elif abs_num >= 1_000:
        return f"{abs_num/1_000:.1f}K"
    else:
        return f"{abs_num:.2f}"
    


def chartAndTokenDetail():
    st.divider()
    chartFrame,Info = st.columns([0.8,0.2])
    with chartFrame:
        components.iframe(
            src=f"https://www.geckoterminal.com/{network_id}/pools/{pool}?embed=1&info=0&swaps=0&grayscale=0&light_chart=0&chart_type=price&resolution=15m",
            height=450,  # Adjust height as needed
            scrolling=True,
            width=950
        )

    with Info:
        with st.container(height=450):
            with st.container():
                if 'image_url' in st.session_state:
                    image_url = st.session_state.image_url
                    print(image_url)
                    st.markdown(
                        f"""
                        <img src="{image_url}" style ="width:300px;height:100px;">
                        """,
                        unsafe_allow_html=True
                    )            
            
            "--------------------------------------"
            if 'price' in st.session_state:
                price = round(float(st.session_state.price),7)
                price = "{:.13f}".format(price).rstrip("0") 
                st.markdown(
                    f"""
                    <div style='background-color: #e1f3fb; padding: 1px; border-radius: 3px; text-align: center; color: #333;'>
                        ${price}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown('<br>',unsafe_allow_html=True) 

            col = st.columns(3)
            intervals= ['m5','h6','h24']
            price_changes = {
                'm5':st.session_state['m5'],
                'h6':st.session_state['h6'],
                'h24':st.session_state['h24']
            }
            for i in range(0,3):
                with col[i]:
                    with st.container():
                        st.markdown(
                            f"""
                            <style>
                            .label {{ color: olive; font-weight: bold; }}
                            .value {{ color: green; }}
                            </style>
                            <div>
                                <span class="label">{intervals[i]}</span><br>
                            <span class="value">{price_changes[intervals[i]]}%</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                            )

            metric= ['volume','liquidity','holders']
            metric_tag = {
                'volume': "$" + format_number(st.session_state['volume']),
                'liquidity':"$" + format_number(st.session_state['liquidity']),
                'holders':format_number(st.session_state['holders'])
            }
            for i in range(0,3):
                with col[i]:
                    with st.container():
                        st.markdown(
                            f"""
                            <style>
                            .label {{ color: olive; font-weight: bold; }}
                            .value {{ color: green; }}
                            </style>
                            <div>
                                <span class="label">{metric[i]}</span><br>
                            <span class="value">{metric_tag[metric[i]]}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                            )

pageInfo.fetchAll()
chartAndTokenDetail()


def calculate_age(date_time):
    current_date = datetime.now(timezone.utc)
    creation_date = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    delta = current_date - creation_date

    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds_remain = seconds % 60
    months_approx = days / 30.42

    total_hours = days * 24 + hours
    total_minutes = total_hours * 60 + minutes
    total_seconds = total_minutes * 60 + seconds_remain

    if  total_seconds < 60:
        seconds = f'{round(seconds)}s'
        return seconds
    elif total_minutes < 60:
        minutes = f'{round(total_minutes)}m'
        return minutes
    elif total_hours <= 23:
        hours = f'{round(total_hours)}Hr(s)'
        return hours
    elif days <= 29:
        days = f'{round(days)}d'
        return days
    elif months_approx <= 12:
        months = f'{round(months_approx)}months'
        return months
    
    elif days>= 365:
        year = f'{round(days/365)}yr'
        return year


async def showTrades(pool_trades):
    for pool_trade in pool_trades:
        trade = [trade for trade in pool_trade.values()]
        column_needed = st.columns(6)
        for index,column in enumerate(column_needed):
            with column:
                if trade[1] == 'sell':
                    st.markdown(
                        f"""
                    <div style='background-color: #e1f3fb: padding: 1px; border-radius: 5px; text-align: center; color: #ff0000;border: 0.1px solid #a9a9a9'>
                        {str(trade[index])}
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                    <div style='background-color: #e1f3fb: padding: 1px; border-radius: 5px; text-align: center; color: #00ff00;border: 0.1px solid #a9a9a9'>
                        {str(trade[index])}
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                # if trade[1] == 'sell':
                #     st.badge(str(trade[index]),color='red')
                # else:
                #     st.badge(str(trade[index]),color='green')
    await asyncio.sleep(60*3)
    st.rerun()



async def poolTrades():
    
    url = f'https://api.geckoterminal.com/api/v2/networks/{network_id}/pools/{pool}/trades?token=base'

    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # response = await reponse.get(url)
                result = await  response.json()
                pool_datas = result['data']
                pool_trades = []
                for  trade in pool_datas:
                    if len(pool_trades) >= 20:
                        break
                    pool_trade = {}
                    pool_trade['time'] = calculate_age(trade['attributes']['block_timestamp'])
                    pool_trade['trade_direction'] = trade['attributes']['kind']
                    pool_trade['volume'] = round(float(trade['attributes']['volume_in_usd']),3)
                    pool_trade['to_token_amount'] =  round(float(trade['attributes']['to_token_amount']),5)
                    pool_trade['from_token_amount'] =  round(float(trade['attributes']['from_token_amount']),5)
                    pool_trade['price'] =  round(float(trade['attributes']['price_to_in_usd']),6)
                    # pool_trade['trader'] = trade['attributes']['tx_from_address']
                    # pool_trade['hash'] = trade['attributes']['tx_hash']
                    pool_trades.append(pool_trade)
                await showTrades(pool_trades)
        

async def tradeSection():
    st.markdown(
        """
        <div style='background-color: #2F4F4F; padding: 2px; border-radius: 5px; position: relative; height: 40px;'>
            <span style='position: absolute; left: 40px; top: 10px; color: #ffffff;'>Time</span>
            <span style='position: absolute; left: 170px; top: 10px; color: #ffffff;'>Type</span>
            <span style='position: absolute; left: 280px; top: 10px; color: #ffffff;'>Volume</span>
            <span style='position: absolute; left: 350px; top: 10px; color: #ffffff;'>Base Token</span>
            <span style='position: absolute; left: 490px; top: 10px; color: #ffffff;'>Qoute Token</span>
            <span style='position: absolute; left: 620px; top: 10px; color: #ffffff;'>Price</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    with st.container(height=600):
        column_needed = st.columns(6)
        display_info =['Date','Type','Volume (Usd)','Base Token','Qoute Token','Price']

       
        # for index, display_column in enumerate(column_needed):
        #     with display_column :
        #         with st.container():
        #             st.badge(display_info[index])

        await poolTrades()
    

async def displayPool():
    with st.container(height=400):
        pairedToken  = st.session_state.pairedToken
        st.markdown(
            f"""
            <div style='background-color: #e1f3fb; padding: 1px; border-radius: 3px; text-align: center; color: #333;'>
                {pairedToken}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<br>',unsafe_allow_html=True)
        col = st.columns([0.45,0.35,0.2])

        fdv = '$' + format_number(st.session_state['fdv'])
        market_cap = '$' + format_number(st.session_state['market_cap'])
        liquidity = '$'+ format_number(st.session_state['liquidity'])
        volume = '$'+ format_number(st.session_state['volume'])
        supply = format_number(st.session_state['supply'])
        pool_created = calculate_age(st.session_state['poolCreated'])
        address = st.session_state['token_address']
        tokensymbol = st.session_state['tokenSymbol']
        qoute_address = st.session_state['qoute_address'] 
        qoute_symbol = st.session_state['qoute_symbol']
        # st.session_state['supply'] = supply
        #         st.session_state['price'] = price
        #         st.session_state['volume'] = volume_24
        #         st.session_state['market_cap'] = market_cap
        #         st.session_state['fdv'] = fdv
        #         st.session_state['liquidity'] = liquidity
        #         st.session_state['image_url'] = image_url
        metrics_name = ['FDV','SUPPLY','LIQ','MARKETCAP','AGE','VOL']
        metric = {'FDV': fdv,
                  'SUPPLY':supply,
                  'LIQ':liquidity,
                  'VOL':volume,
                  'MARKETCAP':market_cap,
                  'AGE':pool_created
                  }
        displayed = 0
        for i in range(0,3):
            with col[i]:
                st.markdown(
                    f"""
                    <div  padding: 1px; border-radius:0.5px; text-align: center; color: #333;'>
                        {metrics_name[displayed]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div style='background-color: #e1f3fb;  padding: 1px; border-radius:0.5px; text-align: center; color: #333;'>
                        {metric[metrics_name[displayed]]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                displayed +=1
                st.markdown('<br>',unsafe_allow_html=True) 


        for i in range(0,3):
            with col[i]:
                st.markdown(
                    f"""
                    <div  padding: 1px; border-radius:0.5px; text-align: center; color: #333;'>
                        {metrics_name[displayed]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div style='background-color: #e1f3fb;  padding: 1px; border-radius:0.5px; text-align: center; color: #333;'>
                        {metric[metrics_name[displayed]]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                displayed +=1 
                st.markdown('<br>',unsafe_allow_html=True) 

        
        tokenInfo = ['Pair',tokensymbol.upper(),qoute_symbol.upper()]
        details = {
            'Pair':st.session_state['pool'],
            tokensymbol.upper():address,
            qoute_symbol.upper():qoute_address,
        }
        col = st.columns([0.6,0.4])
        for i in range(0,3):
            with col[0]:
                html = f"""
                <div style='background-color: #e1f3fb;  padding: 1px; border-radius:0.5px; text-align: center; color: #333;'>
                {tokenInfo[i]}
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
                st.markdown('<br>',unsafe_allow_html=True) 

            with col[1]:
                html_code = f"""
                <div padding: 1px; border-radius:0.5px>
                <button onclick="copyToClipboard('{details[tokenInfo[i]]}')">Copy Address</button>
                <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(
                        () => alert('Copied to clipboard!'),
                        (err) => alert('Failed to copy: ' + err)
                    );
                }}
                </script>
                </div>
                """
                st.markdown(html_code, unsafe_allow_html=True)
                st.markdown('<br>',unsafe_allow_html=True) 

    

message = """
High risk! Do your own research.Not financial advice! Trade with caution.Verify contract! Beware of scams.Volatile asset! Invest at own risk. "DYOR! No guarantee of profits."
"""  
async def disclaimer():
   with st.container(height=205):
        st.write(message)
        


async def main():
    col1,col2 = st.columns([0.7,0.3])
    with col1:
        task = asyncio.create_task(tradeSection())
        
    with col2:
        task2 = asyncio.create_task(displayPool())
        task3 = asyncio.create_task(disclaimer())
    await task
    await task2
    await task3

asyncio.run(main())