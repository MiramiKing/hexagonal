import argparse
import asyncio
from argparse import RawTextHelpFormatter

from app.bus import get_message_bus
from app.cli.cli import Cli

from .app import run_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HEXAGONAL', formatter_class=RawTextHelpFormatter)
    parser.add_argument('type', help='Choose type, "web" or "cli"')
    args = parser.parse_args()

    if args.type == 'cli':
        asyncio.run(Cli(get_message_bus()).ask_user())
    elif args.type == 'web':
        run_app()
