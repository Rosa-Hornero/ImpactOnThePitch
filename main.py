import json
import time

import streamlit as st
from streamlit_lottie import st_lottie

from utils.enums import TabsEnums

# Page configuration
st.set_page_config(page_title='ImpactOnThePitch', layout='wide')

# Run once flag
if 'run_once' not in st.session_state:
    st.session_state.run_once = True
    st.session_state.selected_tab_id = TabsEnums.SUMMARY.value


# Display the logo animation at the start of the app
if st.session_state.run_once:
    logo_holder = st.empty()

    with logo_holder.container():
        lottie_path = 'static/soccer.json'
        lottie_json = json.load(open(lottie_path))

        col1, col2, col3 = st.columns([1,3,1])
        with col1:
            st.write(' ')
        with col2:
            st_lottie(lottie_json, key='user', loop=False)
        with col3:
            st.write(' ')

        time.sleep(2)

    logo_holder.empty()
    st.session_state.run_once = False

# Navigation pages definition
views = {
    'Resources': [
        st.Page('views/dashboard.py', title='ImpactOnThePitch', icon='⚽', default=True),
    ],
}

# Start the navigation
pg = st.navigation(views, expanded=True)
pg.run()