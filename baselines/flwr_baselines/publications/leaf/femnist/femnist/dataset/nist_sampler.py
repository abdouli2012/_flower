import math
import pathlib
from logging import INFO, WARN
from typing import Union

import pandas as pd
from flwr.common.logger import log

from femnist.dataset.dataset_utils import _create_samples_division_list


class NistSampler:
    """
    Attributes
    ----------
    _data_info_df: pd.DataFrame
        dataframe that hold the information about the files' location
        (path_by_writer,writer_id,hash,path_by_class,character,path)

    """
    def __init__(self, data_info_df: pd.DataFrame):
        self._data_info_df = data_info_df

    def sample(
        self, sampling_type: str, frac: float, n_clients: Union[int, None] = None, random_seed: int = None
    ) -> pd.DataFrame:
        # n_clients is not used when niid
        # The question is if that hold in memory
        if sampling_type == "iid":
            if n_clients is None:
                raise ValueError("n_clients can not be None for idd training")
            idd_data_info_df = self._data_info_df.sample(
                frac=frac, random_state=random_seed
            )
            # add client ids (todo: maybe better in the index)
            idd_data_info_df["client_id"] = _create_samples_division_list(
                idd_data_info_df.shape[0], n_clients, True
            )
            return idd_data_info_df
        elif sampling_type == "niid":
            if n_clients is not None:
                log(
                    WARN,
                    "The n_clinets is ignored in case of niid training. "
                    "The number of clients is equal to the number of unique writers",
                )
            # It uses the following sampling logic:
            # Take N users with their full data till it doesn't exceed the total number of data that can be used
            # Then take remaining M samples (from 1 or more users, probably only one) till the  total number of samples
            # is reached
            frac_samples = math.ceil(
                frac * self._data_info_df.shape[0]
            )  # make it consistent with pd.DatFrame.sample()
            niid_data_info_full = self._data_info_df.copy()
            writer_ids_to_cumsum = (
                niid_data_info_full.groupby("writer_id")
                .size()
                .sample(frac=1.0, random_state=random_seed)
                .cumsum()
            )
            writer_ids_to_consider_mask = writer_ids_to_cumsum < frac_samples
            partial_writer_id = writer_ids_to_consider_mask.idxmin()
            niid_data_info_full = niid_data_info_full.set_index(
                "writer_id", append=True
            )
            writer_ids_to_consider = writer_ids_to_consider_mask[
                writer_ids_to_consider_mask
            ].index.values
            niid_data_info = niid_data_info_full.loc[
                niid_data_info_full.index.get_level_values("writer_id").isin(
                    writer_ids_to_consider
                )
            ]
            # fill in remainder
            current_n_samples = niid_data_info.shape[0]
            missing_samples = frac_samples - current_n_samples
            partial_writer_samples = niid_data_info_full.loc[
                niid_data_info_full.index.get_level_values("writer_id")
                == partial_writer_id
            ].iloc[:missing_samples]

            niid_data_info = pd.concat([niid_data_info, partial_writer_samples], axis=0)
            return niid_data_info
        else:
            raise ValueError(
                f"The given sampling_type of sampling is not supported. Given: {sampling_type}"
            )


if __name__ == "__main__":
    df_info_path = pathlib.Path("../../data/processed/resized_images_to_labels.csv")
    df_info = pd.read_csv(df_info_path, index_col=0)
    sampler = NistSampler(df_info)
    sampled_data_info = sampler.sample("niid", 0.05, 100)
    sampled_data_info.to_csv("data/processed/niid_sampled_images_to_labels.csv")

    import matplotlib.pyplot as plt

    plt.figure()
    sampled_data_info.reset_index(drop=False)["writer_id"].value_counts().plot.hist()
    log(INFO, sampled_data_info.shape)
    # plt.show()
