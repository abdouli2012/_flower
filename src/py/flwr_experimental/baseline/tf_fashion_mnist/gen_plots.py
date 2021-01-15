# Copyright 2020 Adap GmbH. All Rights Reserved.
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
"""Generate plots for Fashion-MNIST results."""


from typing import List, Tuple

import numpy as np
from flwr_experimental.baseline.plot import bar_chart, line_chart

RESULTS = {
    "fedavg-t10": [
        (0, 0.03759999945759773),
        (1, 0.03759999945759773),
        (2, 0.03759999945759773),
        (3, 0.03759999945759773),
        (4, 0.03759999945759773),
        (5, 0.03759999945759773),
        (6, 0.03759999945759773),
        (7, 0.03759999945759773),
        (8, 0.03759999945759773),
        (9, 0.03759999945759773),
        (10, 0.03759999945759773),
        (11, 0.03759999945759773),
        (12, 0.03759999945759773),
        (13, 0.03759999945759773),
        (14, 0.03759999945759773),
        (15, 0.03759999945759773),
        (16, 0.03759999945759773),
        (17, 0.03759999945759773),
        (18, 0.03759999945759773),
        (19, 0.03759999945759773),
        (20, 0.03759999945759773),
    ],
    "fedavg-t12": [
        (0, 0.03759999945759773),
        (1, 0.03759999945759773),
        (2, 0.03759999945759773),
        (3, 0.03759999945759773),
        (4, 0.03759999945759773),
        (5, 0.03759999945759773),
        (6, 0.03759999945759773),
        (7, 0.03759999945759773),
        (8, 0.03759999945759773),
        (9, 0.03759999945759773),
        (10, 0.03759999945759773),
        (11, 0.03759999945759773),
        (12, 0.03759999945759773),
        (13, 0.03759999945759773),
        (14, 0.03759999945759773),
        (15, 0.03759999945759773),
        (16, 0.03759999945759773),
        (17, 0.03759999945759773),
        (18, 0.03759999945759773),
        (19, 0.03759999945759773),
        (20, 0.03759999945759773),
    ],
    "fedavg-t14": [
        (0, 0.03759999945759773),
        (1, 0.03759999945759773),
        (2, 0.6743999719619751),
        (3, 0.6802999973297119),
        (4, 0.6802999973297119),
        (5, 0.6802999973297119),
        (6, 0.6802999973297119),
        (7, 0.7853999733924866),
        (8, 0.7853999733924866),
        (9, 0.7876999974250793),
        (10, 0.7642999887466431),
        (11, 0.8054999709129333),
        (12, 0.8181999921798706),
        (13, 0.8108999729156494),
        (14, 0.7907000184059143),
        (15, 0.763700008392334),
        (16, 0.8091999888420105),
        (17, 0.8296999931335449),
        (18, 0.8123999834060669),
        (19, 0.8123999834060669),
        (20, 0.8101999759674072),
    ],
    "fedavg-t16": [
        (0, 0.03759999945759773),
        (1, 0.7197999954223633),
        (2, 0.7720999717712402),
        (3, 0.7900999784469604),
        (4, 0.7811999917030334),
        (5, 0.7724000215530396),
        (6, 0.8023999929428101),
        (7, 0.8043000102043152),
        (8, 0.8230999708175659),
        (9, 0.8327999711036682),
        (10, 0.8299000263214111),
        (11, 0.8402000069618225),
        (12, 0.853600025177002),
        (13, 0.8370000123977661),
        (14, 0.83160001039505),
        (15, 0.8424000144004822),
        (16, 0.830299973487854),
        (17, 0.8476999998092651),
        (18, 0.8632000088691711),
        (19, 0.8636999726295471),
        (20, 0.8657000064849854),
    ],
    "fedfs-t10": [
        (0, 0.03759999945759773),
        (1, 0.7343000173568726),
        (2, 0.7664999961853027),
        (3, 0.7900000214576721),
        (4, 0.805899977684021),
        (5, 0.8237000107765198),
        (6, 0.8406999707221985),
        (7, 0.8263000249862671),
        (8, 0.8442999720573425),
        (9, 0.8564000129699707),
        (10, 0.8651999831199646),
        (11, 0.8375999927520752),
        (12, 0.8646000027656555),
        (13, 0.8669999837875366),
        (14, 0.861299991607666),
        (15, 0.8773999810218811),
        (16, 0.800599992275238),
        (17, 0.8676999807357788),
        (18, 0.8763999938964844),
        (19, 0.8695999979972839),
        (20, 0.873199999332428),
    ],
    "fedfs-t12": [
        (0, 0.03759999945759773),
        (1, 0.7153000235557556),
        (2, 0.7835999727249146),
        (3, 0.8083999752998352),
        (4, 0.816100001335144),
        (5, 0.8215000033378601),
        (6, 0.8429999947547913),
        (7, 0.8464000225067139),
        (8, 0.8603000044822693),
        (9, 0.8482999801635742),
        (10, 0.8450000286102295),
        (11, 0.866599977016449),
        (12, 0.863099992275238),
        (13, 0.8709999918937683),
        (14, 0.873199999332428),
        (15, 0.8701000213623047),
        (16, 0.8600000143051147),
        (17, 0.8766999840736389),
        (18, 0.8697999715805054),
        (19, 0.8795999884605408),
        (20, 0.8830999732017517),
    ],
    "fedfs-t14": [
        (0, 0.03759999945759773),
        (1, 0.7245000004768372),
        (2, 0.7972000241279602),
        (3, 0.8059999942779541),
        (4, 0.8252999782562256),
        (5, 0.8334000110626221),
        (6, 0.8560000061988831),
        (7, 0.8510000109672546),
        (8, 0.8650000095367432),
        (9, 0.8621000051498413),
        (10, 0.866599977016449),
        (11, 0.8615999817848206),
        (12, 0.8636999726295471),
        (13, 0.8740000128746033),
        (14, 0.866100013256073),
        (15, 0.867900013923645),
        (16, 0.83160001039505),
        (17, 0.8741999864578247),
        (18, 0.8736000061035156),
        (19, 0.8810999989509583),
        (20, 0.8762000203132629),
    ],
    "fedfs-t16": [
        (0, 0.03759999945759773),
        (1, 0.7476999759674072),
        (2, 0.7982000112533569),
        (3, 0.8276000022888184),
        (4, 0.8256999850273132),
        (5, 0.8312000036239624),
        (6, 0.8536999821662903),
        (7, 0.8483999967575073),
        (8, 0.85589998960495),
        (9, 0.8687000274658203),
        (10, 0.8664000034332275),
        (11, 0.8586999773979187),
        (12, 0.8662999868392944),
        (13, 0.8754000067710876),
        (14, 0.878600001335144),
        (15, 0.8763999938964844),
        (16, 0.748199999332428),
        (17, 0.8806999921798706),
        (18, 0.8794000148773193),
        (19, 0.8813999891281128),
        (20, 0.8708000183105469),
    ],
}

RESULTS_WALL_CLOCK_TIME = {
    "fedavg-14": 218.49,
    "fedfs-14": 61.16,
    "fedavg-16": 153.56,
    "fedfs-16": 66.84,
}


def accuracy_t10() -> None:
    """Generate plots."""
    lines = [
        ("FedAvg, t=10", RESULTS["fedavg-t10"]),
        ("FedFS, t=10", RESULTS["fedfs-t10"]),
    ]
    plot(lines, "fmnist-progress-t10")


def accuracy_t12() -> None:
    """Generate plots."""
    lines = [
        ("FedAvg, t=12", RESULTS["fedavg-t12"]),
        ("FedFS, t=12", RESULTS["fedfs-t12"]),
    ]
    plot(lines, "fmnist-progress-t12")


def accuracy_t14() -> None:
    """Generate plots."""
    lines = [
        ("FedAvg, t=14", RESULTS["fedavg-t14"]),
        ("FedFS, t=14", RESULTS["fedfs-t14"]),
    ]
    plot(lines, "fmnist-progress-t14")


def accuracy_t16() -> None:
    """Generate plots."""
    lines = [
        ("FedAvg, t=16", RESULTS["fedavg-t16"]),
        ("FedFS, t=16", RESULTS["fedfs-t16"]),
    ]
    plot(lines, "fmnist-progress-t16")


def accuracy_fedavg_vs_fedfs() -> None:
    """Comparision of FedAvg vs FedFS."""
    fedavg = [
        RESULTS["fedavg-t10"][-1][1],
        RESULTS["fedavg-t12"][-1][1],
        RESULTS["fedavg-t14"][-1][1],
        RESULTS["fedavg-t16"][-1][1],
    ]
    fedfs = [
        RESULTS["fedfs-t10"][-1][1],
        RESULTS["fedfs-t12"][-1][1],
        RESULTS["fedfs-t14"][-1][1],
        RESULTS["fedfs-t16"][-1][1],
    ]
    bar_chart(
        y_values=[
            np.array([x * 100 for x in fedavg]),
            np.array([x * 100 for x in fedfs]),
        ],
        bar_labels=["FedAvg", "FedFS"],
        x_label="Timeout",
        x_tick_labels=["T=10", "T=12", "T=14", "T=16"],
        y_label="Accuracy",
        filename="fmnist-accuracy_fedavg_vs_fedfs",
    )


def wall_clock_time_fedavg_vs_fedfs() -> None:
    """Comparision of FedAvg vs FedFS."""

    bar_chart(
        y_values=[
            np.array(
                [
                    RESULTS_WALL_CLOCK_TIME["fedavg-14"],
                    RESULTS_WALL_CLOCK_TIME["fedavg-16"],
                ]
            ),
            np.array(
                [
                    RESULTS_WALL_CLOCK_TIME["fedfs-t14"],
                    RESULTS_WALL_CLOCK_TIME["fedfs-16"],
                ]
            ),
        ],
        bar_labels=["FedAvg", "FedFS"],
        x_label="Timeout",
        x_tick_labels=["T=14", "T=16"],
        y_label="Completion time",
        filename="fmnist-time_fedavg_vs_fedfs",
    )


def plot(lines: List[Tuple[str, List[Tuple[int, float]]]], filename: str) -> None:
    """Plot a single line chart."""
    values = [np.array([x * 100 for _, x in val]) for _, val in lines]
    labels = [label for label, _ in lines]
    line_chart(
        values,
        labels,
        "Round",
        "Accuracy",
        filename=filename,
        y_floor=0,
        y_ceil=100,
    )


def main() -> None:
    """Call all plot functions."""
    accuracy_t10()
    accuracy_t12()
    accuracy_t14()
    accuracy_t16()
    accuracy_fedavg_vs_fedfs()
    wall_clock_time_fedavg_vs_fedfs()


if __name__ == "__main__":
    main()
