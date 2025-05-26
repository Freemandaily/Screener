import asyncio,aiohttp
import time
import streamlit as st
import requests
from datetime import datetime,timezone
import  streamlit.components.v1 as components
from extract import infopage 

import streamlit as st

st.set_page_config(
    page_title="TokenInfo",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state='auto',
    menu_items={
        'Get Help':None, #'https://www.extremelycoolapp.com/help',
        'Report a bug': None,# "https://www.extremelycoolapp.com/bug",
        'About': None #" This is a header. This is an *extremely* cool app!"
    }
)


if 'pool' in st.session_state:
    pool = st.session_state['pool']
    network_id = st.session_state['network_id']
    # st.session_state.pool
    # st.session_state.network_id
else:
    # pool = '2VzfCX2SFeXL6RhE941SNYRhaEtUt4PectubG8wrdtEa'
    # network_id = 'solana'
    pass

pageInfo = infopage()

def chartAndTokenDetail():
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
        
            if 'image_url' in st.session_state:
                image_url = st.session_state.image_url
                st.markdown(
                    f"""
                    <img src="{image_url}" style ="width:300px;height:100px;">
                    """,
                    unsafe_allow_html=True
                )            
            
            """---------------------------------------------------------------"""
            if 'price' in st.session_state:
                pairedToken  = st.session_state.pairedToken
                price = round(float(st.session_state.price),7)
                st.markdown(
                    f"""
                    <style>
                    .label {{ color: olive; font-weight: bold; }}
                    .value {{ color: green; }}
                    </style>
                    <div>
                        <span class="label">Pair:</span> <span class="value">{pairedToken}</span><br>
                        <span class="label">Price:</span> <span class="value">${price:.5f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            """---------------------------------------------------------------"""
            fiveminute,six_hours,twenty_four_hours = st.columns(3)
            with fiveminute:
                with st.container():
                    m5 = st.session_state['m5'] 
                    st.markdown(
                    f"""
                    <style>
                    .label {{ color: olive; font-weight: bold; }}
                    .value {{ color: green; }}
                    </style>
                    <div>
                        <span class="label">5M</span><br>
                       <span class="value">{m5}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with six_hours:
                with st.container():
                    h6 = st.session_state['h6'] 
                    st.markdown(
                    f"""
                    <style>
                    .label {{ color: olive; font-weight: bold; }}
                    .value {{ color: green; }}
                    </style>
                    <div>
                        <span class="label">6H</span><br>
                       <span class="value">{h6}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with twenty_four_hours:
                h24 = st.session_state['h24'] 
                st.markdown(
                f"""
                <style>
                .label {{ color: gray; font-weight: bold; }}
                .value {{ color: green; }}
                </style>
                <div>
                    <span class="label">24H</span><br>
                    <span class="value">{h24}%</span>
                </div>
                """,
                unsafe_allow_html=True
                )
            
            volume,liquidity,holders = st.columns(3)
            with volume:
                with st.container():
                    volume = st.session_state['volume'] 
                    st.markdown(
                    f"""
                    <style>
                    .label {{ color: olive; font-weight: bold; }}
                    .value {{ color: green; }}
                    </style>
                    <div>
                        <span class="label">VOL</span><br>
                       <span class="value">{volume}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with liquidity:
                with st.container():
                    liquidity = st.session_state['liquidity'] 
                    st.markdown(
                    f"""
                    <style>
                    .label {{ color: olive; font-weight: bold; }}
                    .value {{ color: green; }}
                    </style>
                    <div>
                        <span class="label">Liq</span><br>
                       <span class="value">{liquidity}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with holders:
                holders = st.session_state['holders']

                st.markdown(
                f"""
                <style>
                .label {{ color: gray; font-weight: bold; }}
                .value {{ color: green; }}
                </style>
                <div>
                    <span class="label">Holders</span><br>
                    <span class="value">{holders}%</span>
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
                    st.badge(str(trade[index]),color='red')
                else:
                    st.badge(str(trade[index]),color='green')
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
                    if len(pool_trades) >= 15:
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

    with st.container(height=500):
        column_needed = st.columns(6)
        display_info =['Date','Type','Volume (Usd)','Base Token','Qoute Token','Price']

        for index, display_column in enumerate(column_needed):
            with display_column :
                with st.container():
                    st.badge(display_info[index])

        await poolTrades()
    

async def displayPool():
    with st.container(height=350):
        st.write('Update Pool Info here')


async def main():
    col1,col2 = st.columns([0.7,0.3])
    with col1:
        task = asyncio.create_task(tradeSection())
        
    with col2:
        task2 = asyncio.create_task(displayPool())

    await task
    await task2

asyncio.run(main())
