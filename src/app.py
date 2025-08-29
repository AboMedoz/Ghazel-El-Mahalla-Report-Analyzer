import base64
import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from main import PlotDataFrame


@st.cache_data
def get_plot(local_df, name, label):
    local_plotter = PlotDataFrame(local_df, name)
    return local_plotter.plot_label(label)


st.header("""
    Factory Reports
""")
st.write("Upload File to start Analyzing")

report = st.file_uploader(type='csv', label='report', label_visibility='hidden')
if report:
    file_name = report.name.split('.')[0]

    df = pd.read_csv(report)
    df = df.fillna(0)

    plotter = PlotDataFrame(df, file_name)

    st.sidebar.header("Plot Type")
    plot = st.sidebar.selectbox(label='x Axis', options=['Production', 'Efficiency', 'Availability'],
                                label_visibility='hidden')

    buf = io.BytesIO()
    fig = get_plot(df, file_name, plot)
    fig.savefig(buf, format='png', dpi=200, bbox_inches='tight')
    buf.seek(0)

    b64 = base64.b64encode(buf.read()).decode()
    html = f"""
    <a href="data:image/png;base64,{b64}" target="_blank">
        <img src="data:image/png;base64,{b64}" style="max-width:100%; height:auto;"/>
    </a>
    """

    st.markdown(html, unsafe_allow_html=True)
    # st.pyplot(fig, use_container_width=True)
    st.download_button(label='Download Plot', data=buf, file_name=f'{plot}_Report.png', mime='image/png')
