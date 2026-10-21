# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Guard the eval runner's argparse wiring against launcher-flag collisions.

The per-policy runners build their parser as::

    add_common_eval_args(parser)
    add_app_launcher_args(parser)  # robolab.core.utils.launcher_utils

argparse raises if two calls declare the same flag. This never shows up in the
other tests because they drive ``AppLauncher`` directly rather than through the
runner's parser — so it's asserted explicitly here.
"""

import argparse

from robolab.core.utils.launcher_utils import add_app_launcher_args
from robolab.eval.runner import add_common_eval_args


def test_common_eval_args_do_not_collide_with_app_launcher():
    parser = argparse.ArgumentParser()
    add_common_eval_args(parser)
    # Must not raise: add_common_eval_args must not declare any launcher-owned flag.
    add_app_launcher_args(parser)

    dests = {action.dest for action in parser._actions}
    # run_evaluation() consumes all of these; `device` and `headless` come from the launcher
    # helper (IsaacLab 3.0 itself no longer registers --headless).
    for dest in ("renderer", "rendering_type", "enable_gt_state", "run_index_offset", "seed",
                 "device", "headless"):
        assert dest in dests


def test_headless_flag_is_accepted():
    # IsaacLab 3.0 runs headless by default; RoboLab's docs and scripts still pass --headless.
    parser = argparse.ArgumentParser()
    add_common_eval_args(parser)
    add_app_launcher_args(parser)

    assert parser.parse_args(["--headless"]).headless is True


def test_run_index_offset_defaults_to_zero_and_accepts_an_override():
    parser = argparse.ArgumentParser()
    add_common_eval_args(parser)

    assert parser.parse_args([]).run_index_offset == 0
    assert parser.parse_args(["--run-index-offset", "9"]).run_index_offset == 9


def test_seed_defaults_to_zero_and_accepts_an_override():
    parser = argparse.ArgumentParser()
    add_common_eval_args(parser)

    assert parser.parse_args([]).seed == 0
    assert parser.parse_args(["--seed", "1099"]).seed == 1099


def test_instruction_type_accepts_zero_one_or_multiple_fields():
    parser = argparse.ArgumentParser()
    add_common_eval_args(parser)

    assert parser.parse_args([]).instruction_type is None
    assert parser.parse_args(["--instruction-type", "vague"]).instruction_type == ["vague"]
    assert parser.parse_args(
        ["--instruction-type", "vague", "video"]
    ).instruction_type == ["vague", "video"]
