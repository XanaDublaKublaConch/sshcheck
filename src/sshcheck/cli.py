from pathlib import Path

from typing_extensions import Annotated

# Dependency imports
import typer
from rich.terminal_theme import DIMMED_MONOKAI, SVG_EXPORT_THEME

# Other themes: MONOKAI, NIGHT_OWLISH
from rich.console import Console
from rich.table import Table
from yaml import safe_load

# Local imports
from .api import CheckedServer, PolicyStatus


def format_set(the_set: set, color="green") -> str:
    """
    Format the set as a colored string for rich console output
    :param the_set: A set of things
    :param color: How to color the things
    :return: A string, formatted richly
    """
    out = ", ".join(the_set)
    if "None" in out:
        color = "light_slate_grey"

    return f"[bold {color}]{out}[/bold {color}]"


def main(

    host: Annotated[str, typer.Argument(help="Hostname or IP address")],
    port: Annotated[
        int, typer.Option(help="Listening port for sshd service", min=1, max=65535)
    ] = 22,
    svg_export: Annotated[
        bool, typer.Option("--svg-export", help="Export to SVG?")
    ] = False,
    html_export: Annotated[
        bool, typer.Option("--html-export", help="Export to HTML?")
    ] = False,
    pdf_export: Annotated[
        bool, typer.Option("--pdf-export", help="Export to PDF?")
    ] = False,
    png_export: Annotated[
        bool, typer.Option("--png-export", help="Export to PNG?")
    ] = False,
):
    """
    Check the kex, hka, cipher, mac, and other stuff on the server against the policy
    :param host: ip or hostname
    :param port: listening port of the ssh server
    :param svg_export: export to svg
    :param html_export: export to html
    :param pdf_export: export to pdf
    :param png_export: export to png
    :return:
    """
    # Load in the policy
    with open("policy.yml", "r") as policy_file:
        ssh_policy = safe_load(policy_file)
    # Checkit
    svr = CheckedServer(hostname=host, port=port, policy=ssh_policy)
    svr.check_ssh()

    match svr.host_key_status:
        case PolicyStatus.APPROVED:
            color = "green"
        case PolicyStatus.CONTAINED:
            color = "red"
        case PolicyStatus.OTHER:
            color = "yellow"
        case PolicyStatus.UNAPPROVED:
            color = "red"
        case _:  # Could be None?
            color = "lightslategrey"

    # record = True allows rich to export captured prints to svg, html, etc.
    console = Console(record=True)
    table = Table(
        show_header=True,
        header_style="bold blue",
        title=f"Results for {svr.hostname}:{svr.port} ({svr.ip_address})",
        caption=f"Server sent us a host key in [bold {color}]{svr.host_key_status.name.lower()} {svr.host_key_type}[/bold {color}] format.",
        show_lines=True,
        title_style="bold white on deep_sky_blue2",
    )
    table.add_column("Type", style="dim")
    table.add_column("Policy: Approved")
    table.add_column("Policy: Contained")
    table.add_column("Policy: Override")
    table.add_column("Policy: BAD!")

    # Add the security findings foe each type
    for key in ["kex", "hka", "ciphers", "mac"]:
        err_dict: dict[str, set] = {f"Error {key}": {"No data found"}}
        result_dict: dict[str, set] = getattr(svr, key, err_dict)
        table.add_row(
            key.upper(),
            format_set(result_dict.get("approved")),
            format_set(result_dict.get("contained"), "red"),
            format_set(result_dict.get("unknown"), "yellow"),
            format_set(result_dict.get("bad"), "red"),
        )
    # Add the compression stuff. Rich tables don't support colspan, so fill with spaces
    table.add_row(
        "Compression\nAlgorithms",
        format_set(svr.compress, "light_slate_grey"),
        " ",  # Contained N/A
        " ",  # Unknown N/A
        " ",  # Bad N/A
    )
    console.print(table)
    if svg_export:
        filename = f"{svr.hostname}.svg"
        console.save_svg(filename, theme=SVG_EXPORT_THEME)
        console.print(f"[dim cyan]SVG report saved as {filename}.[/dim cyan]")
    if html_export:
        filename = f"{svr.hostname}.html"
        console.save_html(filename, theme=DIMMED_MONOKAI)

        console.print(f"[dim cyan]HTML report saved as {filename}[/dim cyan]")
    if pdf_export:
        try:
            import cairosvg

            filename = f"{svr.hostname}.pdf"
            console.save_svg("temp.svg")
            cairosvg.svg2pdf(url="temp.svg", write_to=filename)
            Path("temp.svg").unlink()
            console.print(f"[dim cyan]PDF file saved to {filename}[/dim cyan]")
        except ModuleNotFoundError:
            console.print("[bold red]cairosvg module must be installed to export PDF!")
    if png_export:
        try:
            import cairosvg

            filename = f"{svr.hostname}.png"
            console.save_svg("temp.svg")
            cairosvg.svg2png(url="temp.svg", write_to=filename)
            Path("temp.svg").unlink()
            console.print(f"[dim cyan]PNG file saved to {filename}[/dim cyan]")
        except ModuleNotFoundError:
            console.print("[bold red]cairosvg module must be installed to export PNG!")


def run_cli():
    typer.run(main)
