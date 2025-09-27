import streamlit as st
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from report_processor import DailyReportProcessor
from sample_data import generate_sample_data, save_sample_excel

# Page configuration
st.set_page_config(
    page_title="Daily Staff Report Review Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .error-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def display_priority_badge(priority):
    """Display priority with color coding"""
    colors = {
        'Critical': '🔴',
        'High': '🟠', 
        'Medium': '🟡',
        'Low': '🟢'
    }
    return f"{colors.get(priority, '⚪')} {priority}"

def create_visualizations(results_df, summary):
    """Create data visualizations"""
    if results_df.empty:
        st.info("No data available for visualization")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Action breakdown pie chart
        if summary['action_breakdown']:
            fig_actions = px.pie(
                values=list(summary['action_breakdown'].values()),
                names=list(summary['action_breakdown'].keys()),
                title="Actions Required Distribution",
                color_discrete_map={'Follow-up': '#36a2eb', 'Escalate': '#ff6384'}
            )
            st.plotly_chart(fig_actions, use_container_width=True)
    
    with col2:
        # Priority breakdown bar chart
        if summary['priority_breakdown']:
            fig_priority = px.bar(
                x=list(summary['priority_breakdown'].keys()),
                y=list(summary['priority_breakdown'].values()),
                title="Issues by Priority Level",
                color=list(summary['priority_breakdown'].keys()),
                color_discrete_map={
                    'Critical': '#dc3545',
                    'High': '#fd7e14', 
                    'Medium': '#ffc107',
                    'Low': '#28a745'
                }
            )
            st.plotly_chart(fig_priority, use_container_width=True)
    
    # Employee performance chart
    if len(results_df) > 0:
        employee_issues = results_df['Employee'].value_counts().head(10)
        if len(employee_issues) > 0:
            fig_employees = px.bar(
                x=employee_issues.values,
                y=employee_issues.index,
                orientation='h',
                title="Top 10 Employees with Most Issues",
                labels={'x': 'Number of Issues', 'y': 'Employee'}
            )
            st.plotly_chart(fig_employees, use_container_width=True)

def main():
    st.title("📊 Daily Staff Report Review Agent")
    st.markdown("### Advanced Task Monitoring & Escalation System")
    st.markdown("---")
    
    # Enhanced overview with features
    with st.expander("🚀 Features & Capabilities", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **📊 Analysis Features:**
            - Smart consecutive day detection
            - Priority-based task classification
            - Advanced data cleaning
            - Multiple date format support
            """)
        with col2:
            st.markdown("""
            **🔍 Error Handling:**
            - Comprehensive data validation
            - Automatic data cleaning
            - Detailed error reporting
            - Warning system for data issues
            """)
        with col3:
            st.markdown("""
            **📈 Reporting:**
            - Interactive visualizations
            - Detailed summary statistics
            - Export capabilities
            - Priority-based sorting
            """)
    
    # Initialize processor
    processor = DailyReportProcessor()
    
    # Sidebar for options
    st.sidebar.header("⚙️ Configuration")
    
    # Option to use sample data or upload file
    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Upload Excel File", "Use Sample Data"]
    )
    
    # Advanced settings
    with st.sidebar.expander("🔧 Advanced Settings"):
        show_warnings = st.checkbox("Show data warnings", value=True)
        show_visualizations = st.checkbox("Show visualizations", value=True)
        auto_analyze = st.checkbox("Auto-analyze on upload", value=False)
    
    # Initialize session state for data
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'data_generated' not in st.session_state:
        st.session_state.data_generated = False
    
    df = None
    
    if data_source == "Upload Excel File":
        st.subheader("📁 Upload Daily Reports")
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="File should contain columns: Employee, Task, Date, Status"
        )
        
        if uploaded_file is not None:
            try:
                # Show file details
                file_details = {
                    "Filename": uploaded_file.name,
                    "File size": f"{uploaded_file.size / 1024:.2f} KB",
                    "File type": uploaded_file.type
                }
                
                with st.expander("📋 File Details"):
                    for key, value in file_details.items():
                        st.write(f"**{key}:** {value}")
                
                # Read the file with error handling
                try:
                    df = pd.read_excel(uploaded_file)
                    st.session_state.df = df
                    st.success(f"✅ File uploaded successfully! {len(df)} records found.")
                except Exception as read_error:
                    st.error(f"❌ Error reading Excel file: {str(read_error)}")
                    st.info("💡 Try saving your file as .xlsx format or check for corrupted data")
                    return
                    
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                return
    
    else:
        st.subheader("📋 Sample Data")
        st.info("💡 Using generated sample data for demonstration")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Generate Sample Data", type="primary"):
                with st.spinner("Generating sample data..."):
                    df = generate_sample_data()
                    st.session_state.df = df
                    st.session_state.data_generated = True
                st.success(f"✅ Sample data generated! {len(df)} records created.")
        
        with col2:
            if st.button("📥 Download Sample Template"):
                sample_excel = save_sample_excel()
                with open('sample_daily_reports.xlsx', 'rb') as f:
                    st.download_button(
                        label="📥 Download Sample Excel File",
                        data=f.read(),
                        file_name="sample_daily_reports.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        # Use the data from session state if available
        if st.session_state.data_generated and st.session_state.df is not None:
            df = st.session_state.df
    
    # Use session state data if available
    if df is None and st.session_state.df is not None:
        df = st.session_state.df
    
    if df is not None:
        # Enhanced data validation
        is_valid, message = processor.validate_data(df)
        
        if not is_valid:
            st.error(f"❌ {message}")
            st.info("💡 Required columns: Employee, Task, Date, Status")
            
            # Show data preview for debugging
            st.subheader("🔍 Data Preview (for debugging)")
            st.dataframe(df.head(), use_container_width=True)
            return
        else:
            if "warning" in message.lower():
                st.warning(f"⚠️ {message}")
            else:
                st.success(f"✅ {message}")
        
        # Display data preview
        st.subheader("📊 Data Preview")
        
        # Data summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📋 Total Records", len(df))
        with col2:
            st.metric("👥 Employees", df['Employee'].nunique())
        with col3:
            st.metric("📝 Unique Tasks", df['Task'].nunique())
        with col4:
            # Fix the status checking logic
            status_check = df['Status'].astype(str).str.upper()
            not_done_count = len(df[status_check.isin(['NOT DONE', 'NOTDONE', 'INCOMPLETE', 'MISSED'])])
            st.metric("❌ Not Done Tasks", not_done_count)
        with col5:
            try:
                # Convert dates properly for display
                df_temp = df.copy()
                df_temp['Date'] = pd.to_datetime(df_temp['Date'], errors='coerce')
                date_range = f"{df_temp['Date'].min().strftime('%Y-%m-%d')} to {df_temp['Date'].max().strftime('%Y-%m-%d')}" if len(df_temp) > 0 else "N/A"
                st.metric("📅 Date Range", "")
                st.caption(date_range)
            except:
                st.metric("📅 Date Range", "")
                st.caption("Invalid dates")
        
        # Show data preview table
        with st.expander("👁️ View Data Details", expanded=False):
            st.dataframe(df, use_container_width=True)
        
        # Process reports
        st.subheader("🔍 Analysis Results")
        
        analyze_button = st.button("🚀 Analyze Reports", type="primary") or (auto_analyze and df is not None)
        
        if analyze_button:
            with st.spinner("🔄 Processing reports... This may take a moment for large datasets."):
                try:
                    results_df, errors, warnings = processor.process_reports(df)
                    
                    # Display errors if any
                    if errors:
                        st.error("❌ **Errors encountered during processing:**")
                        for error in errors:
                            st.error(f"• {error}")
                    
                    # Display warnings if any and if enabled
                    if warnings and show_warnings:
                        st.warning("⚠️ **Processing warnings:**")
                        for warning in warnings:
                            st.warning(f"• {warning}")
                    
                    if results_df.empty:
                        st.success("🎉 **Excellent news!** No missed tasks found.")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ **Found {len(results_df)} issues requiring attention**")
                        
                        # Enhanced results display with priority colors
                        st.markdown("### 📋 Detailed Results")
                        
                        # Display the results table with proper formatting
                        st.dataframe(
                            results_df,
                            use_container_width=True,
                            column_config={
                                "Priority": st.column_config.TextColumn("Priority", width="small"),
                                "Action": st.column_config.TextColumn("Action", width="small"),
                                "Days Missed": st.column_config.NumberColumn("Days Missed", width="small")
                            }
                        )
                        
                        # Generate and display summary
                        summary = processor.generate_summary_report(results_df)
                        
                        st.markdown("### 📈 Summary Statistics")
                        
                        # Enhanced metrics display
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("🚨 Total Issues", summary['total_issues'])
                        with col2:
                            st.metric("👥 Employees Affected", summary['employees_affected'])
                        with col3:
                            st.metric("📝 Tasks Affected", summary['tasks_affected'])
                        with col4:
                            st.metric("📊 Avg Days Missed", f"{summary['avg_days_missed']:.1f}")
                        
                        # Action and priority breakdown
                        col1, col2 = st.columns(2)
                        with col1:
                            if summary['action_breakdown']:
                                st.markdown("**🎯 Actions Required:**")
                                for action, count in summary['action_breakdown'].items():
                                    st.write(f"• {action}: {count}")
                        
                        with col2:
                            if summary['priority_breakdown']:
                                st.markdown("**⚡ Priority Breakdown:**")
                                for priority, count in summary['priority_breakdown'].items():
                                    st.write(f"• {display_priority_badge(priority)}: {count}")
                        
                        # Key insights
                        st.markdown("### 🎯 Key Insights")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"**Most Issues:** {summary['most_problematic_employee']}")
                        with col2:
                            st.info(f"**Most Missed Task:** {summary['most_problematic_task']}")
                        
                        # Visualizations
                        if show_visualizations:
                            st.markdown("### 📊 Data Visualizations")
                            create_visualizations(results_df, summary)
                        
                        # Download options
                        st.markdown("### 📥 Export Options")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📄 Download Results (CSV)",
                                data=csv,
                                file_name=f"staff_report_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        
                        with col2:
                            # Create Excel with multiple sheets
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                results_df.to_excel(writer, sheet_name='Analysis Results', index=False)
                                
                                # Summary sheet
                                summary_df = pd.DataFrame([summary])
                                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                                
                                # Employee breakdown
                                if not results_df.empty:
                                    employee_breakdown = results_df.groupby('Employee').agg({
                                        'Task': 'count',
                                        'Days Missed': 'sum',
                                        'Priority': lambda x: ', '.join(x.unique())
                                    }).rename(columns={'Task': 'Total Issues'})
                                    employee_breakdown.to_excel(writer, sheet_name='Employee Breakdown')
                            
                            st.download_button(
                                label="📊 Download Full Report (Excel)",
                                data=buffer.getvalue(),
                                file_name=f"staff_report_full_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        
                        with col3:
                            # Generate action plan
                            action_plan = []
                            for _, row in results_df.iterrows():
                                if row['Action'] == 'Escalate':
                                    action_plan.append(f"🔴 URGENT: Contact {row['Employee']} about {row['Task']} (missed {row['Days Missed']} days)")
                                else:
                                    action_plan.append(f"🟡 Follow up with {row['Employee']} about {row['Task']}")
                            
                            action_text = "\n".join(action_plan)
                            st.download_button(
                                label="📋 Download Action Plan",
                                data=action_text,
                                file_name=f"action_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                
                except Exception as process_error:
                    st.error(f"❌ **Critical error during analysis:** {str(process_error)}")
                    st.info("💡 Please check your data format and try again. If the problem persists, try using sample data to test the system.")
                    # Show debug information
                    st.subheader("🔧 Debug Information")
                    st.write("**Data shape:**", df.shape)
                    st.write("**Columns:**", list(df.columns))
                    st.write("**Data types:**")
                    st.write(df.dtypes)
                    st.write("**Sample data:**")
                    st.dataframe(df.head(3))
    
    # Enhanced instructions section
    st.markdown("---")
    st.subheader("📖 User Guide")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Quick Start", "📊 Data Format", "🔧 Features", "❓ Troubleshooting"])
    
    with tab1:
        st.markdown("""
        ### How to use this application:
        1. **📁 Choose Data Source**: Upload your Excel file or use sample data for testing
        2. **✅ Validation**: The system automatically validates your data format
        3. **🔍 Analysis**: Click "Analyze Reports" to process the data
        4. **📊 Results**: View detailed results with priority levels and visualizations
        5. **📥 Export**: Download results in multiple formats for reporting
        
        **💡 Pro Tips:**
        - Use the sample data feature to understand the expected format
        - Enable auto-analyze for immediate results upon upload
        - Check advanced settings for customization options
        """)
    
    with tab2:
        st.markdown("""
        ### Required Data Format:
        Your Excel file must contain these columns:
        """)
        
        sample_format = pd.DataFrame({
            'Employee': ['John Smith', 'Sarah Johnson', 'John Smith'],
            'Task': ['Safety Check', 'Report Submission', 'Safety Check'],
            'Date': ['2024-01-01', '2024-01-01', '2024-01-02'],
            'Status': ['Done', 'Not Done', 'Not Done']
        })
        st.dataframe(sample_format, use_container_width=True)
        
        st.markdown("""
        **📝 Column Details:**
        - **Employee**: Staff member name (text)
        - **Task**: Task description (text)
        - **Date**: Task date (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)
        - **Status**: Task completion status ("Done", "Not Done", "Incomplete", "Missed")
        
        **🔧 Supported Status Values:**
        - ✅ Completed: "Done", "Complete", "Completed"
        - ❌ Not Done: "Not Done", "NotDone", "Incomplete", "Missed"
        """)
    
    with tab3:
        st.markdown("""
        ### 🚀 Advanced Features:
        
        **🧠 Smart Analysis:**
        - Automatic consecutive day detection (accounts for weekends)
        - Priority classification based on task type and duration
        - Advanced data cleaning and validation
        
        **📊 Priority System:**
        - 🔴 **Critical**: Safety/compliance tasks or 5+ days missed
        - 🟠 **High**: Important tasks or 3+ days missed  
        - 🟡 **Medium**: 2+ days missed
        - 🟢 **Low**: Single day missed
        
        **📈 Reporting Features:**
        - Interactive charts and visualizations
        - Detailed summary statistics
        - Employee performance breakdown
        - Multiple export formats (CSV, Excel, Action Plans)
        
        **🔧 Error Handling:**
        - Comprehensive data validation
        - Automatic data cleaning
        - Detailed error and warning messages
        - Multiple date format support
        """)
    
    with tab4:
        st.markdown("""
        ### ❓ Common Issues & Solutions:
        
        **📁 File Upload Issues:**
        - Ensure file is in .xlsx or .xls format
        - Check file size (must be under 200MB)
        - Verify all required columns are present
        
        **📊 Data Format Issues:**
        - Date formats: Use YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY
        - Status values: Use "Done" or "Not Done" (case insensitive)
        - Remove empty rows and columns
        
        **🔍 Analysis Issues:**
        - If no results appear, check if any tasks are marked "Not Done"
        - Verify employee and task names are consistent
        - Ensure dates are valid and properly formatted
        
        **💡 Best Practices:**
        - Test with sample data first
        - Keep employee names consistent across entries
        - Use clear, descriptive task names
        - Regularly backup your data before processing
        """)

if __name__ == "__main__":
    main()