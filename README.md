# Local Data Analysis of System Logs

## Project Overview
This project focuses on extracting, processing, and visualizing data from local system log files (`/var/log/syslog`). It provides insights into system activity patterns and error distribution using Python.

## Features
* **Log Parsing**: Automated extraction of timestamps, services, and log levels using Regex.
* **Visualizations**: 
    * Bar charts to identify resource spikes and hourly activity.
    * Pie charts to show the distribution of log severity (INFO vs ERROR).
* **Export**: Automatic generation of HTML reports for deep-dive analysis.
* **Automation**: Script structure ready for weekly scheduling via Cron.

## Requirements
* Python 3.x
* Pandas
* Matplotlib
* Seaborn

## Installation & Usage
1. Activate your virtual environment:
   ```bash
   source myenv/bin/activate