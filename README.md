[![Coverage](.github/badges/coverage.svg)](https://nafanius.github.io/list_holcim/coverage_html_report/)
[![pages-build-deployment](https://github.com/nafanius/list_holcim/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/nafanius/list_holcim/actions/workflows/pages/pages-build-deployment)
[![Test and Coverage](https://github.com/nafanius/list_holcim/actions/workflows/ci.yml/badge.svg)](https://github.com/nafanius/list_holcim/actions/workflows/ci.yml)

# Concrete Delivery Management System

**Live site:** [holcim_lista](https://bit.ly/holcim_lista)

**Static Example on GitHub Pages** [GitHub Pages](https://nafanius.github.io/list_holcim/)

## Overview

The **Concrete Delivery Management System** is a comprehensive tool for managing concrete delivery processes. It allows real-time analysis, synchronization, and visualization of operational data. The system operates via a web interface and integrates with a chatbot for quick updates and communication with drivers.

The system automatically syncs data from Google Sheets and receives messages from drivers about order deliveries.

The homepage displays data for the current day and the next two business days.

## Data Updates

Information is updated through:

- Synchronization of orders from Google Sheets (every 20 minutes).
- Messages from drivers via the chatbot about the status of specific orders.

⚠ Note: The chatbot update feature works only on Warsow Zawodzie 14.

## Features

### Branch Switcher

A button to change the concrete plant branch.

### Data Display

Data is displayed for the following three business days:

- **Current day** (green background),
- **Next business day** (yellow background),
- **Following business day** (pink background).

### Data Sections

1. **ROZKŁAD**: Driver schedule, availability analysis, and planning.
2. **ZAMÓWIENIA**: List of customer orders and their changes.
3. **HARMONOGRAM ZAŁADUNKÓW**: Concrete mixer loading plan and statistics.

---

### 1. ROZKŁAD

The **ROZKŁAD** is generated by the dispatcher at the end of the workday for the following day (source: Google Sheets).

#### Forecast of First Loading Time and Number of Trips

- Analyzes the schedule and predicts the number of trips for each driver.
- Shows when the driver will pick up the first order.
- Adjusted during the workday based on delays, cancellations, etc.
- Updates based on changes in Google Sheets and messages from drivers.

#### Auto-Generated Schedule

- If the dispatcher’s schedule is unavailable, the system automatically generates one based on the **HARMONOGRAM ZAŁADUNKÓW** and the number of available drivers.
- If there are not enough drivers, the system highlights problematic periods in red and generates a table with details.

#### "Available Drivers Schedule" Chart

- Shows the number of available drivers throughout the day.
- If drivers are unavailable, the chart drops below zero (in red).

#### Optimal Number of Drivers and First Loading Time

- Analyzes the **ZAMÓWIENIA** and **HARMONOGRAM ZAŁADUNKÓW**.
- Determines the minimum required number of drivers.
- Indicates the start time for drivers to avoid staff shortages.

---

### 2. ZAMÓWIENIA

Displays a list of customer orders that updates every 20 minutes during working hours (synchronization with Google Sheets).

Recent changes (within 4 hours) are highlighted in colors:

- ❌ **Red** (struck-through): Deleted orders.
- ✅ **Green**: New or added orders.

---

### 3. HARMONOGRAM ZAŁADUNKÓW

Shows loading details such as time, product quantity, loading number, remaining amounts, etc.

- Dynamically updates via Google Sheets and chatbot messages from drivers.

**Color Codes:**

- 🟠 **Orange**: Orders currently being loaded.

#### "Work Intensity" Chart

- 🔵 **Blue**: Amount of concrete loaded per hour.
- 🟠 **Orange**: Amount of concrete remaining to be loaded in current orders.

#### "Crane/Pump Ratio" Chart

- Represents the proportion of loads made by crane versus pump.

## Project Structure

```
📦 concrete-delivery-management
├── 📁 data_drive/                      # Database access and SQL-related logic
│   ├── __init__.py
│   └── data_sql.py
├── 📁 html_driver/                     # HTML extraction utilities
│   ├── __init__.py
│   └── get_html.py
├── 📁 jupyter/                         # Jupyter notebooks for data analysis
│   ├── 1.py
│   ├── __init__.py
│   ├── driver_stat.ipynb
│   ├── driver_stat_for_count_optimal_drivers_and_time.ipynb
│   ├── DRIVERS.ipynb
│   ├── rozklad_kurs.ipynb
│   ├── rozklad_kurs_for_difrents time.ipynb
│   └── Untitled.ipynb
├── 📁 site/                            # Web frontend
│   ├── index.html
│   └── 📁 static/
│       ├── 📁 image/
│       │   ├── favicon-16x16.png
│       │   └── holcim_logo_color.svg
│       └── 📁 styles/
│           └── styles.css
├── 📁 src/                             # Core backend logic
│   ├── __init__.py
│   ├── convert_lists.py                # Converting data and adding HTML tags
│   ├── download_excel.py               # Download Google Sheets in Excel format to local instance
│   ├── get_del_new_lists.py            # Monitoring changes compared to the previous state of the file
│   ├── get_lista.py                    # Obtaining current data from the file
│   ├── reboot_system.py                # Restart the system if there is no internet connection
│   └── settings.py
├── 📁 statistic/                       # Statistical calculations and models
│   ├── __init__.py
│   ├── adjust_time.py
│   ├── driver.py
│   ├── order.py
│   └── static_forms.py
├── 📁 tests/                           # Unit tests
│   ├── __init__.py
│   ├── test_adjust_time.py
│   ├── test_driver.py
│   └── test_order.py
├── 📄 Holcim_lista_polish.pdf          # Project description and instructions in Polish for users
├── 📄 LICENSE                          # MIT license file
├── 📄 main.py                          # Entry point of the application
├── 📄 README.md                        # Project description and instructions
└── 📄 requirement.txt                  # Python dependencies
```

---

## Future Developments

Potential features include:

- **Vehicle Movement Monitoring**:

  - Automatic license plate scanning at the site entrance and exit using cameras.
  - Analysis of driver departure and return times linked to specific orders.
  - GPS data integration for vehicle tracking and precise delivery time monitoring.

- **Client Location and Route Optimization**:

  - Adding GPS coordinates for client construction sites.
  - Estimating driver arrival times to sites and return to the plant.
  - Real-time traffic data (e.g., via Google Maps) for better delivery planning.

- **Unloading Queue Monitoring**:

  - Tracking the number of vehicles waiting to unload at the client site using GPS.
  - Real-time data analysis and dynamic adjustments to loading pace.

- **Electronic Loading Queue**:

  - Implementing systems to notify drivers of their loading order via electronic boards, chatbots, or SMS.

- **Driver Demand Analysis**:
  - Forecasting the optimal number of drivers for planned orders.
  - Auto-adjusting the driver schedule to minimize downtime and maximize efficiency.
  - Identifying moments when driver shortages might occur for proactive resource management.

---

## Installation

To use the system, clone this repository and follow the installation steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nafanius/list_holcim.git
   ```
2. Set up the environment and dependencies (e.g., Google Sheets API).

3. Configure the chatbot and data synchronization.

4. Start the server and access the web interface.
