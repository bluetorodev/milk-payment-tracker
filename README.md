# 🥛 Milk Delivery Payment Calculator

An interactive Streamlit application for tracking and calculating milk delivery payments based on your original spreadsheet data.

## Features

- 📅 **Year Selection**: Choose any year from 2020-2030 and get accurate month/day calculations
- 📋 **Interactive Data Table**: Edit delivery days directly in the interface
- 💰 **Dynamic Calculations**: Automatic calculation of amounts based on delivery status
- 📊 **Summary Statistics**: View total payments, delivered days, and averages
- 📈 **Data Visualization**: Charts showing monthly payments and delivery distribution
- 💾 **Data Persistence**: Save and load your data between sessions
- 📥 **Export Options**: Download data as CSV or JSON files
- ⚙️ **Flexible Pricing**: Adjust milk price per kg dynamically
- 🗓️ **Leap Year Support**: Automatically handles leap years (February with 29 days)

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run milk_delivery_app.py
   ```

3. **Open in Browser**: The app will automatically open in your default browser at `http://localhost:8501`

## Usage Guide

### Year Selection
- Use the "Select Year" input in the sidebar to choose any year (2020-2030)
- The app automatically calculates the correct number of days for each month
- Leap years are handled automatically (February will show 29 days in leap years)
- Your delivery data is preserved when switching between years

### Editing Data
- Click on any cell in the "Days Not Delivered" column to edit delivery status
- Use the sidebar to change the price per kilogram
- Changes are automatically calculated and displayed

### Saving Data
- Use the "Save Data" button in the sidebar to store your current session
- Use "Load Data" to restore previously saved information
- "Reset to Default" restores data for the current year with default settings

### Visualizations
- **Monthly Payment Chart**: Bar chart showing payment amounts for each month
- **Delivery Status Pie Chart**: Distribution of delivered vs not delivered days
- **Summary Cards**: Key metrics displayed in an easy-to-read format

### Exporting Data
- Download your current data as CSV for use in Excel or other spreadsheet applications
- Export as JSON for data interchange or backup purposes

## Data Structure

The app dynamically generates the following information for each month based on the selected year:
- **Month**: Month and year identifier (e.g., "Jan 25" for January 2025)
- **Days**: Total days in the month (automatically calculated, 28-31 days)
- **Price per Kg**: Current milk price in Rupees
- **Days Not Delivered**: Editable field for tracking missed deliveries
- **Total Delivered**: Calculated field (Total days - Not delivered days)
- **Amount**: Calculated payment amount (Delivered days × Price per kg)

### Leap Year Handling
- The app automatically detects leap years and sets February to 29 days
- Non-leap years will have February with 28 days
- All other months remain constant (31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

## Technical Details

- Built with Streamlit for interactive web interface
- Uses Plotly for interactive charts and visualizations
- Pandas for data manipulation and calculations
- Session state for data persistence during runtime
- Responsive design that works on desktop and mobile devices

## Author

Created with 💖 by bluetoro_dev.