# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse

from isaaclab.app import AppLauncher


def add_app_launcher_args(parser: argparse.ArgumentParser) -> None:
    """IsaacLab's launcher flags, plus the 2.x ``--headless`` flag RoboLab's docs still use.

    IsaacLab 3.0 runs headless by default (``--viz kit`` opens a viewer) and no longer registers
    ``--headless`` / ``--enable_cameras`` / ``--rendering_mode``, so scripts that call
    ``parser.parse_args()`` would reject ``--headless``. After launch, ``args.headless`` holds the
    resolved value either way (the launcher writes it back into the namespace).
    """
    AppLauncher.add_app_launcher_args(parser)
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without a viewer. The default on IsaacLab 3.0 (pass --viz kit for a viewer); "
        "kept for compatibility.",
    )
