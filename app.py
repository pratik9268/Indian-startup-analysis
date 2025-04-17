import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_investor_detail(investor):
    st.title(investor)
    last_5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5_df)

    col1, col2 = st.columns(2)
    with col1:
        biggest_investment = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index, biggest_investment.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Investment in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Investment in Rounds')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Investment in Citys')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on year Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)


def show_overall_analysis():
    st.title('Overall Analysis')

    total = round(df['amount'].sum())
    st.metric('Total Invested Amount', str(total) + 'Cr')

    col1, col2 = st.columns(2)
    with col1:
        max_raise = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum Raised Invested Amount', str(max_raise) + 'Cr')
    with col2:
        max_raise = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).index[0]
        st.metric('By', str(max_raise))

    avg = round(df.groupby('startup')['amount'].sum().mean())
    st.metric('Avg Funding Amount', str(avg) + 'Cr')

    total_funded_startup = round(df['startup'].nunique())
    st.metric('Total Funded Startup', str(total_funded_startup))


# New function added here
def load_startup_detail(startup):
    st.title(startup)
    st.subheader('Startup Details')

    startup_df = df[df['startup'] == startup]

    st.write('### Recent Funding')
    st.dataframe(startup_df[['date', 'investors', 'vertical', 'city', 'round', 'amount']].sort_values(by='date', ascending=False))

    st.write('### Total Funding')
    total_funding = startup_df['amount'].sum()
    st.metric('Total Funding Amount', f'{total_funding} Cr')

    st.write('### Number of Funding Rounds')
    st.metric('Funding Rounds', startup_df.shape[0])

    round_series = startup_df.groupby('round')['amount'].sum()
    if not round_series.empty:
        st.write('### Round Wise Investment')
        fig, ax = plt.subplots()
        ax.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('show overall analysis')
    if btn0:
        show_overall_analysis()

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_detail(selected_startup)

else:
    selected_invester = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    st.title('Investor Analysis')
    if btn2:
        load_investor_detail(selected_invester)
