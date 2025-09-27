import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_data() -> pd.DataFrame:
    """
    Generate sample daily reports data for demonstration.
    """
    employees = ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Emily Brown', 'David Wilson']
    tasks = [
        'Daily Safety Check',
        'Equipment Maintenance',
        'Quality Control Review',
        'Inventory Count',
        'Team Meeting Attendance',
        'Report Submission',
        'Customer Follow-up'
    ]
    
    # Generate data for the last 10 days
    start_date = datetime.now() - timedelta(days=9)
    dates = [start_date + timedelta(days=i) for i in range(10)]
    
    data = []
    
    for employee in employees:
        for date in dates:
            # Each employee gets 3-4 random tasks per day
            daily_tasks = random.sample(tasks, random.randint(3, 4))
            
            for task in daily_tasks:
                # 85% chance of "Done", 15% chance of "Not Done"
                status = "Done" if random.random() > 0.15 else "Not Done"
                
                # Create some patterns for demonstration
                if employee == "Mike Davis" and task == "Equipment Maintenance":
                    if date.day % 3 == 0:  # Every 3rd day
                        status = "Not Done"
                
                if employee == "Sarah Johnson" and task == "Report Submission":
                    if date >= datetime.now() - timedelta(days=3):  # Last 3 days
                        status = "Not Done"
                
                data.append({
                    'Employee': employee,
                    'Task': task,
                    'Date': date.strftime('%Y-%m-%d'),
                    'Status': status
                })
    
    return pd.DataFrame(data)

def save_sample_excel():
    """
    Save sample data as Excel file for download.
    """
    df = generate_sample_data()
    df.to_excel('sample_daily_reports.xlsx', index=False)
    return df