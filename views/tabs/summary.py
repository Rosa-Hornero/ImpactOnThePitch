import streamlit as st

def render_summary_tab():
    #st.header('Información')

    #tab_holder.empty()
    cols = st.columns([1,3,1], vertical_alignment='center')
    cols[0].write('')
    cols[2].write('')
    with cols[1]:
        st.title('⚽ Welcome to Impact On The Pitch')
        st.divider()
        #info_message = "Please <b>follow the next steps</b> before you begin:<br><br>&nbsp;&nbsp;&nbsp;&nbsp;🅰️ <b>Select a participant identifier</b> (<i>participant_id</i>) and <b>session identifier</b> (<i>session_id</i>) from the designated fields in the sidebar on the left.<br>&nbsp;&nbsp;&nbsp;&nbsp;🅱️ If you wish to <b>restart the demo</b> and choose new identifiers, use the <b>‘🔄 Restart & Refresh’</b> button in the sidebar on the left to clear the current selections and start over.<br><br>Once you have selected both identifiers, you will see a <b>detailed analysis divided into <u>5 sections</u></b>:<br><br>&nbsp;&nbsp;&nbsp;&nbsp;1️⃣ <b><i>Summary</i></b> 📊: an overview of the analysis of all tests.<br>&nbsp;&nbsp;&nbsp;&nbsp;2️⃣ <b><i>Touch & Reaction Time</i></b> 👆: measures the child's speed and accuracy in touching a mole using a single finger while it appears at different locations.<br>&nbsp;&nbsp;&nbsp;&nbsp;3️⃣ <b><i>Drag & Drop</i></b> 🥕: evaluates the child's ability to drag and drop an object (a carrot towards a rabbit) using a single finger.<br>&nbsp;&nbsp;&nbsp;&nbsp;4️⃣ <b><i>Zoom In / Zoom Out</i></b> 🐰: analyses the child's ability to enlarge and reduce the size of a rabbit image using the pinch gesture with two fingers.<br>&nbsp;&nbsp;&nbsp;&nbsp;5️⃣ <b><i>Spiral Test</i></b> 🎯: evaluates the child's accuracy in tracing a spiral with a stylus, always trying to keep inside the black line that forms the spiral.<br>&nbsp;&nbsp;&nbsp;&nbsp;6️⃣ <b><i>Drawing Test</i></b> 🌳: analyses the child's ability to colour a tree using the stylus without going outside the contour lines.<br><br>😄 Finally, you can explore the results to obtain valuable information about children's motor and cognitive development!"
        info_message = """
<div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
  <p>Discover how player injuries shape the game in the Premier League.</p>
  
  <p>This platform explores a detailed dataset covering the impact of player absences on team performance across eight clubs—<strong>Arsenal, Aston Villa, Brentford, Burnley, Everton, Manchester United, Newcastle and Tottenham</strong>—between 2019 and 2024. With over <strong>600 injury records</strong>, we reveal how missing players affect match results, team dynamics, and individual performances.</p>
  
  <h2>Data Highlights:</h2>
  <ul>
    <li><strong>Insights on Key Clubs:</strong> Analyze how teams adapt when key players are sidelined.</li>
    <li><strong>Performance Metrics:</strong> Compare pre- and post-injury match ratings and statistics.</li>
    <li><strong>Extensive Sources:</strong>
      <ul>
        <li><strong>Transfer Market:</strong> Injury records and durations.</li>
        <li><strong>Football Critic:</strong> Player ratings for impacted matches.</li>
        <li><strong>Sky Sports:</strong> Supplemental match statistics and performance data.</li>
        <li><strong>Link to dataset: </strong><a href="https://www.kaggle.com/datasets/amritbiswas007/player-injuries-and-team-performance-dataset/data" target="_blank">Player Injuries and Team Performance Dataset</a></li>
      </ul>
    </li>
  </ul>
  
  <p>Use our interactive tools to uncover patterns, trends, and the hidden impact of injuries on the beautiful game.</p>
</div>
"""
        st.markdown(f'<div style= font-size: 17px;">{info_message}</div>', unsafe_allow_html=True)
#### End of Tabs content ####

