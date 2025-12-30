"""ASCII/Braille chart generation for terminal output."""


def create_heartrate_bar_chart_ascii(
    heartrate_data: list[dict], width: int = 72, height: int = 10
) -> str:
    """
    Create an ASCII bar chart from heart rate data using Braille characters.

    Args:
        heartrate_data: List of dicts with 'timestamp' and 'bpm' keys
        width: Width of chart in characters (default 72 = 144 buckets)
        height: Height of chart in characters (default 10)

    Returns:
        ASCII bar chart as string
    """
    if not heartrate_data:
        return "No heart rate data"

    # Convert irregular timestamp data to 10-minute buckets (144 total = 24 hours * 6)
    from datetime import datetime

    # Get actual min/max from raw data for Y-axis labels
    all_bpms: list[float] = [
        float(reading.get("bpm"))  # type: ignore[arg-type]
        for reading in heartrate_data
        if reading.get("bpm") is not None
    ]
    actual_min: float = (min(all_bpms) - 10) if all_bpms else 0.0
    actual_max: float = max(all_bpms) if all_bpms else 100.0

    # Create 144 buckets (24 hours * 6 = one bucket per 10 minutes)
    ten_minute_buckets: list[list[float]] = [[] for _ in range(144)]

    for reading in heartrate_data:
        timestamp_str = reading.get("timestamp", "")
        bpm = reading.get("bpm")

        if timestamp_str and bpm is not None:
            try:
                # Parse timestamp and calculate which 10-minute bucket it belongs to
                dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                # Calculate total minutes since midnight
                total_minutes = dt.hour * 60 + dt.minute
                # Determine which 10-minute bucket (0-143)
                bucket_idx = total_minutes // 10
                if 0 <= bucket_idx < 144:
                    ten_minute_buckets[bucket_idx].append(bpm)
            except (ValueError, AttributeError):
                continue

    # Calculate average BPM for each 10-minute bucket
    buckets = []
    for bucket in ten_minute_buckets:
        if bucket:
            buckets.append(sum(bucket) / len(bucket))
        else:
            buckets.append(0)

    return _create_ascii_bar_chart_from_buckets(
        buckets, width, height, "BPM", actual_min, actual_max
    )


def create_ascii_bar_chart(met_items: list[float], width: int = 72, height: int = 10) -> str:
    """
    Create an ASCII bar chart from MET data using Braille characters for higher resolution.

    Args:
        met_items: List of MET values (typically 1440 items for a full day)
        width: Width of chart in characters (default 72 = 144 buckets = 10 min/bucket)
        height: Height of chart in characters (default 10)

    Returns:
        ASCII bar chart as string
    """
    if not met_items:
        return "No MET data"

    # Group items into buckets - use 2x width since we'll pack 2 bars per character
    # 1440 items -> 144 buckets = 10 items per bucket (10 minutes each)
    num_buckets = width * 2
    bucket_size = len(met_items) // num_buckets
    if bucket_size == 0:
        bucket_size = 1

    buckets = []
    for i in range(0, len(met_items), bucket_size):
        bucket = met_items[i : i + bucket_size]
        if bucket:
            # Use max value in bucket for visualization
            buckets.append(max(bucket))

    # Ensure we have exactly 'num_buckets' buckets
    buckets = buckets[:num_buckets]

    return _create_ascii_bar_chart_from_buckets(buckets, width, height, "MET")


def _create_ascii_bar_chart_from_buckets(
    buckets: list[float],
    width: int,
    height: int,
    unit: str,
    actual_min: float | None = None,
    actual_max: float | None = None,
) -> str:
    """
    Internal function to create ASCII bar chart from pre-bucketed data.

    Args:
        buckets: List of values (should be width * 2 for dual-column packing)
        width: Width in characters
        height: Height in characters
        unit: Unit label (e.g., "MET" or "BPM")
        actual_min: Actual minimum value from source data (for Y-axis labels)
        actual_max: Actual maximum value from source data (for Y-axis labels)

    Returns:
        ASCII bar chart as string
    """
    # Braille patterns for vertical bars
    # Dots are arranged: 1,2,3,7 (left column), 4,5,6,8 (right column)
    #   1 • • 4
    #   2 • • 5
    #   3 • • 6
    #   7 • • 8
    # Bit positions: 0=1, 1=2, 2=3, 3=4, 4=5, 5=6, 6=7, 7=8
    braille_base = 0x2800

    # Left column patterns (dots 1,2,3,7) from bottom to top
    left_patterns = [
        0b00000000,  # 0: no dots
        0b01000000,  # 1: dot 7 (bit 6)
        0b01000100,  # 2: dots 3,7 (bits 2,6)
        0b01000110,  # 3: dots 2,3,7 (bits 1,2,6)
        0b01000111,  # 4: dots 1,2,3,7 (bits 0,1,2,6)
    ]

    # Right column patterns (dots 4,5,6,8) from bottom to top
    right_patterns = [
        0b00000000,  # 0: no dots
        0b10000000,  # 1: dot 8 (bit 7)
        0b10100000,  # 2: dots 6,8 (bits 5,7)
        0b10110000,  # 3: dots 5,6,8 (bits 4,5,7)
        0b10111000,  # 4: dots 4,5,6,8 (bits 3,4,5,7)
    ]

    # Find max value for scaling (use actual if provided, otherwise bucketed)
    max_val = actual_max if actual_max is not None else (max(buckets) if buckets else 1.0)
    if max_val == 0:
        max_val = 1.0

    # Find min value (use actual if provided, otherwise from non-zero buckets)
    if actual_min is not None:
        min_val = actual_min
    else:
        non_zero_vals = [v for v in buckets if v > 0]
        min_val = min(non_zero_vals) if non_zero_vals else 0

    # Each character has 4 dots of resolution, so total resolution is height * 4
    total_dots = height * 4

    # Calculate Y-axis labels (show at top, 3 midpoints, and bottom)
    # We'll show labels for rows 0, 2, 5, 7, 9 (for height=10)
    y_labels = {}
    label_rows = [0, 2, 5, 7, 9] if height >= 10 else [0, height // 2, height - 1]

    for row in label_rows:
        # Calculate value at this row (from top)
        # Row 0 = max, Row height-1 = min
        if row == 0:
            value_at_row = max_val
        elif row == height - 1:
            value_at_row = min_val
        else:
            value_at_row = max_val - (row / (height - 1)) * (max_val - min_val)
        y_labels[row] = f"{value_at_row:.0f}"

    # Find max label width for alignment
    max_label_width = max(len(label) for label in y_labels.values()) if y_labels else 0

    # Create chart lines from top to bottom
    lines = []
    for row in range(height):
        # Add Y-axis label if this row has one
        if row in y_labels:
            label = y_labels[row].rjust(max_label_width)
            line = f"{label} │ "
        else:
            line = " " * max_label_width + " │ "

        # Process buckets in pairs (left and right columns)
        for i in range(0, len(buckets), 2):
            left_val = buckets[i] if i < len(buckets) else 0
            right_val = buckets[i + 1] if i + 1 < len(buckets) else 0

            # Calculate dots for left bar (scale from min to max)
            value_range = max_val - min_val
            if value_range > 0 and left_val > 0:
                left_dots_filled = int(((left_val - min_val) / value_range) * total_dots)
            else:
                left_dots_filled = 0

            row_bottom = total_dots - (row + 1) * 4
            row_top = row_bottom + 4

            if left_dots_filled <= row_bottom:
                left_pattern = left_patterns[0]
            elif left_dots_filled >= row_top:
                left_pattern = left_patterns[4]
            else:
                dots_in_row = left_dots_filled - row_bottom
                left_pattern = left_patterns[dots_in_row]

            # Calculate dots for right bar (scale from min to max)
            if value_range > 0 and right_val > 0:
                right_dots_filled = int(((right_val - min_val) / value_range) * total_dots)
            else:
                right_dots_filled = 0

            if right_dots_filled <= row_bottom:
                right_pattern = right_patterns[0]
            elif right_dots_filled >= row_top:
                right_pattern = right_patterns[4]
            else:
                dots_in_row = right_dots_filled - row_bottom
                right_pattern = right_patterns[dots_in_row]

            # Combine left and right patterns
            combined_pattern = left_pattern | right_pattern
            char = chr(braille_base + combined_pattern)
            line += char
        lines.append(line)

    # Add a baseline with Y-axis alignment
    baseline = " " * max_label_width + " └" + "─" * width
    lines.append(baseline)

    # Add hour labels (0-23) with Y-axis alignment
    # Each hour = 6 buckets (60 min / 10 min per bucket)
    # With 2 buckets per character = 3 characters per hour
    # Build hour labels with proper spacing (each hour gets 3 chars)
    hour_parts = []
    for hour in range(24):
        if hour < 10:
            # Single digit: " X " (space, digit, space)
            hour_parts.append(f" {hour} ")
        else:
            # Double digit: "XX " (digit, digit, space)
            hour_parts.append(f"{hour} ")

    # Trim to exactly 72 characters and add Y-axis padding
    hour_line = " " * (max_label_width + 3) + "".join(hour_parts)[:width]
    lines.append(hour_line)

    return "\n".join(lines)
