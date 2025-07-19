# VAPI Car Rental Assistant

A Python application that creates an AI-powered customer service agent for Ultra Car Rental Service using the VAPI platform.

## Overview

This application creates "Elizabeth", an AI assistant that helps customers with car rental inquiries including:
- Account lookups
- Rental start/end dates
- Extension cost calculations

## Setup

1. Install dependencies:
```bash
pip install requests python-dotenv
```

2. Set your VAPI API key:
```bash
export VAPI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python app.py
```

## Features

- **File Upload**: Uploads customer data (renters_info.csv) and rental schedules (rental_schedule.csv) to VAPI
- **Agent Creation**: Creates an AI assistant with GPT-4o model and Kylie voice
- **Custom Tools**: Three specialized tools for account lookup, rental dates, and extension costs
- **Knowledge Base**: Integrates CSV data for real-time customer information retrieval

## Data Files

- `renters_info.csv`: Customer information (name, phone, rental agreement number, age)
- `rental_schedule.csv`: Rental details (dates, costs, extension rates)

## Video Demonstration

Watch the full tutorial and demonstration: https://www.youtube.com/watch?v=RaLstFJtXZE