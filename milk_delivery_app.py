import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import calendar

# Configure the page
st.set_page_config(
    page_title="Milk Delivery Payment Calculator",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stDataFrame {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_months_data(year, price_per_kg=55.0):
    """Generate months data for a given year"""
    months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    months = []
    days_in_months = []
    
    for i, month_name in enumerate(months_names, 1):
        # Get days in month for the given year
        days_in_month = calendar.monthrange(year, i)[1]
        days_in_months.append(days_in_month)
        months.append(f"{month_name} {str(year)[-2:]}")
    
    return {
        'Month': months,
        'Days': days_in_months,
        'per Kg in Rs': [price_per_kg] * 12,
        'Milk Not Delivered': [0] * 12,  # Start with no missed deliveries
        'Total Delivered Milk': days_in_months.copy(),
        'Amt in Rs': [days * price_per_kg for days in days_in_months]
    }

# Initialize session state for data persistence
if 'df' not in st.session_state:
    current_year = datetime.now().year
    st.session_state.selected_year = current_year
    st.session_state.price_per_kg = 55.0
    st.session_state.df = pd.DataFrame(get_months_data(current_year, 55.0))

def calculate_amounts(df, price_per_kg):
    """Calculate total delivered milk and amounts"""
    df['Total Delivered Milk'] = df['Days'] - df['Milk Not Delivered']
    df['per Kg in Rs'] = price_per_kg
    df['Amt in Rs'] = df['Total Delivered Milk'] * price_per_kg
    return df

def create_summary_metrics(df):
    """Create summary statistics"""
    total_payment = df['Amt in Rs'].sum()
    total_delivered_days = df['Total Delivered Milk'].sum()
    total_not_delivered_days = df['Milk Not Delivered'].sum()
    avg_monthly_payment = df['Amt in Rs'].mean()
    
    return {
        'total_payment': total_payment,
        'total_delivered_days': total_delivered_days,
        'total_not_delivered_days': total_not_delivered_days,
        'avg_monthly_payment': avg_monthly_payment
    }

def create_monthly_chart(df):
    """Create monthly payment chart"""
    fig = px.bar(
        df, 
        x='Month', 
        y='Amt in Rs',
        title='Monthly Payment Amount',
        labels={'Amt in Rs': 'Payment Amount (Rs)', 'Month': 'Month'},
        color='Amt in Rs',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    return fig

def create_delivery_pie_chart(df):
    """Create delivery status pie chart"""
    totals = df.groupby(['Total Delivered Milk', 'Milk Not Delivered']).size().reset_index(name='count')
    
    delivered = df['Total Delivered Milk'].sum()
    not_delivered = df['Milk Not Delivered'].sum()
    
    fig = px.pie(
        values=[delivered, not_delivered],
        names=['Delivered Days', 'Not Delivered Days'],
        title='Annual Delivery Status Distribution',
        color_discrete_map={'Delivered Days': '#4CAF50', 'Not Delivered Days': '#f44336'}
    )
    return fig

# Main app
def main():
    # Header
    st.title("🥛 Milk Delivery Payment Calculator")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Year selection
        selected_year = st.number_input(
            "Select Year", 
            min_value=2020, 
            max_value=2030, 
            value=st.session_state.selected_year,
            step=1,
            key="year_input"
        )
        
        # Check if year changed and regenerate data
        if selected_year != st.session_state.selected_year:
            st.session_state.selected_year = selected_year
            # Preserve existing "Milk Not Delivered" data if possible, otherwise reset
            if 'preserved_delivery_data' not in st.session_state:
                st.session_state.df = pd.DataFrame(get_months_data(selected_year, st.session_state.price_per_kg))
            else:
                months_data = get_months_data(selected_year, st.session_state.price_per_kg)
                # Apply previously saved delivery data if available
                if len(st.session_state.preserved_delivery_data) == 12:
                    months_data['Milk Not Delivered'] = st.session_state.preserved_delivery_data
                st.session_state.df = pd.DataFrame(months_data)
            st.rerun()
        
        # Price control
        new_price = st.number_input(
            "Price per Kg (Rs)", 
            min_value=1.0, 
            max_value=200.0, 
            value=st.session_state.price_per_kg,
            step=1.0,
            key="price_input"
        )
        
        if new_price != st.session_state.price_per_kg:
            st.session_state.price_per_kg = new_price
        
        # Data management
        st.markdown("### 📊 Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Data", use_container_width=True):
                # Save to JSON
                data_dict = st.session_state.df.to_dict('records')
                st.session_state.saved_data = data_dict
                st.success("Data saved!")
        
        with col2:
            if st.button("🔄 Load Data", use_container_width=True):
                if hasattr(st.session_state, 'saved_data'):
                    st.session_state.df = pd.DataFrame(st.session_state.saved_data)
                    st.success("Data loaded!")
                else:
                    st.warning("No saved data found!")
        
        if st.button("🔄 Reset to Default", use_container_width=True):
            # Reset to default data for current year
            st.session_state.df = pd.DataFrame(get_months_data(st.session_state.selected_year, 55.0))
            st.session_state.price_per_kg = 55.0
            # Add default delivery issue for May (common scenario)
            if len(st.session_state.df) > 4:  # May is the 5th month (index 4)
                st.session_state.df.loc[4, 'Milk Not Delivered'] = 12  # 12 days not delivered in May
                st.session_state.df = calculate_amounts(st.session_state.df, st.session_state.price_per_kg)
            st.success(f"Data reset for {st.session_state.selected_year}!")
    
    # Update calculations
    st.session_state.df = calculate_amounts(st.session_state.df, st.session_state.price_per_kg)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Monthly Delivery Data")
        
        # Make the dataframe editable
        df_editor = st.session_state.df.copy()
        
        # Configure column settings for editing
        column_config = {
            "Month": st.column_config.TextColumn("Month", disabled=True),
            "Days": st.column_config.NumberColumn("Days", disabled=True),
            "per Kg in Rs": st.column_config.NumberColumn("Price per Kg (Rs)", disabled=True),
            "Milk Not Delivered": st.column_config.NumberColumn("Days Not Delivered", min_value=0, max_value=31),
            "Total Delivered Milk": st.column_config.NumberColumn("Total Delivered", disabled=True),
            "Amt in Rs": st.column_config.NumberColumn("Amount (Rs)", disabled=True)
        }
        
        # Display editable dataframe
        edited_df = st.data_editor(
            df_editor,
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )
        
        # Update session state if data was edited
        if not edited_df.equals(st.session_state.df):
            # Preserve the "Milk Not Delivered" data for year changes
            st.session_state.preserved_delivery_data = edited_df['Milk Not Delivered'].tolist()
            st.session_state.df = edited_df
            st.session_state.df = calculate_amounts(st.session_state.df, st.session_state.price_per_kg)
            st.rerun()
    
    with col2:
        st.subheader("📊 Summary")
        
        # Calculate summary metrics
        metrics = create_summary_metrics(st.session_state.df)
        
        # Display metrics
        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 Total Annual Payment</h4>
            <h2>₹{metrics['total_payment']:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>✅ Total Delivered Days</h4>
            <h2>{metrics['total_delivered_days']} days</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>❌ Not Delivered Days</h4>
            <h2>{metrics['total_not_delivered_days']} days</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 Avg Monthly Payment</h4>
            <h2>₹{metrics['avg_monthly_payment']:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown("---")
    st.subheader("📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly payment chart
        fig1 = create_monthly_chart(st.session_state.df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Delivery status pie chart
        fig2 = create_delivery_pie_chart(st.session_state.df)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Data export section
    st.markdown("---")
    st.subheader("💾 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download as CSV
        csv = st.session_state.df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="milk_delivery_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Download as JSON
        json_data = st.session_state.df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="milk_delivery_data.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Milk Delivery Payment Calculator | Made with ❤️ by bluetoro_dev</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()