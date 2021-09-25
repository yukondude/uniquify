"""Source path file scanner."""

# This file is part of uniquify.
# Copyright 2021 Dave Rogers <thedude@yukondude.com>.
# Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from collections import namedtuple, defaultdict
import glob
import hashlib
import os
import os.path


FileInstance = namedtuple(
    "FileInstance", "encounter_no full_path relative_path file_name modified_timestamp"
)


def collect_file_hashes(source_paths):
    """Collect all of the files in the given paths into a dictionary keyed by their
    unique hash value."""
    collected_paths = defaultdict(list)
    encounter_no = 0

    for source_path in source_paths:
        for full_path in glob.iglob(source_path + "**/**", recursive=True):
            if not os.path.isfile(full_path):
                continue

            encounter_no += 1
            relative_path = os.path.relpath(full_path, source_path)
            file_name = os.path.basename(relative_path)
            modified_timestamp = os.path.getmtime(full_path)
            file_hash = hash_file(full_path)

            collected_paths[file_hash].append(
                FileInstance(
                    encounter_no,
                    full_path,
                    relative_path,
                    file_name,
                    modified_timestamp,
                )
            )

    return collected_paths


def hash_file(file_path):
    """Return the SHA512 hash of the given file in hex form."""
    sha512 = hashlib.sha512()
    buffer_size = 64 * 1024

    with open(file_path, "rb") as hashed_file:
        while True:
            data = hashed_file.read(buffer_size)

            if not data:
                break

            sha512.update(data)

    return sha512.hexdigest()


def uniquify(source_paths):
    """Implement the uniquify algorithm."""
    collect_file_hashes(source_paths)
