# OuraCLI Usage Guide for LLMs

## Overview
ouracli is a CLI tool for accessing Oura Ring health data. It provides
multiple commands for different data types and supports various output
formats.

## Setup Requirements

### Authentication
ouracli requires an Oura Personal Access Token in the environment variable
PERSONAL_ACCESS_TOKEN to access the API.

**Obtain a token**: Visit https://cloud.ouraring.com/personal-access-tokens

**Set the token** using one of these methods (checked in order):

1. **Environment variable** (recommended for CI/CD, Docker):
   ```bash
   export PERSONAL_ACCESS_TOKEN=your_token_here
   ```

2. **Local project file** (recommended for development):
   - Create `secrets/oura.env` in your project directory
   - Add: `PERSONAL_ACCESS_TOKEN=your_token_here`

3. **Home directory file** (recommended for personal use across projects):
   - Create `~/.secrets/oura.env`
   - Add: `PERSONAL_ACCESS_TOKEN=your_token_here`

Without a valid token, all commands will fail with an authentication error.

## Available Commands

### Data Retrieval Commands
- `activity` - Daily activity data (steps, MET values, calories)
- `sleep` - Daily sleep data (stages, efficiency, heart rate)
- `readiness` - Daily readiness scores
- `heartrate` - Time-series heart rate data
- `spo2` - Daily blood oxygen data
- `stress` - Daily stress data
- `workout` - Workout sessions
- `session` - Activity sessions
- `tag` - User-added tags
- `rest_mode` - Rest mode periods
- `personal_info` - User profile information
- `all` - All available data types

## Date Range Specification

All commands (except `personal_info`) accept a date range argument with flexible formats.

### ✅ SUPPORTED DATE FORMATS

#### Single Date (No Quotes Needed)
```bash
ouracli activity 2025-12-25
ouracli sleep today
ouracli heartrate yesterday
```

#### Relative Ranges (From Today Backwards)
```bash
ouracli activity "7 days"      # Last 7 days including today
ouracli sleep "30 days"        # Last 30 days
ouracli readiness "2 weeks"    # Last 2 weeks
ouracli stress "1 month"       # Last month
```

#### Date + Duration (From Specific Date Forward)
```bash
ouracli activity "2025-12-01 28 days"    # 28 days starting Dec 1
ouracli sleep "2025-09-23 7 days"        # Week starting Sept 23
ouracli heartrate "2025-12-15 2 weeks"   # 2 weeks from Dec 15
```

**⚠️ IMPORTANT**: Use quotes when the date range contains spaces!

### ❌ UNSUPPORTED DATE FORMATS (Common LLM Mistakes)

These formats will **FAIL** - do NOT use them:

```bash
# ❌ Two separate date arguments
ouracli activity 2025-09-23 2025-09-30
# Error: "Got unexpected extra argument (2025-09-30)"

# ❌ "to" syntax
ouracli activity "2025-09-23 to 2025-09-30"
# Error: "Invalid date specification"

# ❌ Range operator syntax
ouracli activity "2025-09-23..2025-09-30"
# Error: "Invalid date specification"

# ❌ Separate flag options
ouracli activity --start-date 2025-09-23 --end-date 2025-09-30
# Error: "No such option: --start-date"

# ❌ Relative past syntax
ouracli activity "3 months ago"
# Error: "Invalid date specification"
```

### 🔧 Converting Date Ranges for LLMs

If you need data between two specific dates:

**Step 1**: Calculate the number of days between dates
```
Example: Sept 23 to Sept 30 = 7 days (inclusive)
         Dec 1 to Dec 31 = 30 days (inclusive)
```

**Step 2**: Use the "date + duration" format
```bash
# ✅ CORRECT: To get data from Sept 23 to Sept 30
ouracli activity "2025-09-23 7 days"

# ✅ CORRECT: To get all of December 2025
ouracli activity "2025-12-01 30 days"
```

**For "X months ago" queries**:
```bash
# ❌ WRONG: ouracli activity "3 months ago"

# ✅ CORRECT: Calculate exact date first
# If today is 2025-12-30, 3 months ago is ~2025-09-30
ouracli activity "2025-09-30 7 days"
```

### 📋 Date Format Examples

```bash
# Single day
ouracli activity 2025-12-25
ouracli sleep today

# Last N days/weeks/months (from today)
ouracli activity "7 days"
ouracli sleep "2 weeks"
ouracli readiness "30 days"

# Specific date ranges
ouracli activity "2025-12-01 28 days"     # All of December (if 28-31 days)
ouracli sleep "2025-09-23 7 days"         # One week from Sept 23
ouracli heartrate "2025-12-15 2 weeks"    # Two weeks from Dec 15
```

## Output Formats

All commands support multiple output formats via flags (only one can be used at a time):

- `--tree` (default) - Human-readable tree structure
- `--json` - Raw JSON data (⚠️ **RECOMMENDED for LLMs**)
- `--markdown` - Markdown formatted output with charts
- `--html` - Interactive HTML with Chart.js visualizations
- `--dataframe` - Pandas DataFrame format

### ⚠️ LLM Best Practice: Always Use --json

```bash
# ✅ RECOMMENDED for programmatic analysis
ouracli activity "7 days" --json

# ❌ NOT RECOMMENDED for parsing
ouracli activity "7 days" --tree
```

### Examples
```bash
ouracli activity today --json
ouracli heartrate 2025-12-15 --html > heartrate.html
ouracli activity "2025-12-01 7 days" --markdown
```

## Special Features

### Activity Data (MET Charts)
- HTML format includes interactive 5-minute resolution bar charts (288 bars per day)
- Shows detailed activity patterns throughout the day
- Hourly labels (00-23) on X-axis
- Example: `ouracli activity "2025-12-01 28 days" --html > activity.html`

### Heart Rate Data
- HTML format includes interactive 5-minute resolution charts
- Tree format includes ASCII/Braille bar charts with Y-axis labels
- Dynamic Y-axis range (10 BPM below minimum to actual maximum)
- Example: `ouracli heartrate 2025-12-15 --html > hr.html`

### All Data Command
- `--by-day` (default) - Group all data types by day
- `--by-method` - Group by data type (activity, sleep, etc.)
- Example: `ouracli all "7 days" --by-day --html`

## Important Notes for LLMs

### Oura API Date Behavior
- The Oura API may have timezone-related quirks
- Single-day queries sometimes return empty results
- Using date ranges (e.g., "YYYY-MM-DD 2 days") is more reliable than single dates
- When querying specific dates, consider adding a buffer day

### Readiness Contributors Data
⚠️ **IMPORTANT**: The `contributors.resting_heart_rate` field in readiness data is a
**SCORE (0-100)**, NOT an actual BPM measurement. This score indicates how your RHR
compares to your baseline:
- Low score (e.g., 19, 47) = RHR is elevated vs. baseline (negative readiness impact)
- High score (e.g., 95, 100) = RHR is optimal vs. baseline (positive readiness impact)
- Actual BPM values are found in the heartrate command's time-series data
- Example: A readiness score of 47 might correspond to an actual RHR of 65-70 bpm (still normal range)

**Do NOT interpret these contributor scores as actual heart rate measurements when analyzing
health metrics.**

### Output Redirection
- HTML and Markdown outputs are best saved to files:
  ```bash
  ouracli activity today --html > output.html
  open output.html  # macOS
  ```

### Common Workflows

1. **Quick Data Check**:
   ```bash
   ouracli activity today --tree
   ```

2. **Detailed Analysis**:
   ```bash
   ouracli activity "2025-12-01 28 days" --html > dec_activity.html
   open dec_activity.html
   ```

3. **Raw Data Export for LLM Analysis**:
   ```bash
   ouracli all "7 days" --json
   ouracli heartrate 2025-12-15 --json
   ```

4. **Multi-Day Report**:
   ```bash
   ouracli all "7 days" --by-day --html > weekly_report.html
   ```

## Command Examples by Use Case

### Sleep Analysis
```bash
ouracli sleep "7 days" --json           # Recommended for LLMs
ouracli sleep "30 days" --html > sleep_report.html
```

### Heart Rate Monitoring
```bash
ouracli heartrate today --tree          # Quick ASCII chart
ouracli heartrate "2025-12-15 1 days" --json  # Single day data
```

### Activity Tracking
```bash
ouracli activity today --json           # Today's activity
ouracli activity "2025-12-01 7 days" --html > week_activity.html
```

### Comprehensive Health Report
```bash
ouracli all "30 days" --json            # All data for analysis
ouracli all "30 days" --by-day --html > monthly_health.html
```

## Troubleshooting Guide for LLMs

### Error: "Got unexpected extra argument"
**Cause**: You used two separate date arguments instead of one date range argument

```bash
# ❌ WRONG
ouracli activity 2025-09-23 2025-09-30

# ✅ CORRECT - Calculate days (30-23 = 7) and use:
ouracli activity "2025-09-23 7 days"
```

### Error: "Invalid date specification"
**Cause**: You used unsupported syntax like "to", "..", or relative expressions

```bash
# ❌ WRONG
ouracli activity "2025-09-23 to 2025-09-30"
ouracli activity "3 months ago"

# ✅ CORRECT
ouracli activity "2025-09-23 7 days"
ouracli activity "2025-09-30 7 days"  # Calculate exact date for "3 months ago"
```

### Error: "No such option: --start-date"
**Cause**: You tried to use flag-based date specification

```bash
# ❌ WRONG
ouracli activity --start-date 2025-09-23 --end-date 2025-09-30

# ✅ CORRECT
ouracli activity "2025-09-23 7 days"
```

### No Data Returned
**Causes**:
1. Ring hasn't synced recently
2. Date is outside available data range
3. Single-day query hitting API timezone issues

**Solutions**:
```bash
# If single day fails, try adding buffer
ouracli activity "2025-12-25 2 days" --json

# Use broader range
ouracli activity "7 days" --json
```

## Tips for Using with Shell Commands

### Pipe to Tools
```bash
ouracli activity today --json | jq '.[]'
ouracli sleep "7 days" --json | python3 -m json.tool
```

### Save and Open
```bash
ouracli heartrate today --html > /tmp/hr.html && open /tmp/hr.html
```

## Quick Reference Card

| Task | Command |
|------|---------|
| Today's activity | `ouracli activity today --json` |
| Last week's sleep | `ouracli sleep "7 days" --json` |
| Specific date range | `ouracli activity "2025-12-01 30 days" --json` |
| All data types | `ouracli all "7 days" --json` |
| Heart rate chart | `ouracli heartrate today --html > hr.html` |
| Compare periods | Run two queries with different date ranges |

## Error Handling

- If a date query returns no data, try a broader date range
- Check that the Oura Ring has synced recent data
- Ensure `secrets/oura.env` or environment contains valid PERSONAL_ACCESS_TOKEN
- When in doubt about date formats, use "7 days" or similar relative ranges
