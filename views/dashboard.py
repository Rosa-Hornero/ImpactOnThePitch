# This project is licensed under the MIT License.
# See the LICENSE file for more details.

from datetime import datetime

import extra_streamlit_components as stx
import streamlit as st

from utils.enums import TabsEnums
from views.tabs import *


### Start of Sidebar content ###
with st.sidebar:
    # Set the title and logo
    st.logo('static/images/Fut_logo.png', size='large')
    st.sidebar.title('ImpactOnThePitch')
    info_message = """<p><strong>Thank You for Visiting InjuryImpact.</strong></p>
<p>😊 We appreciate your <strong>interest</strong> in exploring the <strong>impact of player injuries</strong> on Premier League teams.</p>
<p>🌍 <strong>Stay connected</strong> with us to dive deeper into football analytics and never miss an update!</p>
<p>📱 Follow us on our social media channels for more insights, updates, and exciting football and technology content.</p>"""
    st.markdown(f'<div style="padding: 10px; border-radius: 15px  font-size: 17px;">{info_message}</div>', unsafe_allow_html=True)

    # Set a divider
    st.divider()

    #Apartado RRSS
    st.title("Follow us on our social media")

    # LinkedIn
    st.markdown('''
        <a href="https://www.linkedin.com/in/rosa-hornero/" target="_blank" style="text-decoration:none;">
            💼 LinkedIn
        </a>
    ''', unsafe_allow_html=True)

    # Twitter
    st.markdown('''
        <a href="https://x.com/hornero_rosa" target="_blank" style="text-decoration:none;">
            🐦 Twitter
        </a>
    ''', unsafe_allow_html=True)

#### End of Sidebar content ####

#### Start of Tabs content ####

# Tabs definition
tab_holder = st.empty()
with tab_holder.container():
        stx.tab_bar(
            data=[
                stx.TabBarItemData(id=TabsEnums.SUMMARY.value, title='📊 Information', description=''),
                stx.TabBarItemData(id=TabsEnums.ARSENAL.value, title='💣 Arsenal', description=''),
                stx.TabBarItemData(id=TabsEnums.ASTON.value, title='🦁 Aston Villa', description=''),
                stx.TabBarItemData(id=TabsEnums.BRENTFORD.value, title='🐝 Brentford', description=''),
                stx.TabBarItemData(id=TabsEnums.BURNLEY.value, title='🔥  Burnley', description=''),
                stx.TabBarItemData(id=TabsEnums.EVERTON.value, title='🏰  Everton', description=''),
                stx.TabBarItemData(id=TabsEnums.UNITED.value, title='👹  ManUnited', description=''),
                stx.TabBarItemData(id=TabsEnums.NEWCASTLE.value, title='🪶  Newcastle', description=''),
                stx.TabBarItemData(id=TabsEnums.TOTTENHAM.value, title='𓅥 Tottenham', description=''),
            ],
            key='selected_tab_id',
            default=st.session_state.selected_tab_id
        )

        # Render the selected tab
        if st.session_state.selected_tab_id == TabsEnums.SUMMARY.value:
            render_summary_tab()
        elif st.session_state.selected_tab_id == TabsEnums.ARSENAL.value:
            render_arsenal_tab()
        elif st.session_state.selected_tab_id == TabsEnums.ASTON.value:
            render_aston_villa_tab()
        elif st.session_state.selected_tab_id == TabsEnums.BRENTFORD.value:
            render_bretford_tab()
        elif st.session_state.selected_tab_id == TabsEnums.BURNLEY.value:
            render_burnley_tab()
        elif st.session_state.selected_tab_id == TabsEnums.EVERTON.value:
            render_everton_tab()
        elif st.session_state.selected_tab_id == TabsEnums.NEWCASTLE.value:
            render_newcastle_tab()
        elif st.session_state.selected_tab_id == TabsEnums.TOTTENHAM.value:
            render_tottenham_tab()
        elif st.session_state.selected_tab_id == TabsEnums.UNITED.value:
            render_united_tab()
