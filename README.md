# OuraCLI

CLI tool for accessing Oura Ring data.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ouracli

# Install dependencies
task py:install
```

## Configuration

Set up your Oura API personal access token:

```bash
cp secrets/oura.env.example secrets/oura.env
# Edit secrets/oura.env and add your token
```

## Usage

```bash
# Get daily activity data
ouracli activity --days 7

# Get sleep data for yesterday
ouracli sleep yesterday

# Get all data for today
ouracli all today --format json

# Available output formats: tree (default), json, dataframe, markdown
ouracli sleep today --format markdown
```

### Available Commands

- `activity` - Daily activity data
- `sleep` - Daily sleep data
- `readiness` - Daily readiness scores
- `heartrate` - Heart rate time series
- `workout` - Workout summaries
- `session` - Session data
- `spo2` - Daily SpO2 data
- `stress` - Daily stress data
- `personal-info` - Personal information
- `rest-mode` - Rest mode periods
- `all` - All available data

### Date Ranges

Flexible date range options:

- `today` - Current day
- `yesterday` - Previous day
- `1 day` or `1 days` - Today
- `2 days` - Today and yesterday
- `n days` - Last n days
- `n weeks` - Last n weeks
- `n months` - Last n months
- `YYYY-MM-DD` + period - Start date plus period (e.g., `2024-01-01 7 days`)

## Development

```bash
# Format code
task py:fmt

# Lint code
task py:lint

# Type check
task py:type

# Run tests
task test

# Run tests with coverage
task test:coverage

# Pre-commit checks
task check
```

## License

MIT
