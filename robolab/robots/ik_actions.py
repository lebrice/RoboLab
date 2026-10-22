# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import torch
from isaaclab.envs.mdp.actions.task_space_actions import DifferentialInverseKinematicsAction


class WxyzPoseDifferentialIKAction(DifferentialInverseKinematicsAction):
    """Differential IK whose absolute pose actions are (x, y, z, qw, qx, qy, qz).

    That is RoboLab's policy-facing quaternion order; IsaacLab 3.0's IK controller takes
    (x, y, z, qx, qy, qz, qw). ``raw_actions`` keeps what the policy sent.
    """

    def process_actions(self, actions: torch.Tensor):
        if self.action_dim != 7:  # Relative or position-only commands carry no quaternion.
            super().process_actions(actions)
            return
        super().process_actions(actions[:, [0, 1, 2, 4, 5, 6, 3]])
        self._raw_actions[:] = actions
