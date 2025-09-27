# Daily Staff Report Review Agent

### App : 
         https://daily-staff-report-review-agent.streamlit.app/
         
## 📊 Overview
The Daily Staff Report Review Agent is a comprehensive Streamlit web application designed to analyze staff daily reports, detect missed tasks, and generate appropriate follow-up actions. This tool helps managers and supervisors efficiently identify performance issues and take corrective measures.

## 🚀 Features

### Core Functionality
- **Smart Task Analysis**: Automatically detects missed tasks and categorizes them
- **Follow-up Generation**: Creates "Follow-up" actions for single-day misses
- **Escalation Management**: Generates "Escalate" actions for consecutive missed days
- **Priority Classification**: Assigns priority levels based on task type and duration

### Advanced Features
- **Multiple File Format Support**: Handles both .xlsx and .xls Excel files
- **Data Validation**: Comprehensive validation with detailed error reporting
- **Interactive Visualizations**: Charts and graphs for better data insights
- **Export Options**: Multiple export formats (CSV, Excel, Action Plans)
- **Session Management**: Data persistence across interactions

### Priority System
- 🔴 **Critical**: Safety/compliance tasks or 5+ days missed
- 🟠 **High**: Important tasks or 3+ days missed
- 🟡 **Medium**: 2+ days missed
- 🟢 **Low**: Single day missed

## 📋 Requirements

### System Requirements
- Python 3.7+
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- XLRD

### Data Requirements
Your Excel file must contain these columns:

- **Employee**: Staff member name (text)
- **Task**: Task description (text)
- **Date**: Task date (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)
- **Status**: Task completion status ("Done", "Not Done", "Incomplete", "Missed")

## 🛠️ Installation

1. Clone or download the project files
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## 📖 Usage Guide

### Quick Start
1. **Choose Data Source**: Upload Excel file or use sample data
2. **Data Validation**: System automatically validates format
3. **Analysis**: Click "Analyze Reports" to process data
4. **Results**: View detailed results with priority levels
5. **Export**: Download results in preferred format

### Sample Data Format
| Employee      | Task              | Date       | Status    |
|---------------|-------------------|------------|-----------|
| John Smith    | Safety Check      | 2024-01-01 | Done      |
| Sarah Johnson | Report Submission | 2024-01-01 | Not Done  |
| John Smith    | Safety Check      | 2024-01-02 | Not Done  |

### Supported Status Values
- ✅ **Completed**: "Done", "Complete", "Completed"
- ❌ **Not Done**: "Not Done", "NotDone", "Incomplete", "Missed"

## 🏗️ Architecture

### Project Structure
```
streamlit_template1/
├── app.py                 # Main Streamlit application
├── report_processor.py    # Core analysis engine
├── sample_data.py         # Sample data generator
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── uploads/
    └── Candidate_Task_DailyReports.xlsx
```

### Key Components

1. **Main Application (app.py)**
   - User Interface: Streamlit-based web interface
   - Session Management: Data persistence across interactions
   - File Handling: Upload and processing of Excel files
   - Visualization: Interactive charts and graphs
   - Export Functions: Multiple download options

2. **Report Processor (report_processor.py)**
   - Data Validation: Comprehensive input validation
   - Analysis Engine: Core logic for detecting missed tasks
   - Priority Assignment: Smart priority classification
   - Error Handling: Robust error management and reporting

3. **Sample Data Generator (sample_data.py)**
   - Demo Data: Generates realistic sample data
   - Template Creation: Creates downloadable Excel templates
   - Testing Support: Provides data for application testing

## 📊 Analysis Logic

### Consecutive Day Detection
The system uses advanced logic to detect consecutive missed days:
- Accounts for weekends (allows up to 3-day gaps)
- Groups consecutive misses for escalation
- Handles different date formats automatically

### Priority Calculation
Priority is determined by:
- **Task Type**: Keywords like "safety", "compliance" increase priority
- **Duration**: Number of consecutive days missed
- **Business Impact**: Critical vs. routine tasks

### Action Generation
- **Single Miss**: Generates "Follow-up" action
- **Multiple Consecutive Days**: Generates "Escalate" action
- **Priority-based Sorting**: Orders results by urgency

## 📈 Output Reports

### Analysis Results Table
| Employee    | Task          | Date(s) Missed          | Action   | Priority | Days Missed |
|-------------|---------------|-------------------------|----------|----------|-------------|
| John Smith  | Safety Check  | 2024-01-01 to 2024-01-03 | Escalate | Critical | 3          |

### Summary Statistics
- Total Issues Found
- Employees Affected
- Tasks Affected
- Average Days Missed

### Action Breakdown
- Priority Distribution

### Export Options
- **CSV Export**: Simple tabular data
- **Excel Report**: Multi-sheet comprehensive report
- **Action Plan**: Ready-to-use task list for managers

## 🔧 Configuration

### Advanced Settings
- **Show Warnings**: Display data processing warnings
- **Show Visualizations**: Enable/disable charts
- **Auto-analyze**: Automatic analysis on file upload

### Customization Options
- Priority keywords can be modified in `report_processor.py`
- Consecutive day threshold can be adjusted
- Export formats can be extended

## 🚨 Error Handling

### Data Validation
- Missing required columns detection
- Invalid date format handling
- Empty or corrupted file management
- Duplicate entry removal

### Processing Errors
- Comprehensive error logging
- User-friendly error messages
- Debug information display
- Recovery suggestions

## 📊 Visualizations

### Available Charts
- **Action Distribution**: Pie chart showing Follow-up vs. Escalate
- **Priority Breakdown**: Bar chart of priority levels
- **Employee Performance**: Top employees with most issues

### Interactive Features
- Hover tooltips for detailed information
- Responsive design for different screen sizes
- Color-coded priority system

## 🔍 Troubleshooting

### Common Issues

#### File Upload Problems
**Issue**: "Missing optional dependency 'xlrd'"  
**Solution**: Install xlrd with `pip install xlrd`

#### Analysis Not Working
**Issue**: No results after clicking "Analyze Reports"  
**Solution**: Check if any tasks are marked as "Not Done"

#### Data Format Issues
**Issue**: Date parsing errors  
**Solution**: Use supported date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)

### Best Practices
- Test with sample data first
- Keep employee names consistent
- Use clear, descriptive task names
- Regular data backups before processing

## 🚀 Deployment

### Local Deployment
```
streamlit run app.py
```

### Cloud Deployment
The application can be deployed on:
- Streamlit Cloud

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a virtual environment
3. Install dependencies
4. Make your changes
5. Test thoroughly
6. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling
- Write unit tests for new features

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support
For support and questions:
- Create an issue in the repository
- Check the troubleshooting guide
- Review the documentation

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Core analysis functionality
- Excel file support
- Basic visualizations
- Export capabilities

### Planned Features
- Email notification integration
- Advanced filtering options
- Historical trend analysis
- Multi-language support

## 🏆 Acknowledgments
- Built with Streamlit for the web interface
- Pandas for data processing
- Plotly for interactive visualizations
- OpenPyXL and XLRD for Excel file handling
