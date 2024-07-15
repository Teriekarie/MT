
import streamlit as st
import pandas as pd
import altair as alt

# Setting a theme for the dashboard
st.set_page_config(
    page_title="Uber Onboarding Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com',
        'Report a bug': "https://www.example.com",
        'About': "# This is a header. This is an *extremely* cool dashboard!"
    }
)

# Adding a custom theme with CSS for styling
def add_custom_css():
    st.markdown("""
    <style>
        /* Main font for the entire dashboard */
        html, body, [class*="css"] {
            font-family: "Gill Sans", sans-serif;
        }
        /* Main dashboard background color */
        body {
            background-color: #f0f2f5;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #fafafa;
            color: #4f8af4;
        }
        /* Title color */
        h1 {
            color: #ff6347;
        }
        /* Card styling */
        .metric-card {
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 10px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-card.large {
            height: 150px;
            background-color: #4f8af4;
        }
        .metric-card.blue {
            background-color: #1f77b4;
        }
        .metric-card.green {
            background-color: #2ca02c;
        }
        .metric-card.red {
            background-color: #d62728;
        }
        .metric-value {
            font-size: 36px;
            font-weight: bold;
        }
        .metric-label {
            font-size: 18px;
        }
        /* Container for metric cards */
        .metric-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        /* Divider style */
        .divider {
            border-top: 2px solid #4f8af4;
            margin: 40px 0;
        }
    </style>
    """, unsafe_allow_html=True)

add_custom_css()


# Title of the dashboard
st.title('🚗 Uber Onboarding Analysis')

# Load the cleaned dataset
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d', errors='coerce')
    return data

data = load_data('june_data2.csv')

# Sidebar: adding filters for Date Range
def sidebar_filters(data):
    st.sidebar.header('Search Filters')

    # Date filter
    min_date, max_date = data['date'].min().date(), data['date'].max().date()
    start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # City filter
    if 'city' in data.columns:
        city_options = ['All'] + sorted(list(data['city'].unique()))
        selected_city = st.sidebar.multiselect('Select City', options=city_options, default='All')
        if 'All' in selected_city:
            selected_city = city_options[1:]
        filtered_data = filtered_data[filtered_data['city'].isin(selected_city)]

    # Type of partner filter
    if 'type_of_partner' in data.columns:
        data['type_of_partner'] = data['type_of_partner'].fillna('N/A')
        partner_options = ['All'] + sorted(list(data['type_of_partner'].unique()))
        selected_partner = st.sidebar.multiselect('Select Partner', options=partner_options, default='All')
        if 'All' in selected_partner:
            selected_partner = partner_options[1:]
        filtered_data = filtered_data[filtered_data['type_of_partner'].isin(selected_partner)]

    # Onboarder filter
    if 'onboarder' in data.columns:
        data['onboarder'] = data['onboarder'].fillna('N/A')
        onboarder_options = ['All'] + sorted(list(data['onboarder'].unique()))
        selected_onboarder = st.sidebar.multiselect('Select Onboarder', options=onboarder_options, default='All')
        if 'All' in selected_onboarder:
            selected_onboarder = onboarder_options[1:]
        filtered_data = filtered_data[filtered_data['onboarder'].isin(selected_onboarder)]

    # Comment filter
    if 'comment' in data.columns:
        data['comment'] = data['comment'].fillna('N/A')
        comment_options = ['All'] + sorted(list(data['comment'].unique()))
        selected_comment = st.sidebar.multiselect('Select Comment', options=comment_options, default='All')
        if 'All' in selected_comment:
            selected_comment = comment_options[1:]
        filtered_data = filtered_data[filtered_data['comment'].isin(selected_comment)]

    return filtered_data, start_date, end_date

filtered_data, start_date, end_date = sidebar_filters(data)


# Key Metrics calculation
def calculate_metrics(filtered_data):
    metrics = {
        'total_cities': filtered_data['city'].nunique(),
        'total_onboarders': filtered_data['onboarder'].nunique(),
        'total_partners': filtered_data['type_of_partner'].nunique(),
        'total_drivers': filtered_data['names'].nunique(),
        'total_driving': filtered_data[filtered_data['comment'].str.contains('driving', case=False, na=False)]['names'].nunique(),
        'total_not_driving': filtered_data[filtered_data['comment'].str.contains('not driving', case=False, na=False)]['names'].nunique(),
        'total_uploading_docs': filtered_data[filtered_data['comment'].str.contains('uploading docs', case=False, na=False)]['names'].nunique(),
        'total_trip_completed': filtered_data[filtered_data['comment'].str.contains('trip completed', case=False, na=False)]['names'].nunique(),
        'total_rewards_expired': filtered_data[filtered_data['comment'].str.contains('rewards expired', case=False, na=False)]['names'].nunique(),
        'total_payment_stopped': filtered_data[filtered_data['comment'].str.contains('payment stopped', case=False, na=False)]['names'].nunique(),
        'total_invalid': filtered_data[filtered_data['comment'].str.contains('invalid', case=False, na=False)]['names'].nunique()
    }
    return metrics

metrics = calculate_metrics(filtered_data)

# Icons for metrics
icons = {
    "city": "🏙️",
    "onboarder": "🧑‍🏫",
    "partner": "🤝",
    "drivers": "🚗",
    "driving": "🟢",
    "not_driving": "🔴",
    "uploading_docs": "📄",
    "trip_completed": "✅",
    "rewards_expired": "🏅",
    "payment_stopped": "💸",
    "invalid": "❌"
}

# Display key metrics
def display_metrics(metrics, icons):
    st.markdown(f"""
    <div class='metric-container'>
        <div class='metric-card large'>
            <span class='metric-value'>{metrics['total_cities']}</span>
            <span class='metric-label'>{icons['city']} Cities</span>
        </div>
        <div class='metric-card large blue'>
            <span class='metric-value'>{metrics['total_onboarders']}</span>
            <span class='metric-label'>{icons['onboarder']} Onboarders</span>
        </div>
        <div class='metric-card large green'>
            <span class='metric-value'>{metrics['total_partners']}</span>
            <span class='metric-label'>{icons['partner']} Driving Type</span>
        </div>
    </div>
    <div class='divider'></div>
    <div class='metric-container'>
        <div class='metric-card blue'>
            <span class='metric-value'>{metrics['total_drivers']}</span>
            <span class='metric-label'>{icons['drivers']} Registered Drivers</span>
        </div>
        <div class='metric-card green'>
            <span class='metric-value'>{metrics['total_driving']}</span>
            <span class='metric-label'>{icons['driving']} Drivers Driving</span>
        </div>
        <div class='metric-card red'>
            <span class='metric-value'>{metrics['total_not_driving']}</span>
            <span class='metric-label'>{icons['not_driving']} Drivers Not Driving</span>
        </div>
        <div class='metric-card blue'>
            <span class='metric-value'>{metrics['total_uploading_docs']}</span>
            <span class='metric-label'>{icons['uploading_docs']} Uploading Docs</span>
        </div>
        <div class='metric-card green'>
            <span class='metric-value'>{metrics['total_trip_completed']}</span>
            <span class='metric-label'>{icons['trip_completed']} Trip Completed</span>
        </div>
        <div class='metric-card red'>
            <span class='metric-value'>{metrics['total_rewards_expired']}</span>
            <span class='metric-label'>{icons['rewards_expired']} Rewards Expired</span>
        </div>
        <div class='metric-card blue'>
            <span class='metric-value'>{metrics['total_payment_stopped']}</span>
            <span class='metric-label'>{icons['payment_stopped']} Payment Stopped</span>
        </div>
        <div class='metric-card green'>
            <span class='metric-value'>{metrics['total_invalid']}</span>
            <span class='metric-label'>{icons['invalid']} Invalid Account</span>
        </div>
    </div>
    <div class='divider'></div>
    """, unsafe_allow_html=True)

display_metrics(metrics, icons)


# Create a chart for the `comment` column
def create_comment_chart(filtered_data):
    comment_counts = filtered_data['comment'].value_counts().reset_index()
    comment_counts.columns = ['comment', 'count']
    
    chart = alt.Chart(comment_counts).mark_bar().encode(
        x=alt.X('comment:N', title='Comment'),
        y=alt.Y('count:Q', title='Count'),
        tooltip=['comment', 'count']
    ).properties(
        title='',
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return chart

# Create a chart for the `city` column
def create_city_chart(filtered_data):
    city_counts = filtered_data['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
    
    chart = alt.Chart(city_counts).mark_bar().encode(
        x=alt.X('city:N', title='City'),
        y=alt.Y('count:Q', title='Count'),
        tooltip=['city', 'count']
    ).properties(
        title='',
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return chart

# Create a chart for the `onboarder` column
def create_onboarder_chart(filtered_data):
    onboarder_counts = filtered_data['onboarder'].value_counts().reset_index()
    onboarder_counts.columns = ['onboarder', 'count']
    
    chart = alt.Chart(onboarder_counts).mark_bar().encode(
        x=alt.X('onboarder:N', title='Onboarder'),
        y=alt.Y('count:Q', title='Count'),
        tooltip=['onboarder', 'count']
    ).properties(
        title='',
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return chart

# Create a pie chart for the `type_of_partner` column
def create_partner_pie_chart(filtered_data):
    partner_counts = filtered_data['type_of_partner'].value_counts().reset_index()
    partner_counts.columns = ['type_of_partner', 'count']
    partner_counts['percentage'] = (partner_counts['count'] / partner_counts['count'].sum()) * 100
    
    chart = alt.Chart(partner_counts).mark_arc().encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="type_of_partner", type="nominal"),
        tooltip=[alt.Tooltip('type_of_partner:N', title='Type of Partner'), 
                 alt.Tooltip('count:Q', title='Count'), 
                 alt.Tooltip('percentage:Q', title='Percentage', format='.1f')]
    ).properties(
        title='',
        width=600,
        height=400
    ).configure_title(
        fontSize=16
    )
    return chart

# Create a chart for weekly trends
def create_weekly_trends_chart(filtered_data):
    weekly_counts = filtered_data['new_week'].value_counts().reset_index()
    weekly_counts.columns = ['new_week', 'count']
    weekly_counts = weekly_counts.sort_values('new_week')
    
    chart = alt.Chart(weekly_counts).mark_line(point=True).encode(
        x=alt.X('new_week:O', title='Week'),
        y=alt.Y('count:Q', title='Count'),
        tooltip=['new_week', 'count']
    ).properties(
        title='',
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return chart

# Create a chart for yearly, monthly, and daily distribution
def create_date_distribution_chart(filtered_data, start_date, end_date):
    if start_date.year != end_date.year:
        # Different years selected
        yearly_counts = filtered_data['date'].dt.year.value_counts().reset_index()
        yearly_counts.columns = ['year', 'count']
        yearly_counts = yearly_counts.sort_values('year')
        
        chart = alt.Chart(yearly_counts).mark_bar().encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('count:Q', title='Total Drivers Onboarded'),
            tooltip=['year', 'count']
        ).properties(
            title='Yearly Distribution',
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )
        
    elif start_date.month != end_date.month:
        # Same year but different months selected
        monthly_counts = filtered_data['date'].dt.month.value_counts().reset_index()
        monthly_counts.columns = ['month', 'count']
        monthly_counts = monthly_counts.sort_values('month')
        monthly_counts['month'] = monthly_counts['month'].apply(lambda x: pd.Timestamp(1900, x, 1).strftime('%B'))
        
        chart = alt.Chart(monthly_counts).mark_bar().encode(
            x=alt.X('month:N', title='Month'),
            y=alt.Y('count:Q', title='Total Drivers Onboarded'),
            tooltip=['month', 'count']
        ).properties(
            title='Monthly Distribution',
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )
        
    else:
        # Same month selected
        daily_counts = filtered_data['date'].dt.day.value_counts().reset_index()
        daily_counts.columns = ['day', 'count']
        daily_counts = daily_counts.sort_values('day')
        
        chart = alt.Chart(daily_counts).mark_bar().encode(
            x=alt.X('day:O', title='Day'),
            y=alt.Y('count:Q', title='Total Drivers Onboarded'),
            tooltip=['day', 'count']
        ).properties(
            title='Daily Distribution',
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )
        
    return chart

# Display charts
chart1_col, chart2_col = st.columns(2)
chart3_col, chart4_col = st.columns(2)
chart5_col, chart6_col = st.columns(2)

with chart1_col:
    st.write("### Comment Distribution")
    comment_chart = create_comment_chart(filtered_data)
    st.altair_chart(comment_chart, use_container_width=True)

with chart2_col:
    st.write("### City Distribution")
    city_chart = create_city_chart(filtered_data)
    st.altair_chart(city_chart, use_container_width=True)

with chart3_col:
    st.write("### Onboarder Distribution")
    onboarder_chart = create_onboarder_chart(filtered_data)
    st.altair_chart(onboarder_chart, use_container_width=True)

with chart4_col:
    st.write("### Partner Distribution")
    partner_pie_chart = create_partner_pie_chart(filtered_data)
    st.altair_chart(partner_pie_chart, use_container_width=True)

with chart5_col:
    st.write("### Weekly Trends")
    weekly_trends_chart = create_weekly_trends_chart(filtered_data)
    st.altair_chart(weekly_trends_chart, use_container_width=True)

with chart6_col:
    st.write("### Date Distribution")
    date_distribution_chart = create_date_distribution_chart(filtered_data, start_date, end_date)
    st.altair_chart(date_distribution_chart, use_container_width=True)

# Display filtered data
st.write("### Filtered Uber Onboarding Data")
st.dataframe(filtered_data)
