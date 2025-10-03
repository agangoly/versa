#!/usr/bin/env python3

# Copyright 2024 Jiatong Shi
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import logging

import numpy as np
import torch

try:
    import torchaudio
    import torchaudio.functional as F
    from torchaudio.pipelines import SQUIM_OBJECTIVE, SQUIM_SUBJECTIVE
except ImportError:
    logging.warning(
        "Import error. Please install pesq, pystoi, torchaudio for torch squim"
    )


def squim_metric(pred_x, gt_x, fs):
    """
    Reference:
    Kumar, Anurag, et al. “TorchAudio-Squim: Reference-less Speech Quality and Intelligibility measures in TorchAudio.”,
    ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2023
    https://pytorch.org/audio/main/tutorials/squim_tutorial.html

    """
    gt_x = torch.from_numpy(gt_x)
    pred_x = torch.from_numpy(pred_x)

    if fs != 16000:
        gt_x = F.resample(gt_x, fs, 16000)
        pred_x = F.resample(pred_x, fs, 16000)

    gt_x = gt_x.unsqueeze(0).float()
    pred_x = pred_x.unsqueeze(0).float()

    subjective_model = SQUIM_SUBJECTIVE.get_model()
    if torch.cuda.is_available():
        gt_x = gt_x.cuda()
        pred_x = pred_x.cuda()
        subjective_model = subjective_model.cuda()
    torch_squim_mos = subjective_model(pred_x, gt_x)

    return {"torch_squim_mos": torch_squim_mos.cpu().detach().numpy()[0]}


def squim_metric_no_ref(pred_x, fs):
    """
    Reference:
    Kumar, Anurag, et al. “TorchAudio-Squim: Reference-less Speech Quality and Intelligibility measures in TorchAudio.”,
    ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2023
    https://pytorch.org/audio/main/tutorials/squim_tutorial.html

    """
    pred_x = torch.from_numpy(pred_x)
    if fs != 16000:
        pred_x = F.resample(pred_x, fs, 16000)

    pred_x = pred_x.unsqueeze(0).float()

    objective_model = SQUIM_OBJECTIVE.get_model()
    if torch.cuda.is_available():
        pred_x = pred_x.cuda()
        objective_model = objective_model.cuda()
    torch_squim_stoi, torch_squim_pesq, torch_squim_si_sdr = objective_model(pred_x)

    return {
        "torch_squim_stoi": torch_squim_stoi.cpu().detach().numpy()[0],
        "torch_squim_pesq": torch_squim_pesq.cpu().detach().numpy()[0],
        "torch_squim_si_sdr": torch_squim_si_sdr.cpu().detach().numpy()[0],
    }


if __name__ == "__main__":
    a = np.random.random(16000)
    b = np.random.random(16000)
    scores = squim_metric(a, b, 16000)
    print(scores)
