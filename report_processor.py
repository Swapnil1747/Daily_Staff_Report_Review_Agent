import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DailyReportProcessor:
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
    
    def process_reports(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
        """
        Process daily reports to detect missed tasks and generate actions.
        
        Returns:
            Tuple of (results_df, errors, warnings)
        """
        # Reset results and error tracking
        self.results = []
        self.errors = []
        self.warnings = []
        
        try:
            # Data cleaning and validation
            df_clean = self._clean_data(df)
            
            if df_clean.empty:
                self.errors.append("No valid data found after cleaning")
                return pd.DataFrame(columns=['Employee', 'Task', 'Date(s) Missed', 'Action', 'Priority', 'Days Missed']), self.errors, self.warnings
            
            # Filter for 'Not Done' tasks only
            not_done_tasks = df_clean[df_clean['Status'].str.upper().isin(['NOT DONE', 'NOTDONE', 'INCOMPLETE', 'MISSED'])].copy()
            
            if not_done_tasks.empty:
                self.warnings.append("No missed tasks found in the data")
                return pd.DataFrame(columns=['Employee', 'Task', 'Date(s) Missed', 'Action', 'Priority', 'Days Missed']), self.errors, self.warnings
            
            # Group by Employee and Task to analyze patterns
            grouped = not_done_tasks.groupby(['Employee', 'Task'])
            
            for (employee, task), group in grouped:
                try:
                    # Sort dates to check for consecutive misses
                    dates = sorted(group['Date'].tolist())
                    
                    # Analyze consecutive patterns
                    consecutive_groups = self._find_consecutive_groups(dates)
                    
                    for date_group in consecutive_groups:
                        priority = self._calculate_priority(len(date_group), task)
                        
                        if len(date_group) == 1:
                            # Single miss - Follow-up
                            self.results.append({
                                'Employee': employee,
                                'Task': task,
                                'Date(s) Missed': date_group[0].strftime('%Y-%m-%d'),
                                'Action': 'Follow-up',
                                'Priority': priority,
                                'Days Missed': 1
                            })
                        else:
                            # Multiple consecutive days - Escalate
                            date_range = f"{date_group[0].strftime('%Y-%m-%d')} to {date_group[-1].strftime('%Y-%m-%d')}"
                            self.results.append({
                                'Employee': employee,
                                'Task': task,
                                'Date(s) Missed': date_range,
                                'Action': 'Escalate',
                                'Priority': priority,
                                'Days Missed': len(date_group)
                            })
                            
                except Exception as e:
                    self.errors.append(f"Error processing {employee} - {task}: {str(e)}")
                    logger.error(f"Error processing {employee} - {task}: {str(e)}")
            
            results_df = pd.DataFrame(self.results)
            
            # Sort by priority and days missed
            if not results_df.empty:
                priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
                results_df['priority_sort'] = results_df['Priority'].map(priority_order)
                results_df = results_df.sort_values(['priority_sort', 'Days Missed'], ascending=[True, False])
                results_df = results_df.drop('priority_sort', axis=1)
            
            return results_df, self.errors, self.warnings
            
        except Exception as e:
            self.errors.append(f"Critical error in processing: {str(e)}")
            logger.error(f"Critical error in processing: {str(e)}")
            return pd.DataFrame(columns=['Employee', 'Task', 'Date(s) Missed', 'Action', 'Priority', 'Days Missed']), self.errors, self.warnings
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the input data"""
        try:
            df_clean = df.copy()
            
            # Remove rows with missing critical data
            initial_count = len(df_clean)
            df_clean = df_clean.dropna(subset=['Employee', 'Task', 'Date', 'Status'])
            
            if len(df_clean) < initial_count:
                self.warnings.append(f"Removed {initial_count - len(df_clean)} rows with missing critical data")
            
            # Clean employee names
            df_clean['Employee'] = df_clean['Employee'].astype(str).str.strip().str.title()
            
            # Clean task names
            df_clean['Task'] = df_clean['Task'].astype(str).str.strip()
            
            # Clean status values
            df_clean['Status'] = df_clean['Status'].astype(str).str.strip().str.upper()
            
            # Convert dates with error handling
            date_errors = 0
            for idx, date_val in df_clean['Date'].items():
                try:
                    if pd.isna(date_val):
                        df_clean = df_clean.drop(idx)
                        date_errors += 1
                        continue
                    
                    # Try to parse different date formats
                    if isinstance(date_val, str):
                        # Common date formats
                        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%m-%d-%Y', '%d-%m-%Y']:
                            try:
                                df_clean.at[idx, 'Date'] = pd.to_datetime(date_val, format=fmt)
                                break
                            except:
                                continue
                        else:
                            # If no format worked, try pandas auto-parsing
                            df_clean.at[idx, 'Date'] = pd.to_datetime(date_val, errors='coerce')
                    else:
                        df_clean.at[idx, 'Date'] = pd.to_datetime(date_val, errors='coerce')
                        
                    if pd.isna(df_clean.at[idx, 'Date']):
                        df_clean = df_clean.drop(idx)
                        date_errors += 1
                        
                except Exception as e:
                    df_clean = df_clean.drop(idx)
                    date_errors += 1
            
            if date_errors > 0:
                self.warnings.append(f"Removed {date_errors} rows with invalid dates")
            
            # Remove duplicates
            initial_count = len(df_clean)
            df_clean = df_clean.drop_duplicates(subset=['Employee', 'Task', 'Date'])
            
            if len(df_clean) < initial_count:
                self.warnings.append(f"Removed {initial_count - len(df_clean)} duplicate entries")
            
            return df_clean
            
        except Exception as e:
            self.errors.append(f"Error in data cleaning: {str(e)}")
            return pd.DataFrame()
    
    def _find_consecutive_groups(self, dates: List[datetime]) -> List[List[datetime]]:
        """Find groups of consecutive dates with improved logic"""
        if not dates:
            return []
        
        groups = []
        current_group = [dates[0]]
        
        for i in range(1, len(dates)):
            # Check if current date is consecutive to the previous one (within 1-2 days to account for weekends)
            days_diff = (dates[i] - dates[i-1]).days
            if days_diff <= 3:  # Allow for weekends
                current_group.append(dates[i])
            else:
                # Start a new group
                groups.append(current_group)
                current_group = [dates[i]]
        
        # Add the last group
        groups.append(current_group)
        
        return groups
    
    def _calculate_priority(self, days_missed: int, task: str) -> str:
        """Calculate priority based on days missed and task type"""
        # Critical tasks (safety, compliance related)
        critical_keywords = ['safety', 'security', 'compliance', 'audit', 'emergency', 'critical']
        high_keywords = ['quality', 'customer', 'client', 'deadline', 'urgent']
        
        task_lower = task.lower()
        
        # Check if it's a critical task
        if any(keyword in task_lower for keyword in critical_keywords):
            return 'Critical' if days_missed >= 1 else 'High'
        
        # Check if it's a high priority task
        if any(keyword in task_lower for keyword in high_keywords):
            return 'Critical' if days_missed >= 3 else 'High'
        
        # Regular tasks
        if days_missed >= 5:
            return 'Critical'
        elif days_missed >= 3:
            return 'High'
        elif days_missed >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Enhanced data validation"""
        try:
            if df.empty:
                return False, "The uploaded file is empty"
            
            required_columns = ['Employee', 'Task', 'Date', 'Status']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"
            
            # Check for minimum data requirements
            if len(df) < 1:
                return False, "File must contain at least one data row"
            
            # Check data types and formats
            issues = []
            
            # Check for empty critical columns
            for col in required_columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    issues.append(f"{col}: {null_count} missing values")
            
            if issues:
                return True, f"Data validation warnings: {'; '.join(issues)}"
            
            return True, "Data validation successful"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def generate_summary_report(self, results_df: pd.DataFrame) -> Dict:
        """Generate comprehensive summary statistics"""
        if results_df.empty:
            return {
                'total_issues': 0,
                'employees_affected': 0,
                'tasks_affected': 0,
                'action_breakdown': {},
                'priority_breakdown': {},
                'avg_days_missed': 0,
                'most_problematic_employee': 'None',
                'most_problematic_task': 'None'
            }
        
        summary = {
            'total_issues': len(results_df),
            'employees_affected': results_df['Employee'].nunique(),
            'tasks_affected': results_df['Task'].nunique(),
            'action_breakdown': results_df['Action'].value_counts().to_dict(),
            'priority_breakdown': results_df['Priority'].value_counts().to_dict(),
            'avg_days_missed': results_df['Days Missed'].mean(),
            'most_problematic_employee': results_df['Employee'].value_counts().index[0] if not results_df.empty else 'None',
            'most_problematic_task': results_df['Task'].value_counts().index[0] if not results_df.empty else 'None'
        }
        
        return summary