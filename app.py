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
st.set_page_config(
    page_title="App_Page",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state='auto',
    menu_items={
        'Get Help':None, #'https://www.extremelycoolapp.com/help',
        'Report a bug': None,# "https://www.extremelycoolapp.com/bug",
        'About': None #" This is a header. This is an *extremely* cool app!"
    }
)
st.markdown(
    """
     <div style='background: linear-gradient(90deg, #1E3A8A, #3B82F6); padding: 15px; margin-top: -10px; border-radius: 8px; box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15); text-align: center; position: relative;'>
        <h1 style='color: #E0FFFF; font-size: 28px; font-weight: bold; margin: 0; text-transform: uppercase; letter-spacing: 1.5px;'>
            🚀 TokenVision: Unleash the Power of Crypto Insights
        </h1>
        <p style='color: #A5B4FC; font-size: 14px; margin-top: 3px;'>
            Explore Real-Time Market Data & Conquer the Blockchain
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


gecko_url = 'https://api.geckoterminal.com/api/v2/'

response =  requests.get(gecko_url + 'networks')
if response.status_code == 200:
    result = response.json()
    data = result['data']
    networks = { }
    for network in data:
        networks[network['attributes']['name']] = network['id']




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
        #'''------------------------------------------------------------------------------------------------'''
        column_needed=  st.columns([1,6])
        pool_name = re.sub(r'\s*\d+(\.\d+)?%\s*', '', pool_info[0])
        pool_name = pool_name.lower().strip()
        if len(pool_name) > 15:
            names = pool_name.split('/')
            pool_name = names[0]+'/'+ names[1]
            if len(pool_name)> 15:
                pool_name = names[0]

        with column_needed[0]: #4CAF50  2F4F4F 3498DB 

            st.markdown(
                """
                <style>
                    div[data-testid="stButton"] > button {
                        margin-top: 8px;  /* Aligns button vertically with the Markdown div */
                        background-color: #3498DB;  /* Matches your button style */
                        color: white;
                        border: none;
                        font-weight: 7000;
                        padding: 5px 10px;
                        border-radius: 3px;
                        cursor: pointer;
                        height: 40px;  /* Match the div height */
                        line-height: 30px;  /* Center text vertically */
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 150px;  /* Set button width */
                    }
                    div[data-testid="stButton"] {
                        margin: 0;  /* Remove container margins */
                        padding: 0;  /* Remove container padding */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )
            if st.button(pool_name, key=vary_button_key):
        #     if st.button(pool_name,key=f'{vary_button_key}'):
                st.session_state.pool = pool_data['pair']
                st.session_state['network_id'] = network_id
                st.switch_page('tokenInfo.py')
        
        price = round(float(pool_info[1]),7)
        price = "{:.10f}".format(price).rstrip("0")
        age = calculate_age(pool_info[2])
        # fdv = int(float(pool_info[3])) 
        fdv = format_number(int(float(pool_info[3])))
        changes =  pool_info[4]
        vary_button_key += 1

        with column_needed[1]:
            st.markdown(
            f"""
            <div style='background-color: #2F4F4F; padding: 2px;margin-top: 25px;border-radius: 5px; position: relative; height: 40px;'>
                <span style='position: absolute; left: 80px;font-weight: bold; top: 10px; color: #00FFFF;'>{price}</span>
                <span style='position: absolute; left: 330px;font-weight: bold; top: 10px; color: #FFD700;'>{age}</span>
                <span style='position: absolute; left: 550px;font-weight: bold; top: 10px; color: white;'>{fdv}</span>
                <span style='position: absolute; left: 750px;font-weight: bold; top: 10px; color: #FF00FF;'>{changes} </span>
            </div>
            """,
            unsafe_allow_html=True # FF00FF
            )


        # for index, column in enumerate(column_needed):
        #     with column :
        #         vary_button_key+=1 # for creating unique button
        #         if index == 0 : 
        #             pool_name = re.sub(r'\s*\d+(\.\d+)?%\s*', '', pool_info[index])
        #             pool_name = pool_name.lower().strip()
        #             if st.button(pool_name,key=f'{vary_button_key}'):
        #                 # st.session_state['pool'] = pool_info[5]
        #                 st.session_state.pool = pool_data['pair']
        #                 st.session_state['network_id'] = network_id
        #                 st.switch_page('tokenInfo.py')  # ":blue[Go to Page 1]
        #                 # st.page_link('tokenInfo.py',label=f':orange[{pool_name}]',icon="🔥")
                        
                       
        #             # st.toast('this is love')
        #         elif index == 1:
        #             price = round(float(pool_info[index]),7)
        #             price = "{:.13f}".format(price).rstrip("0") 
        #             st.page_link('tokenInfo.py',label=f':green[{price}]')
        #             # st.session_state['pool'] = pool_info[5]
        #             st.session_state.pool = pool_data['pair']
        #             st.session_state['network_id'] = network_id
        #         elif index == 2:
        #             age = calculate_age(pool_info[index])
        #             st.page_link('tokenInfo.py',label=f':rainbow[{age}]')
        #             st.session_state['pool'] = pool_info[5]
        #             st.session_state['network_id'] = network_id
        #         elif index == 3:
        #             fdv = int(float(pool_info[index]))
        #             st.page_link('tokenInfo.py',label=f':violet[{fdv:,}]')
        #             st.session_state['pool'] = pool_info[5]
        #             st.session_state['network_id'] = network_id
        #         else:
        #             st.page_link('tokenInfo.py',label=f':gray[{pool_info[index]}]')
        #             st.session_state['pool'] = pool_info[5]
        #             st.session_state['network_id'] = network_id
        # # st.divider()
       
       
    
        

def page_show(network,network_id):
    column_needed=  st.columns(5)
    display_info =['Pool','Price (USD)','Age','FDV (USD)','24H Change']
   
    # for index, display_column in enumerate(column_needed):
    #     with display_column :
    #         with st.container():
    #             st.badge(display_info[index])
    
    st.markdown(
            f"""
            <div style='background-color: #2F4F4F; padding: 2px;margin-top: 25px;border-radius: 5px; position: relative; height: 40px;'>
                <span style='position: absolute; left: 45px;font-weight: bold; top: 10px; color: #3498DB;'>Pool</span>
                <span style='position: absolute; left: 240px;font-weight: bold; top: 10px; color: #00FFFF;'>Price(USD)</span>
                <span style='position: absolute; left: 500px;font-weight: bold; top: 10px; color: #FFD700;'>Age</span>
                <span style='position: absolute; left: 700px;font-weight: bold; top: 10px; color: white;'>FDV (USD) </span>
                <span style='position: absolute; left: 900px;font-weight: bold; top: 10px; color: #FF00FF;'>24H Change </span>
            </div>
            """,
            unsafe_allow_html=True # FF00FF
        )
    
    # st.stop()

    poolState(network_id)
    

pages = [st.Page(page= lambda name=network_name,id=network_id : page_show(name,id), title= network_name,url_path=network_name.lower(),icon=':material/star_half:') for network_name , network_id in networks.items() ]
pages.append(st.Page('tokenInfo.py',url_path='tokenInfo'))
navi = st.navigation(pages)
navi.run()




