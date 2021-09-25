"""Command line client interface."""

# This file is part of uniquify.
# Copyright 2021 Dave Rogers <thedude@yukondude.com>.
# Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c",
    "--canonical-choice",
    default="shortest",
    show_default=True,
    type=click.Choice(
        ["first", "shortest", "youngest", "oldest"], case_sensitive=False
    ),
    help="When there are multiple identical files, choose one as the canonical file:"
    "first encountered, shortest path, most recently modified, oldest modification "
    "time",
)
@click.option(
    "-l",
    "--link-mode",
    default="soft",
    show_default=True,
    type=click.Choice(["none", "soft", "hard"], case_sensitive=False),
    help="If 'none' do not migrate identical files, otherwise use the chosen form of "
    "filesystem link between identical copies of the file and the canonical copy.",
)
@click.argument(
    "sourcepath",
    nargs=-1,
    required=True,
    type=click.Path(
        dir_okay=True, exists=True, file_okay=False, readable=True, resolve_path=True
    ),
)
@click.argument(
    "targetpath",
    nargs=1,
    type=click.Path(
        dir_okay=True,
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
        writable=True,
    ),
)
def main(**kwargs):
    """Migrate unique files from one or more source paths to a new target path root. The
    target path must be an empty directory."""
    print(kwargs)
