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

from flower_benchmark.plot import bar_chart, line_chart

RESULTS = {
    "fn-c10-r40-fedfs-v1-16": [
        (0, 0.03759999945759773),
        (1, 0.7357000112533569),
        (2, 0.7964000105857849),
        (3, 0.8057000041007996),
        (4, 0.8197000026702881),
        (5, 0.8321999907493591),
        (6, 0.8583999872207642),
        (7, 0.8324999809265137),
        (8, 0.864300012588501),
        (9, 0.8565000295639038),
        (10, 0.8743000030517578),
        (11, 0.8575000166893005),
        (12, 0.8496999740600586),
        (13, 0.8644999861717224),
        (14, 0.8758999705314636),
        (15, 0.8762999773025513),
        (16, 0.8198999762535095),
        (17, 0.8725000023841858),
        (18, 0.882099986076355),
        (19, 0.8758999705314636),
        (20, 0.8791000247001648),
        (21, 0.8792999982833862),
        (22, 0.885699987411499),
        (23, 0.8748000264167786),
        (24, 0.8561000227928162),
        (25, 0.8564000129699707),
        (26, 0.8363999724388123),
        (27, 0.876800000667572),
        (28, 0.8805999755859375),
        (29, 0.8569999933242798),
        (30, 0.8654000163078308),
        (31, 0.8705999851226807),
        (32, 0.8468999862670898),
        (33, 0.887499988079071),
        (34, 0.8823000192642212),
        (35, 0.8806999921798706),
        (36, 0.8823000192642212),
        (37, 0.8889999985694885),
        (38, 0.8101000189781189),
        (39, 0.8652999997138977),
        (40, 0.8766000270843506),
    ],
    "fn-c10-r40-fedfs-v0-16-16": [
        (0, 0.03759999945759773),
        (1, 0.7462000250816345),
        (2, 0.7843000292778015),
        (3, 0.7990999817848206),
        (4, 0.8149999976158142),
        (5, 0.8291000127792358),
        (6, 0.8413000106811523),
        (7, 0.8600999712944031),
        (8, 0.8511999845504761),
        (9, 0.8668000102043152),
        (10, 0.857699990272522),
        (11, 0.8673999905586243),
        (12, 0.8765000104904175),
        (13, 0.8773999810218811),
        (14, 0.8773999810218811),
        (15, 0.8562999963760376),
        (16, 0.8758999705314636),
        (17, 0.8729000091552734),
        (18, 0.8722000122070312),
        (19, 0.8356999754905701),
        (20, 0.8776999711990356),
        (21, 0.8845000267028809),
        (22, 0.8700000047683716),
        (23, 0.8766999840736389),
        (24, 0.8870999813079834),
        (25, 0.7976999878883362),
        (26, 0.876800000667572),
        (27, 0.8084999918937683),
        (28, 0.8737999796867371),
        (29, 0.8867999911308289),
        (30, 0.8797000050544739),
        (31, 0.8866999745368958),
        (32, 0.8795999884605408),
        (33, 0.8743000030517578),
        (34, 0.8881000280380249),
        (35, 0.8858000040054321),
        (36, 0.8881000280380249),
        (37, 0.8851000070571899),
        (38, 0.8403000235557556),
        (39, 0.8751000165939331),
        (40, 0.8812000155448914),
    ],
    "fn-c10-r40-fedfs-v0-16-08": [
        (0, 0.03759999945759773),
        (1, 0.644599974155426),
        (2, 0.7526000142097473),
        (3, 0.7882999777793884),
        (4, 0.8141000270843506),
        (5, 0.8335000276565552),
        (6, 0.8378999829292297),
        (7, 0.8572999835014343),
        (8, 0.86080002784729),
        (9, 0.84170001745224),
        (10, 0.8429999947547913),
        (11, 0.8489000201225281),
        (12, 0.858299970626831),
        (13, 0.8694999814033508),
        (14, 0.8694000244140625),
        (15, 0.8751999735832214),
        (16, 0.8722000122070312),
        (17, 0.8736000061035156),
        (18, 0.8744000196456909),
        (19, 0.8763999938964844),
        (20, 0.8431000113487244),
        (21, 0.8564000129699707),
        (22, 0.869700014591217),
        (23, 0.873199999332428),
        (24, 0.8788999915122986),
        (25, 0.8726000189781189),
        (26, 0.8784999847412109),
        (27, 0.8777999877929688),
        (28, 0.8776000142097473),
        (29, 0.8830000162124634),
        (30, 0.8838000297546387),
        (31, 0.873199999332428),
        (32, 0.8822000026702881),
        (33, 0.8835999965667725),
        (34, 0.8826000094413757),
        (35, 0.8847000002861023),
        (36, 0.8835999965667725),
        (37, 0.7781000137329102),
        (38, 0.8820000290870667),
        (39, 0.8762000203132629),
        (40, 0.8736000061035156),
    ],
    "fn-c10-r40-fedavg-16": [
        (0, 0.03759999945759773),
        (1, 0.6743000149726868),
        (2, 0.7746000289916992),
        (3, 0.7752000093460083),
        (4, 0.7994999885559082),
        (5, 0.8137000203132629),
        (6, 0.8341000080108643),
        (7, 0.822700023651123),
        (8, 0.822700023651123),
        (9, 0.8327999711036682),
        (10, 0.8264999985694885),
        (11, 0.8608999848365784),
        (12, 0.8526999950408936),
        (13, 0.859000027179718),
        (14, 0.8611000180244446),
        (15, 0.8482999801635742),
        (16, 0.8560000061988831),
        (17, 0.8414000272750854),
        (18, 0.8305000066757202),
        (19, 0.8445000052452087),
        (20, 0.8525999784469604),
        (21, 0.8528000116348267),
        (22, 0.8544999957084656),
        (23, 0.8572999835014343),
        (24, 0.8547000288963318),
        (25, 0.8582000136375427),
        (26, 0.8501999974250793),
        (27, 0.8741999864578247),
        (28, 0.8605999946594238),
        (29, 0.8578000068664551),
        (30, 0.8578000068664551),
        (31, 0.8598999977111816),
        (32, 0.8450999855995178),
        (33, 0.85589998960495),
        (34, 0.8565999865531921),
        (35, 0.8582000136375427),
        (36, 0.8547999858856201),
        (37, 0.8608999848365784),
        (38, 0.8503000140190125),
        (39, 0.8677999973297119),
        (40, 0.8535000085830688),
    ],
}


def accuracy_fn_c10() -> None:
    """Generate plots."""
    lines = [
        ("FedFSv1, c=10, t_max=16", RESULTS["fn-c10-r40-fedfs-v1-16"]),
        ("FedFSv0, c=10, t=16/16", RESULTS["fn-c10-r40-fedfs-v0-16-16"]),
        ("FedFSv0, c=10, t=16/08", RESULTS["fn-c10-r40-fedfs-v0-16-08"]),
        ("FedAvg, c=10, t=16", RESULTS["fn-c10-r40-fedavg-16"]),
    ]
    plot(lines, "fmnist-fn-progress-c10")


# def accuracy_fn_c50() -> None:
#     """Generate plots."""
#     lines = [
#     ]
#     plot(lines, "fmnist-fn-progress-c50")


def plot(lines: List[Tuple[str, List[Tuple[int, float]]]], filename: str) -> None:
    """Plot a single line chart."""
    values = [np.array([x * 100 for _, x in val]) for _, val in lines]
    labels = [label for label, _ in lines]
    line_chart(
        values, labels, "Round", "Accuracy", filename=filename, y_floor=60, y_ceil=100,
    )


def main() -> None:
    """Call all plot functions."""
    accuracy_fn_c10()
    # accuracy_fn_c50()


if __name__ == "__main__":
    main()
