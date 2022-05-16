import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests

import plotly.express as px
from streamlit_lottie import st_lottie

from plotly.subplots import make_subplots
import plotly.graph_objects as go

from PIL import Image

# ---- PAGE TITLE ----
st.set_page_config(page_title="Euroleague stats", page_icon= ':basketball:', layout="wide")
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

# ---- HEADER SECTION ----
st.title('Euroleague Player Stats Explorer :basketball: ')

st.markdown("""
This app is created by **Elesa Marounta** and performs simple webscraping of Euroleague player stats data for season 2021-2022!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [basketball.realgm.com](https://basketball.realgm.com/international/league/1/Euroleague/stats/2022/Averages/Qualified/All/points/All/desc/1).
""")


# Web scraping of Eurolague player stats
data1= pd.read_html('https://basketball.realgm.com/international/league/1/Euroleague/stats/2022/Averages/Qualified/All/points/All/desc/1',header=0)

#data1[0]
data2= pd.read_html('https://basketball.realgm.com/international/league/1/Euroleague/stats/2022/Averages/Qualified/All/points/All/desc/2',header=0)

#data2[0]
data3= pd.read_html('https://basketball.realgm.com/international/league/1/Euroleague/stats/2022/Averages/Qualified/All/points/All/desc/3',header=0)

#data3[0]

frames = [data1[0], data2[0], data3[0]]
result = pd.concat(frames)

#result.drop(columns=['Unnamed: 0','#'],inplace=True)

result


# Sidebar - Team selection
sorted_unique_team = sorted(result.Team.unique())
selected_team = st.sidebar.multiselect('Select Team', sorted_unique_team, sorted_unique_team)

# sidebar Image
#st.sidebar.image("https://www.insider.gr/sites/default/files/styles/schema_cover_1_1/public/2021-10/shutterstock%20Euroleague%202021.jpg?itok=3C4wvQrQ", use_column_width=True)
st.sidebar.image('https://lpbasketball.gr/wp-content/uploads/2021/09/euroleague-teams-web.jpg')
st.sidebar.image('https://sportklub.rs/wp-content/uploads/2020/05/lopta-evroliga-180701-750x501.jpeg')



# Filtering data
df_selected_team = result[(result.Team.isin(selected_team))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)



# Download Euroleague player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(result):
    csv = result.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="euroleague21-22.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)


st.write('---')
st.write('## Visualizations of the players statistics :bar_chart: ##')




# TOP SCORERS [BAR CHART]
ppg=result.sort_values(by='PPG', ascending=False)
fig1=px.bar(ppg[:15], y='Player', x='PPG', title='Top scorers this season')
st.plotly_chart(fig1)

# ASSIST LEADERS
assists=result.groupby('Player')['APG'].sum().sort_values(ascending=False).reset_index()
fig=px.bar(assists[:15], y='APG', x='Player', title='Leaders in average assists per game',orientation='v')
fig.update_traces(marker_color='#00CC96')
st.plotly_chart(fig)

# Turnovers
tov_player=result.sort_values(by='TOV', ascending=False)
fig2=px.bar(tov_player[:15], x='Player', y='TOV', title='Players with most turnovers', orientation='v')
fig2.update_traces(marker_color='#FFA15A')
st.plotly_chart(fig2)

# Most minutes played
mpg=result.sort_values(by='MPG',ascending=False)
figg=px.bar(mpg[:15], x='Player', y='MPG', title='Players with most average minutes played per game',template = 'plotly_dark')
st.plotly_chart(figg)

# rebounds per game (offensive + defensive)
rpg=result.sort_values(by='RPG',ascending=False)
fig0=px.bar(rpg[:15], y='RPG', x='Player', title='Top rebounders per game(offensive+deffensive)')
st.plotly_chart(fig0)

# offensive rebounds
orb=result.sort_values(by='ORB',ascending=False)

# defensive rebounds
drb=result.sort_values(by='DRB',ascending=False)


fig3 = make_subplots(rows = 1, cols = 2,
                    subplot_titles=['Defensive RB', 'Offensive RB'],
                   horizontal_spacing=0.1)
trace0 = go.Bar(x = drb['DRB'][:15], y = drb['Player'][:15], name = 'DefRB',
               orientation = 'h', text = drb['DRB'], textposition='inside',texttemplate='%{text:.2f}')
fig3.add_trace(trace0, row = 1, col = 1)
trace1 = go.Bar(x = orb['ORB'][:15], y = orb['Player'][:15], name = 'OffRB',
               orientation = 'h', text = orb['ORB'], textposition='inside',texttemplate='%{text:.2f}')
fig3.add_trace(trace1, row = 1, col = 2)
fig3.update_layout(showlegend = False)
st.plotly_chart(fig3)

# Three pointers
threes_made=result.sort_values(by='3PM', ascending=False)
fig14=px.bar(threes_made[:15], y='3PM', x='Player', title='Top 3-pts scorers per game', template ='ggplot2', orientation='v')
st.plotly_chart(fig14)

# 3pts attempted and threes_made
threes_attempt=result.sort_values(by='3PA', ascending=False)

fig4 = make_subplots(rows = 1, cols = 2,
                    subplot_titles=['3pts made per game', '3pts attempted per game'],
                   horizontal_spacing=0.1)
trace2 = go.Bar(x = threes_made['3PM'][:15], y = threes_made['Player'][:15], name = '3 pts made',
               orientation = 'h', text = threes_made['3PM'], textposition='inside',texttemplate='%{text:.2f}')
fig4.add_trace(trace2, row = 1, col = 1)
trace3 = go.Bar(x = threes_attempt['3PA'][:15], y = threes_attempt['Player'][:15], name = '3 pts attempted',
               orientation = 'h', text = threes_attempt['3PA'], textposition='inside',texttemplate='%{text:.2f}')
fig4.add_trace(trace3, row = 1, col = 2)
fig4.update_layout(showlegend = False)
st.plotly_chart(fig4)


# steals and blocks
spg_player=result.sort_values(by='SPG', ascending=False)
st.plotly_chart(px.bar(spg_player[:15], x='Player', y='SPG', title='Top stealers per game', orientation='v'))

bpg_player=result.sort_values(by='BPG', ascending=False)
st.plotly_chart(px.bar(bpg_player[:15], x='Player', y='BPG', title='Top blockers per game', orientation='v'))

# Free throws
fta=result.sort_values(by='FTA',ascending=False)
ftm=result.sort_values(by='FTM',ascending=False)
fig6 = make_subplots(rows = 1, cols = 2,
                    subplot_titles=['free throws made per game', 'free throws attempted per game'],
                   horizontal_spacing=0.1)
trace5 = go.Bar(x = ftm['FTM'][:15], y = ftm['Player'][:15], name = 'free throws made',
               orientation = 'h', text = ftm['FTM'], textposition='inside',texttemplate='%{text:.2f}')
fig6.add_trace(trace5, row = 1, col = 1)
trace6 = go.Bar(x = fta['FTA'][:15], y = fta['Player'][:15], name = 'free throws attempted',
               orientation = 'h', text = fta['FTA'], textposition='inside',texttemplate='%{text:.2f}')
fig6.add_trace(trace6, row = 1, col = 2)
fig6.update_layout(showlegend = False)
st.plotly_chart(fig6)




# the end

def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

# ---- LOAD ASSETS ----
lottie_bball = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_rEFATf.json")



#--------------------------
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:

        st.write(
            """
            I hope you enjoyed it!



            Keep playing, watching and LOVING basketball!
            """
        )

    with right_column:
        st_lottie(lottie_bball, height=300)
