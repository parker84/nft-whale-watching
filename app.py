import streamlit as st
import pandas as pd
from datetime import datetime 
from google.cloud import bigquery
bqclient = bigquery.Client()

#------dash setup
st.set_page_config(
    layout='wide', 
    page_icon='🐳',
    page_title='NFT Whale Watching',
    menu_items={
        'Get Help': 'https://join.slack.com/t/nftdata/shared_invite/zt-16j5lbu11-IFytBXStjl67XIwrOW82aA',
        'Report a bug': "https://github.com/parker84/nft-whale-watching/issues/new",
        'About': "This dashboard was initially created by [Brydon Parker](https://linkpop.com/brydon)."
    }
)
st.title("NFT Whale Watching")
st.markdown("This dashboard provides the user with data on the top 1000 ETH wallets.")


#--------helpers
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')
    

#-------data queryers
def get_top_ranked_by_balance(date):
    query = """
    select *
    from `bigquery-public-data.crypto_ethereum.balances`
    order by eth_balance desc
    limit 1000
    """
    df = (
        bqclient.query(query)
        .result()
        .to_dataframe(
            create_bqstorage_client=True,
        )
    )
    df['wallet_address'] = df['address']
    df['ether_balance'] = df['eth_balance'].astype(float) / 1e+18
    return df[['wallet_address', 'ether_balance']]


#-------readme
with st.expander('README', expanded=False):
    st.markdown(
    """
    ### Definitions:
    1. 

    ### Caveats:
    1. Results will be updated once a day

    ### Tips:
    1. You can zoom in on any graph by clicking and dragging a box on the graph where you want to zoom.
    2. For each parameter (ex: Province/Country), if you hover over the "(?)" (top right of parameter) you can see more detailed instructions for that parameter. 
    3. Each section can expand/contract if your click on the +/-.
    3. Have questions/feedback? Join our [slack workspace](https://join.slack.com/t/nftdata/shared_invite/zt-16j5lbu11-IFytBXStjl67XIwrOW82aA)
    """
    )


#-------sidebar setup
st.sidebar.title('🐳 Parameters')
rank_by = st.sidebar.selectbox(
    'Choose Your Ranking Method', 
    ['Wallet Balance', 'Absolute ROI', 'Relative ROI'], 
    help='Use this to decide how the top 1000 🐳 are determined.'
)
st.sidebar.markdown(
    """
    Have questions/feedback? 
    Join our [slack workspace](https://join.slack.com/t/nftdata/shared_invite/zt-16j5lbu11-IFytBXStjl67XIwrOW82aA)
    
    Like this dashboard and want to say thanks?       
    [:coffee: buy me a coffee](https://www.buymeacoffee.com/brydon)
    """
)


if rank_by != 'Wallet Balance':
    email = st.text_input(
        label="Still under construction, add your email below to get notified when it's ready",
        value="your_email@something.com",
        help="Enter your email to get notified when we add in `Absolute ROI` and `Relative ROI` rankings"
    )
    if email != 'your_email@something.com':
        st.text("🚀 Thank You! We will notify you when it's ready 🚀")
else:
    date = datetime.now().date()   
    df = get_top_ranked_by_balance(date)
    st.dataframe(df)
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'nft_whales_ranked_by_{rank_by.lower().replace(" ", "_")}.csv',
        mime='text/csv',
    )