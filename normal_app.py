import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# page Configuration
st.set_page_config(
    page_title="Smart Monitor User Dashboard",
    page_icon="🖥",
    layout='wide',
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")


data = pd.read_csv('./file/NL_log30.csv')
maxCount = float(data['Context Name'].value_counts().reset_index()['count'].max())

# sidebar
with st.sidebar :
    st.title('🖥 User Dashboard')

    st.divider()    
    ctxtlist = list(data['Context Name'].unique())
    selectedContext = st.selectbox('Select a Context Name', ctxtlist)
    msgIDlist = list(data[data['Context Name']==selectedContext]['Message ID'].unique())   
    selectedMsgId = st.selectbox('Select a Message ID', msgIDlist)

    st.divider()    
    sliderRange = st.slider("Scale Count value", 0.0, maxCount, (512.0, maxCount))


# Plots
def makeCountPlot(min, max) :
    px_df = data['Context Name'].value_counts().reset_index()
    px_df = px_df[(px_df['count'] >= min) & (px_df['count'] <= max)]
    fig = px.bar(px_df, x='Context Name', y='count')
    tab1.plotly_chart(fig, theme = 'streamlit', use_container_width=True)

def makeDount():
    px_df = data['Context Name'].value_counts().reset_index().sort_values(by='count', ascending=False).iloc[:3, ]
    fig = px.pie(px_df, names='Context Name', values='count', title='Top3 Use modules', hole=.3)

    fig.update_traces(textposition='inside', textinfo='percent + label + value')
    fig.update_layout(font=dict(size=14))
    fig.update(layout_showlegend=False)

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

# Dashboard Main Panel
col = st.columns((3.5, 10.5), gap='medium')

with col[0] :
    st.markdown('### Top3 Module Use')

    ModuleCountData = data['Context Name'].value_counts().reset_index().sort_values(by='count', ascending=False)
    
    for idx in range(0, 3) :
        ModuleName = ModuleCountData['Context Name'].iloc[idx]
        ModuleValue = ModuleCountData['count'].iloc[idx]
        st.metric(label=ModuleName,
                    value=ModuleValue,
                    delta=None)
    

    st.markdown('### Module Percentage')
    makeDount()


with col[1] :
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

    tab1.subheader('Count per Module')
    makeCountPlot(sliderRange[0], sliderRange[1])

    tab2.subheader('Data State')
    tab2.dataframe(data['Context Name'].value_counts().reset_index().sort_values(by='count', ascending=False),
                column_order=("Context Name", "count"),
                hide_index=True,
                width=None,
                column_config={
                    "Context Name" : st.column_config.TextColumn("module"),
                    "count" : st.column_config.ProgressColumn(
                        "usability",
                        format="%f",
                        min_value=0,
                        max_value=maxCount,
                    )
                }
    )

