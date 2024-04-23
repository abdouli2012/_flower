# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower command line interface `build` command."""

import hashlib
import os
import zipfile
from pathlib import Path
from typing import Optional

import jwt
import pathspec
import typer
from typing_extensions import Annotated

from .config_utils import validate_project_dir
from .utils import is_valid_project_name, prompt_text


# pylint: disable=too-many-locals
def build(
    directory: Annotated[
        Optional[Path],
        typer.Option(help="The Flower project directory to bundle into a FAB"),
    ] = None,
    sign: Annotated[bool, typer.Option(help="Flag to sign the FAB")] = False,
    key_path: Annotated[
        Optional[Path], typer.Option(help="Path to the secret key file for signing")
    ] = None,
) -> None:
    """Build a Flower project into a Flower App Bundle (FAB).

    You can run `flwr build` without any argument to bundle the current directory:

        `flwr build`

    You can also build a specific directory:

        `flwr build --directory ./projects/flower-hello-world`

    And finally, to sign the resulting `.fab` file, use the `--sign` argument:

        `flwr build --sign`

    Note that this will prompt the you for the private key to use for signing.
    """
    if directory is None:
        directory = Path.cwd()

    directory = directory.resolve()
    if not directory.is_dir():
        typer.secho(
            f"❌ The path {directory} is not a valid directory.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(code=1)

    if not is_valid_project_name(directory.name):
        typer.secho(
            f"❌ The project name {directory.name} is invalid, "
            "a valid project name must start with a letter or an underscore, "
            "and can only contain letters, digits, and underscores.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(code=1)

    conf = validate_project_dir(directory)
    if conf is None:
        raise typer.Exit(code=1)

    # Load .gitignore rules if present
    ignore_spec = _load_gitignore(directory)

    # Set the name of the zip file
    fab_filename = (
        f"{conf['project']['publisher']}"
        f"-{directory.name}"
        f"-{conf['project']['version']}.fab"
    )
    list_file_content = ""

    allowed_extensions = {".py", ".toml", ".md"}

    with zipfile.ZipFile(fab_filename, "w", zipfile.ZIP_DEFLATED) as fab_file:
        for root, _, files in os.walk(directory, topdown=True):
            # Filter directories and files based on .gitignore
            files = [
                f
                for f in files
                if not ignore_spec.match_file(Path(root) / f)
                and f != fab_filename
                and Path(f).suffix in allowed_extensions
            ]

            for file in files:
                file_path = Path(root) / file
                archive_path = file_path.relative_to(directory)
                fab_file.write(file_path, archive_path)

                # Calculate file info
                sha256_hash = _get_sha256_hash(file_path)
                file_size_bits = os.path.getsize(file_path) * 8  # size in bits
                list_file_content += f"{archive_path},{sha256_hash},{file_size_bits}\n"

        # Add CONTENT and CONTENT.jwt to the zip file
        fab_file.writestr(".info/CONTENT", list_file_content)

        # Optionally sign the CONTENT file
        if sign:
            if key_path is None:
                key_path = Path(
                    prompt_text(
                        "Enter the path to the secret key to sign the CONTENT file",
                        predicate=lambda result: Path(result) is not None,
                    )
                )
            try:
                with open(key_path) as key_file:
                    secret_key = key_file.read().strip()
            except Exception as err:
                typer.echo(f"Failed to read the secret key from file: {err}")
                raise typer.Exit(code=1) from err

            signed_token = _sign_content(list_file_content, secret_key)
            fab_file.writestr(".info/CONTENT.jwt", signed_token)

    typer.secho(
        f"🎊 Successfully built {fab_filename}.", fg=typer.colors.GREEN, bold=True
    )


def _get_sha256_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)  # Read in 64kB blocks
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def _load_gitignore(directory: Path) -> pathspec.PathSpec:
    """Load and parse .gitignore file, returning a pathspec."""
    gitignore_path = directory / ".gitignore"
    patterns = ["__pycache__/"]  # Default pattern
    if gitignore_path.exists():
        with open(gitignore_path, encoding="UTF-8") as file:
            patterns.extend(file.readlines())
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def _sign_content(content: str, secret_key: str) -> str:
    """Signs the content using JWT and returns the token."""
    payload = {"data": content}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
