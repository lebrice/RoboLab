# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Sequence

import torch


def resolve_env_ids(env, env_ids: torch.Tensor | Sequence[int] | slice | None) -> torch.Tensor:
    """Environment indices as a long tensor on the env's device.

    IsaacLab 3.0 passes ``slice(None)`` for "all envs" (``ManagerBasedEnv.reset()``, event and
    recorder terms), where 2.x passed ``None`` or index tensors.
    """
    if env_ids is None:
        env_ids = slice(None)
    if isinstance(env_ids, slice):
        return torch.arange(env.num_envs, device=env.device)[env_ids]
    return torch.as_tensor(env_ids, device=env.device).long()
