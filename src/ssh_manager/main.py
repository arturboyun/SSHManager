#!/usr/bin/env python3

import subprocess
from pathlib import Path
import typer

app = typer.Typer()


def parse_ssh_hosts(config_path: Path):
    """Парсит хосты из SSH config, исключая шаблоны"""
    hosts = []
    try:
        with config_path.open(encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("Host "):
                    parts = stripped.split()[1:]
                    for host in parts:
                        if any(c in host for c in "*?[]!"):
                            continue
                        hosts.append(host.strip())
    except UnicodeDecodeError:
        typer.echo(f"Ошибка чтения файла {config_path}: неверная кодировка.")
        raise typer.Exit(code=1)
    if not config_path.exists():
        typer.echo(f"Файл {config_path} не найден.")
        raise typer.Exit(code=1)

    hosts = parse_ssh_hosts(config_path)

    if not hosts:
        typer.echo("Не найдено ни одного хоста.")
    else:
        for h in hosts:
            typer.echo(h)


@app.command()
def con():
    """Выбрать и подключиться к хосту из ~/.ssh/config"""
    hosts = []
    config_path = Path.home() / ".ssh" / "config"
    try:
        with config_path.open(encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("Host "):
                    parts = stripped.split()[1:]
                    for host in parts:
                        if any(c in host for c in "*?[]!"):
                            continue
                        hosts.append(host.strip())
    except UnicodeDecodeError:
        typer.echo(f"Ошибка чтения файла {config_path}: неверная кодировка.")
        raise typer.Exit(code=1)

    typer.echo("Доступные хосты:", color=True)
    for i, h in enumerate(hosts, start=1):
        typer.echo(f"({i}) {h}")

    while True:
        selected_host = typer.prompt("Выберите хост", type=int)
        if selected_host < 1 or selected_host > len(hosts):
            typer.echo(
                f"[ERROR] Неверный выбор. Пожалуйста, выберите число от 1 до {len(hosts)}."
            )
            continue
        break

    host_to_connect = hosts[selected_host - 1]
    typer.echo(f"Подключение к {host_to_connect}...")
    subprocess.run(["ssh", host_to_connect])


def cli():
    app()
