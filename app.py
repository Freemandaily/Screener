import re
import aiohttp
import streamlit as st
import _asyncio
import requests
from datetime import datetime,timezone
from extract import networkPool

def divider():
    st.divider()
# st.session_state.clear()


gecko_url = 'https://api.geckoterminal.com/api/v2/'

response =  requests.get(gecko_url + 'networks')
if response.status_code == 200:
    result = response.json()
    data = result['data']
    networks = { }
    for network in data:
        networks[network['attributes']['name']] = network['id']


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



def poolState(network_id ):
    pool_state = networkPool({network_id})
    pools_datas = pool_state.fetch_pools(f'/{network_id}/pools?page=5')
    vary_button_key = 0 

    for pool_data in pools_datas: # for pool name in list of pools
        pool_info = [info for info in pool_data.values()]
        # st.divider()
        '''------------------------------------------------------------------------------------------------'''
        column_needed=  st.columns(5)
        for index, column in enumerate(column_needed):
            with column :
                vary_button_key+=1 # for creating unique button
                if index == 0 : 
                    pool_name = re.sub(r'\s*\d+(\.\d+)?%\s*', '', pool_info[index])
                    pool_name = pool_name.lower().strip()
                    if st.button(pool_name,key=f'{vary_button_key}'):
                        # st.session_state['pool'] = pool_info[5]
                        st.session_state.pool = pool_data['pair']
                        st.session_state['network_id'] = network_id
                        st.switch_page('tokenInfo.py')  # ":blue[Go to Page 1]
                        # st.page_link('tokenInfo.py',label=f':orange[{pool_name}]',icon="🔥")
                        
                       
                    # st.toast('this is love')
                elif index == 1:
                    price = round(float(pool_info[index]),5)
                    st.page_link('tokenInfo.py',label=f':green[{price:,}]')
                    # st.session_state['pool'] = pool_info[5]
                    st.session_state.pool = pool_data['pair']
                    st.session_state['network_id'] = network_id
                elif index == 2:
                    age = calculate_age(pool_info[index])
                    st.page_link('tokenInfo.py',label=f':rainbow[{age}]')
                    st.session_state['pool'] = pool_info[5]
                    st.session_state['network_id'] = network_id
                elif index == 3:
                    fdv = int(float(pool_info[index]))
                    st.page_link('tokenInfo.py',label=f':violet[{fdv:,}]')
                    st.session_state['pool'] = pool_info[5]
                    st.session_state['network_id'] = network_id
                else:
                    st.page_link('tokenInfo.py',label=f':gray[{pool_info[index]}]')
                    st.session_state['pool'] = pool_info[5]
                    st.session_state['network_id'] = network_id
        # st.divider()
       
       
    
        

def page_show(network,network_id):
    column_needed=  st.columns(5)
    display_info =['Pool','Price (USD)','Age','FDV (USD)','24H Change']
   
    for index, display_column in enumerate(column_needed):
        with display_column :
            with st.container():
                st.badge(display_info[index])
    # st.stop()

    poolState(network_id)
    

pages = [st.Page(page= lambda name=network_name,id=network_id : page_show(name,id), title= network_name,url_path=network_name.lower(),icon=':material/star_half:') for network_name , network_id in networks.items() ]
pages.append(st.Page('tokenInfo.py',url_path='tokenInfo'))
navi = st.navigation(pages)
navi.run()




