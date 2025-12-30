"""CLI application for OuraCLI."""

from enum import Enum

import typer

from ouracli.client import OuraClient
from ouracli.date_parser import parse_date_range
from ouracli.formatters import format_output
from ouracli.llm_help import show_llm_help

app = typer.Typer(
    help="CLI tool for accessing Oura Ring data",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def llmhelp_callback(value: bool) -> None:
    """Callback for --llmhelp flag."""
    if value:
        typer.echo(show_llm_help())
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    llmhelp: bool = typer.Option(
        False,
        "--llmhelp",
        callback=llmhelp_callback,
        is_eager=True,
        help="Show comprehensive usage guide for LLMs/agents and exit.",
    ),
) -> None:
    """CLI tool for accessing Oura Ring data."""
    # If no command was invoked, show help
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


class OutputFormat(str, Enum):
    """Output format options."""

    TREE = "tree"
    JSON = "json"
    DATAFRAME = "dataframe"
    MARKDOWN = "markdown"
    HTML = "html"


def get_output_format(
    json_flag: bool, tree_flag: bool, markdown_flag: bool, dataframe_flag: bool, html_flag: bool
) -> str:
    """Determine output format from flags. Tree is default."""
    format_flags = [
        (json_flag, "json"),
        (tree_flag, "tree"),
        (markdown_flag, "markdown"),
        (dataframe_flag, "dataframe"),
        (html_flag, "html"),
    ]
    active_flags = [fmt for flag, fmt in format_flags if flag]

    if len(active_flags) > 1:
        raise typer.BadParameter(
            "Only one format flag can be specified at a time: "
            "--json, --tree, --markdown, --dataframe, or --html"
        )

    return active_flags[0] if active_flags else "tree"


@app.command()
def activity(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get daily activity data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_daily_activity(start_date, end_date)
    result = data.get("data", [])
    # For markdown/html, wrap in dict with category for proper heading
    if output_format in ("markdown", "html") and isinstance(result, list):
        result = {"activity": result}
    output = format_output(result, output_format)
    typer.echo(output)


@app.command()
def sleep(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get daily sleep data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_daily_sleep(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def readiness(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get daily readiness data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_daily_readiness(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def spo2(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get daily SpO2 data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_daily_spo2(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def stress(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get daily stress data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_daily_stress(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def heartrate(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get heart rate time series data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    # Convert dates to datetime format for heartrate endpoint
    start_datetime = f"{start_date}T00:00:00"
    end_datetime = f"{end_date}T23:59:59"
    data = client.get_heartrate(start_datetime, end_datetime)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def workout(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get workout data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_workouts(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def session(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get session data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_sessions(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def tag(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get tag data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_tags(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def rest_mode(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get rest mode periods."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_rest_mode_periods(start_date, end_date)
    output = format_output(data.get("data", []), output_format)
    typer.echo(output)


@app.command()
def personal_info(
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
) -> None:
    """Get personal information."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    data = client.get_personal_info()
    output = format_output(data, output_format)
    typer.echo(output)


@app.command(name="all")
def get_all(
    date_range: str = typer.Argument("today", help="Date range (e.g., 'today', '7 days')"),
    json_flag: bool = typer.Option(False, "--json", help="Output as JSON"),
    tree_flag: bool = typer.Option(False, "--tree", help="Output as tree (default)"),
    markdown_flag: bool = typer.Option(False, "--markdown", help="Output as markdown"),
    dataframe_flag: bool = typer.Option(False, "--dataframe", help="Output as dataframe"),
    html_flag: bool = typer.Option(False, "--html", help="Output as HTML"),
    by_day_flag: bool = typer.Option(
        True,
        "--by-day/--by-method",
        help="Group data by day (default) or by method",
    ),
) -> None:
    """Get all available data."""
    output_format = get_output_format(
        json_flag, tree_flag, markdown_flag, dataframe_flag, html_flag
    )
    client = OuraClient()
    start_date, end_date = parse_date_range(date_range)
    data = client.get_all_data(start_date, end_date)
    output = format_output(data, output_format, by_day=by_day_flag)
    typer.echo(output)




def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
