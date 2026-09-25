from __future__ import annotations

import os
import shlex
from collections.abc import Iterable
from contextlib import AbstractContextManager, nullcontext
from typing import Any

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

THEME = Theme(
    {
        "agentctl.brand": "bold bright_cyan",
        "agentctl.success": "bold bright_green",
        "agentctl.error": "bold bright_red",
        "agentctl.warning": "bold yellow",
        "agentctl.info": "bright_cyan",
        "agentctl.muted": "dim",
        "agentctl.path": "bright_blue",
        "agentctl.command": "bold white",
    }
)

_console = Console(theme=THEME, highlight=False)
_error_console = Console(theme=THEME, highlight=False, stderr=True)
_animations_enabled = True


def console_options(*, no_color: bool, force_color: bool) -> dict[str, Any]:
    environment = dict(os.environ)
    if force_color:
        environment.pop("NO_COLOR", None)
    return {
        "force_terminal": True if force_color else False if no_color else None,
        "color_system": "standard" if force_color else None if no_color else "auto",
        "no_color": no_color,
        "_environ": environment,
    }


def configure(*, no_color: bool, force_color: bool, no_animations: bool) -> None:
    global _console, _error_console, _animations_enabled
    options = console_options(no_color=no_color, force_color=force_color)
    _console = Console(
        theme=THEME,
        highlight=False,
        **options,
    )
    _error_console = Console(
        theme=THEME,
        highlight=False,
        stderr=True,
        **options,
    )
    _animations_enabled = (
        not no_animations
        and _console.is_terminal
        and not os.environ.get("CI")
        and os.environ.get("TERM") != "dumb"
    )


def status(message: str) -> AbstractContextManager[Any]:
    if not _animations_enabled:
        return nullcontext()
    return _console.status(
        f"[agentctl.info]{message}[/agentctl.info]",
        spinner="dots12",
        spinner_style="agentctl.brand",
    )


def heading(title: str, subtitle: str | None = None) -> None:
    content: list[Text] = [Text(title, style="agentctl.brand")]
    if subtitle:
        content.append(Text(subtitle, style="agentctl.muted"))
    _console.print(Panel(Group(*content), border_style="bright_cyan", padding=(0, 1)))


def success(title: str, details: Iterable[tuple[str, str]] = ()) -> None:
    rows = list(details)
    body: list[Any] = [Text.assemble(("✓ ", "agentctl.success"), title)]
    if rows:
        table = Table.grid(padding=(0, 1))
        table.add_column(style="agentctl.muted", justify="right")
        table.add_column(style="agentctl.path")
        for label, value in rows:
            table.add_row(label, Text(value))
        body.append(table)
    _console.print(Panel(Group(*body), border_style="green", padding=(0, 1)))


def step(message: str) -> None:
    _console.print(Text.assemble(("› ", "agentctl.info"), message))


def command(argv: list[str]) -> None:
    _console.print(
        Text.assemble(
            ("› ", "agentctl.info"),
            ("Running ", "agentctl.muted"),
            (shlex.join(argv), "agentctl.command"),
        )
    )


def error(message: str) -> None:
    _error_console.print(
        Panel(
            Text.assemble(("✕ ", "agentctl.error"), message),
            title="[agentctl.error]agentctl[/agentctl.error]",
            border_style="red",
            padding=(0, 1),
        )
    )


def diagnostics_table(items: Iterable[Any], *, heading_text: str) -> None:
    rows = list(items)
    if not rows:
        success(heading_text)
        return

    table = Table(
        title=heading_text,
        title_style="agentctl.brand",
        header_style="bold",
        border_style="bright_black",
        show_lines=False,
        expand=True,
    )
    table.add_column("", width=2, no_wrap=True)
    table.add_column("Code", width=12, no_wrap=True)
    table.add_column("Location", ratio=2, style="agentctl.path")
    table.add_column("Finding", ratio=3)
    for item in rows:
        is_error = item.severity == "error"
        symbol = "✕" if is_error else "!"
        style = "agentctl.error" if is_error else "agentctl.warning"
        table.add_row(
            Text(symbol, style=style),
            Text(item.code, style=style),
            Text(item.path),
            Text(item.message),
        )
    _console.print(table)


def json_error(message: str) -> None:
    import json

    print(json.dumps({"ok": False, "error": message}, indent=2, sort_keys=True))
