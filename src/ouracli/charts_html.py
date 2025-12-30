"""Chart.js configuration generation for HTML output."""

import json


def create_chartjs_heartrate_config(heartrate_data: list[dict], chart_id: str) -> str:
    """
    Create Chart.js configuration for heart rate data.

    Args:
        heartrate_data: List of dicts with 'timestamp' and 'bpm' keys
        chart_id: Unique ID for the chart

    Returns:
        JavaScript code to render the chart
    """
    from datetime import datetime

    if not heartrate_data:
        return ""

    # Get actual min/max from raw data for Y-axis range
    all_bpms: list[float] = [
        float(reading.get("bpm"))  # type: ignore[arg-type]
        for reading in heartrate_data
        if reading.get("bpm") is not None
    ]
    if not all_bpms:
        return ""

    actual_min: float = min(all_bpms) - 10  # Floor 10 BPM below minimum
    actual_max: float = max(all_bpms)

    # Create 288 buckets (24 hours * 12 = one bucket per 5 minutes)
    five_minute_buckets: list[list[float]] = [[] for _ in range(288)]

    for reading in heartrate_data:
        timestamp_str = reading.get("timestamp", "")
        bpm = reading.get("bpm")

        if timestamp_str and bpm is not None:
            try:
                dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                # Calculate total minutes since midnight
                total_minutes = dt.hour * 60 + dt.minute
                # Determine which 5-minute bucket (0-287)
                bucket_idx = total_minutes // 5
                if 0 <= bucket_idx < 288:
                    five_minute_buckets[bucket_idx].append(bpm)
            except (ValueError, AttributeError):
                continue

    # Calculate average BPM for each 5-minute bucket
    bucket_averages: list[float | None] = []
    for bucket in five_minute_buckets:
        if bucket:
            bucket_averages.append(sum(bucket) / len(bucket))
        else:
            bucket_averages.append(None)  # Use None for missing data

    # Create labels: show hour labels at hour boundaries, empty strings between
    labels = []
    for i in range(288):
        # Each hour has 12 buckets (60 min / 5 min)
        if i % 12 == 0:
            hour = i // 12
            labels.append(f"{hour:02d}")
        else:
            labels.append("")  # Empty label for non-hour buckets

    # Convert None to null and keep numbers as-is for Chart.js
    data_values = [round(v) if v is not None else None for v in bucket_averages]

    return f"""
    new Chart(document.getElementById('{chart_id}'), {{
        type: 'bar',
        data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
                label: 'BPM (5-min avg)',
                data: {json.dumps(data_values)},
                backgroundColor: 'rgba(76, 175, 80, 0.8)',
                borderColor: 'rgba(46, 125, 50, 1)',
                borderWidth: 0,
                barPercentage: 1.0,
                categoryPercentage: 1.0
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                title: {{
                    display: true,
                    text: '24-Hour Heart Rate (5-minute resolution)',
                    color: '#333',
                    font: {{
                        size: 16
                    }}
                }},
                tooltip: {{
                    callbacks: {{
                        title: function(context) {{
                            const idx = context[0].dataIndex;
                            const hour = Math.floor(idx / 12);
                            const minute = (idx % 12) * 5;
                            return hour.toString().padStart(2, '0') + ':' + minute.toString().padStart(2, '0');
                        }}
                    }}
                }}
            }},
            scales: {{
                y: {{
                    beginAtZero: false,
                    min: {actual_min},
                    max: {actual_max},
                    title: {{
                        display: true,
                        text: 'BPM',
                        color: '#666'
                    }},
                    ticks: {{
                        color: '#666'
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.1)'
                    }}
                }},
                x: {{
                    title: {{
                        display: true,
                        text: 'Hour',
                        color: '#666'
                    }},
                    ticks: {{
                        color: '#666',
                        autoSkip: false,
                        maxRotation: 0,
                        minRotation: 0
                    }},
                    grid: {{
                        color: function(context) {{
                            // Show grid lines only at hour boundaries
                            return context.index % 12 === 0 ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.05)';
                        }}
                    }}
                }}
            }}
        }}
    }});
    """


def create_chartjs_config(met_items: list[float], chart_id: str) -> str:
    """
    Create Chart.js configuration for MET activity data.

    Args:
        met_items: List of MET values (one per minute, typically 1440 items)
        chart_id: Unique ID for the chart

    Returns:
        JavaScript code to render the chart
    """
    # Group into 5-minute buckets (288 buckets = 24 hours * 12)
    five_minute_buckets = []
    for i in range(288):
        start_idx = i * 5  # Each bucket is 5 minutes
        end_idx = start_idx + 5
        if start_idx < len(met_items):
            bucket = met_items[start_idx:end_idx]
            if bucket:
                avg_met = sum(bucket) / len(bucket)
                five_minute_buckets.append(avg_met)
            else:
                five_minute_buckets.append(0)
        else:
            five_minute_buckets.append(0)

    # Create labels: show hour labels at hour boundaries, empty strings between
    labels = []
    for i in range(288):
        # Each hour has 12 buckets (60 min / 5 min)
        if i % 12 == 0:
            hour = i // 12
            labels.append(f"{hour:02d}")
        else:
            labels.append("")  # Empty label for non-hour buckets

    # Round to 2 decimal places for MET values
    data_values = [round(v, 2) for v in five_minute_buckets]

    return f"""
    new Chart(document.getElementById('{chart_id}'), {{
        type: 'bar',
        data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
                label: 'MET (5-min avg)',
                data: {json.dumps(data_values)},
                backgroundColor: 'rgba(76, 175, 80, 0.8)',
                borderColor: 'rgba(46, 125, 50, 1)',
                borderWidth: 0,
                barPercentage: 1.0,
                categoryPercentage: 1.0
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                title: {{
                    display: true,
                    text: '24-Hour MET Activity (5-minute resolution)',
                    color: '#333',
                    font: {{
                        size: 16
                    }}
                }},
                tooltip: {{
                    callbacks: {{
                        title: function(context) {{
                            const idx = context[0].dataIndex;
                            const hour = Math.floor(idx / 12);
                            const minute = (idx % 12) * 5;
                            return hour.toString().padStart(2, '0') + ':' + minute.toString().padStart(2, '0');
                        }}
                    }}
                }}
            }},
            scales: {{
                y: {{
                    beginAtZero: true,
                    max: 6,
                    title: {{
                        display: true,
                        text: 'MET',
                        color: '#666'
                    }},
                    ticks: {{
                        color: '#666'
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.1)'
                    }}
                }},
                x: {{
                    title: {{
                        display: true,
                        text: 'Hour',
                        color: '#666'
                    }},
                    ticks: {{
                        color: '#666',
                        autoSkip: false,
                        maxRotation: 0,
                        minRotation: 0
                    }},
                    grid: {{
                        color: function(context) {{
                            // Show grid lines only at hour boundaries
                            return context.index % 12 === 0 ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.05)';
                        }}
                    }}
                }}
            }}
        }}
    }});
    """
