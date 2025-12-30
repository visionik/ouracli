"""LLM help documentation for OuraCLI."""


def show_llm_help() -> str:
    """Return comprehensive usage guide for LLMs."""
    return """# OuraCLI Usage Guide for LLMs

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

All commands (except `personal_info`) accept a date range argument with flexible formats:

### Supported Formats
- `today` - Current day
- `yesterday` - Previous day
- `N days` - Last N days (e.g., `7 days`, `30 days`)
- `N weeks` - Last N weeks (e.g., `2 weeks`)
- `N months` - Last N months (e.g., `1 month`)
- `YYYY-MM-DD` - Specific single day
- `YYYY-MM-DD N days` - N days starting from specific date (e.g., `2025-12-01 28 days`)
- `YYYY-MM-DD N weeks` - N weeks starting from specific date
- `YYYY-MM-DD N months` - N months starting from specific date

### Examples
```bash
ouracli activity today
ouracli sleep 7 days
ouracli heartrate 2025-12-15
ouracli activity "2025-12-01 28 days"
```

## Output Formats

All commands support multiple output formats via flags (only one can be used at a time):

- `--tree` (default) - Human-readable tree structure
- `--json` - Raw JSON data
- `--markdown` - Markdown formatted output with charts
- `--html` - Interactive HTML with Chart.js visualizations
- `--dataframe` - Pandas DataFrame format

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
- Using date ranges (e.g., "YYYY-MM-DD 2 days") is more reliable
- When querying specific dates, consider adding a buffer day

### Readiness Contributors Data
⚠️ **IMPORTANT**: The `contributors.resting_heart_rate` field in readiness data is a
**SCORE (0-100)**, NOT an actual BPM measurement. This score indicates how your RHR
compares to your baseline:
- Low score (e.g., 19) = RHR is elevated vs. baseline (negative readiness impact)
- High score (e.g., 95) = RHR is optimal vs. baseline (positive readiness impact)
- Actual BPM values are found in the heartrate command's time-series data
- Example: A readiness score of 19 might correspond to an actual RHR of 65 bpm (still normal)

Do NOT interpret these contributor scores as actual heart rate measurements when analyzing
health metrics.

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

3. **Raw Data Export**:
   ```bash
   ouracli heartrate 2025-12-15 --json > hr_data.json
   ```

4. **Multi-Day Report**:
   ```bash
   ouracli all "7 days" --by-day --html > weekly_report.html
   ```

## Command Examples by Use Case

### Sleep Analysis
```bash
ouracli sleep 7 days --tree          # Quick overview
ouracli sleep 30 days --html > sleep_report.html
```

### Heart Rate Monitoring
```bash
ouracli heartrate today --tree       # ASCII chart
ouracli heartrate 2025-12-15 --html > hr_detailed.html
```

### Activity Tracking
```bash
ouracli activity today --tree        # Today's activity
ouracli activity "2025-12-01 7 days" --html > week_activity.html
```

### Comprehensive Health Report
```bash
ouracli all "30 days" --by-day --html > monthly_health.html
```

## Tips for Using with Shell Commands

### Pipe to Tools
```bash
ouracli activity today --json | jq '.[]'
ouracli sleep 7 days --json | python3 -c "import sys, json; ..."
```

### Save and Open
```bash
ouracli heartrate today --html > /tmp/hr.html && open /tmp/hr.html
```

## Error Handling

- If a date query returns no data, try a broader date range
- Check that the Oura Ring has synced recent data
- Ensure `secrets/oura.env` contains valid PERSONAL_ACCESS_TOKEN
"""
