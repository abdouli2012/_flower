"""Handle basic dataset creation.

In case of PyTorch it should return dataloaders for your dataset (for both the clients
and the server). If you are using a custom dataset class, this module is the place to
define it. If your dataset requires to be downloaded (and this is not done
automatically -- e.g. as it is the case for many dataset in TorchVision) and
partitioned, please include all those functions and logic in the
`dataset_preparation.py` module. You can use all those functions from functions/methods
defined here of course.
"""
import os
import numpy as np
import tensorflow as tf
# import keras_cv


def load_selected_client_statistics(selected_client, alpha, dataset, total_clients):
    """Returns the amount of local examples for the selected client (referenced with a client_id)
    which are stored in a numpy array saved on disk.
    This could be done directly by doing len(ds.to_list()) but it's more expensive at run time."""

    path = os.path.join(dataset + "_mlb_dirichlet_train", str(total_clients), str(round(alpha, 2)),
                            "distribution_train.npy")

    # path = os.path.join(dataset+"_mlb_dirichlet_train_and_test", str(round(alpha, 2)), "distribution_train.npy")
    smpls_loaded = np.load(path)
    # print(smpls_loaded[selected_clients])
    local_examples_all_clients = np.sum(smpls_loaded, axis=1)
    # print(local_examples_all_clients)
    return local_examples_all_clients[selected_client]


class PaddedRandomCropCustom(tf.keras.layers.Layer):
    """ Custom keras layer to random crop the input image.
        Same as FedMLB paper.
    """

    def __init__(self, seed=None, height=32, width=32):
        super(PaddedRandomCropCustom, self).__init__()
        self.seed = seed
        self.height = height
        self.width = width

    def call(self, input_tensor, training=True):
        if training:
            input_tensor = tf.image.resize_with_crop_or_pad(image=input_tensor, target_height=self.height + 4,
                                                            target_width=self.width + 4)
            input_tensor = tf.image.random_crop(value=input_tensor, size=[self.height, self.width, 3],
                                                seed=self.seed)
            return input_tensor
        else:
            return input_tensor


class PaddedCenterCropCustom(tf.keras.layers.Layer):
    """ Custom keras layer to center crop the input image.
        Same as FedMLB paper.
    """

    def __init__(self, height=32, width=64, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.width = width

    def call(self, input_tensor):
        input_tensor = tf.image.resize_with_crop_or_pad(image=input_tensor,
                                                        target_height=self.height,
                                                        target_width=self.width)

        input_shape = tf.shape(input_tensor)
        h_diff = input_shape[0] - self.height
        w_diff = input_shape[1] - self.width

        h_start = tf.cast(h_diff / 2, tf.int32)
        w_start = tf.cast(w_diff / 2, tf.int32)
        return tf.image.crop_to_bounding_box(
            input_tensor, h_start, w_start, self.height, self.width
        )


def load_client_datasets_from_files(dataset, sampled_client, batch_size, total_clients=100, alpha=0.3, split="train", seed=None):
    """Loads the partition of the dataset for the sampled client (sampled client represents its client_id).
        Examples are preprocessed via normalization layer.
        Returns a batched dataset."""

    def element_fn_norm_cifar100(image, label):
        norm_layer = tf.keras.layers.Normalization(mean=[0.5071, 0.4865, 0.4409],
                                                   variance=[np.square(0.2673),
                                                             np.square(0.2564),
                                                             np.square(0.2762)])
        return norm_layer(tf.cast(image, tf.float32) / 255.0), label

    def element_fn_norm_tiny_imagenet(image, label):
        norm_layer = tf.keras.layers.Normalization(mean=[0.4802, 0.4481, 0.3975],
                                                   variance=[np.square(0.2770),
                                                             np.square(0.2691),
                                                             np.square(0.2821)])
        return norm_layer(tf.cast(image, tf.float32) / 255.0), tf.expand_dims(label, axis=-1)

    # transform images
    rotate = tf.keras.layers.RandomRotation(0.06, seed=seed)
    flip = tf.keras.layers.RandomFlip(mode="horizontal", seed=seed)

    if dataset not in ["tiny_imagenet"]:
        crop = PaddedRandomCropCustom(seed=seed)
    else:
        crop = PaddedRandomCropCustom(seed=seed, height=64, width=64)

    rotate_flip_crop = tf.keras.Sequential([
        rotate,
        crop,
        flip,
    ])

    center_crop = tf.keras.layers.CenterCrop(64, 64)

    def center_crop_data(image, label):
        return center_crop(image), label

    def transform_data(image, label):
        return rotate_flip_crop(image), label

    path = os.path.join(dataset + "_mlb_dirichlet_train", str(total_clients), str(round(alpha, 2)), split)

    loaded_ds = tf.data.Dataset.load(
        path=os.path.join(path, str(sampled_client)), element_spec=None, compression=None, reader_func=None
    )

    if dataset in ["cifar100"]:
        if split == "test":
            return loaded_ds.map(element_fn_norm_cifar100).batch(
                batch_size, drop_remainder=False)
        loaded_ds = loaded_ds.shuffle(buffer_size=1024, seed=seed)\
            .map(element_fn_norm_cifar100)\
            .map(transform_data)\
            .batch(batch_size, drop_remainder=False)
        loaded_ds = loaded_ds.prefetch(tf.data.AUTOTUNE)
        return loaded_ds
    else:
        # dataset in ["tiny_imagenet"]
        if split == "test":
            return loaded_ds.map(element_fn_norm_tiny_imagenet).map(center_crop_data).batch(
                batch_size, drop_remainder=False)
        loaded_ds = loaded_ds.shuffle(buffer_size=1024, seed=seed) \
            .map(element_fn_norm_tiny_imagenet).map(transform_data) \
            .batch(batch_size, drop_remainder=False)
        # batch_size, drop_remainder=False).map(element_fn_norm_tiny_imagenet)
        loaded_ds = loaded_ds.prefetch(tf.data.AUTOTUNE)
        return loaded_ds
