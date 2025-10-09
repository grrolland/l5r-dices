# -*- coding: utf-8 -*-
import typer
from .roller import roll

app = typer.Typer()
app.command()(roll)

if __name__ == "__main__":
    app()
