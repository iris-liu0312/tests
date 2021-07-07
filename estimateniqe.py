import shutil
import os

import numpy as np
import scipy.misc
import scipy.io
import scipy.ndimage
import skimage.io
import skvideo.measure
import skvideo.utils


# from https://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
def matlab_style_gauss2D(shape=(7, 7), sigma=7 / 6):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m, n = [(ss - 1.) / 2. for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    h = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


# computes mean instead of extracting features
def mean_on_patches(img, patch_size):
    h, w = img.shape
    patch_size = np.int(patch_size)
    patches = []
    for j in range(0, h - patch_size + 1, patch_size):
        for i in range(0, w - patch_size + 1, patch_size):
            patch = img[j:j + patch_size, i:i + patch_size]
            patches.append(patch)

    patches = np.array(patches)

    patch_mean = []
    for p in patches:
        patch_mean.append(np.mean(p))
    patch_mean = np.array(patch_mean)

    return patch_mean


# implemented from https://github.com/utlive/niqe/blob/main/estimatemodelparam.m
def estimate_model_param(folder_path, block_size_row=96, block_size_col=96, sharp_threshold=0.75):
    """Estimates model parameters for Naturalness Image Quality Evaluator. [#f1]_

        Input a folder of pristine images and save parameters to a mat file.

        Parameters
        ----------
        folder_path : str
            Folder containing the pristine images.
        block_size_row : int
            Height of the blocks in to which image is divided
        block_size_col : int
            Width of the blocks in to which image is divided
        sharp_threshold : float
            The sharpness threshold level

        Returns
        -------
        mu_prisparam : float
            mean of multivariate Gaussian model
        cov_prisparam : float
            covariance of multivariate Gaussian model

        References
        ----------
        .. [#f1] Mittal, Anish, Rajiv Soundararajan, and Alan C. Bovik.
        "Making a 'completely blind' image quality analyzer."
        IEEE Signal Processing Letters 20.3 (2013): 209-212.

        """

    # ---------------------------------------------------------------
    # Find names of images in the folder
    current = os.getcwd()
    os.chdir(folder_path)
    names = os.listdir(os.getcwd())
    os.chdir(current)

    # Number of features: 18 features at each scale
    feat_num = 18

    # ---------------------------------------------------------------
    # Make the directory for storing the features
    if os.path.isdir('local_features'):
        shutil.rmtree('local_features')
    os.mkdir('local_features')

    # ---------------------------------------------------------------
    # Compute pristine image features
    for i in range(0, len(names)):
        im = skimage.io.imread(f'{folder_path}/{names[i]}', as_gray=True)
        row, col = im.shape
        block_row_num = row // block_size_row
        block_col_num = col // block_size_col
        im = im[:(block_row_num * block_size_row + 1), :(block_col_num * block_size_col + 1)]
        window = matlab_style_gauss2D()
        window = window / sum(sum(window))

        mu = scipy.ndimage.correlate(im, window, mode='nearest')
        mu_sg = mu * mu
        sigma = np.sqrt(abs(scipy.ndimage.correlate(im * im, window, mode='nearest') - mu_sg))
        struct_dis = np.array(im - mu) / (sigma + 1)
        feat = skvideo.measure.extract_on_patches(struct_dis, 96)
        x, y = feat.shape
        feat = np.reshape(feat, (feat_num, int(x * y / feat_num))).transpose()
        sharpness = mean_on_patches(sigma, 96)

        mdic = {"feat": feat, "sharpness": sharpness}
        scipy.io.savemat(f'local_features/local{i}.mat', mdic)

    # ----------------------------------------------
    # Load pristine image features
    pris_param = 0
    current = os.getcwd()
    os.chdir('local_features')
    names = os.listdir(os.getcwd())
    os.chdir(current)
    for i in range(0, len(names)):
        # Load the features and select the only features
        data = scipy.io.loadmat(f'local_features/{names[i]}')
        sharpness = data['sharpness']
        feat = data['feat']
        threshold = sharp_threshold * np.amax(sharpness)
        feat = feat[(sharpness > threshold).flatten(), :]
        if i == 0:
            pris_param = feat
        else:
            pris_param = np.vstack((pris_param, feat))

    # ----------------------------------------------
    # shrink pris_param to (36,18) via averaging
    step = pris_param.shape[0] / 36
    pris_param_s = np.add.reduceat(pris_param.astype(float), np.arange(0, pris_param.shape[0], step).astype(int))
    pris_param_s = np.divide(pris_param_s, step)

    # Compute model parameters
    mu = np.nanmean(pris_param)
    cov = np.ma.cov(pris_param_s)
    # ----------------------------------------------
    # Save features in the mat file and clean up
    mdic = {"pop_mu": mu, "pop_cov": cov}
    scipy.io.savemat('niqe_fitted_parameters.mat', mdic)
    shutil.rmtree('local_features')
    return mu, cov


def fit_niqe(input_video_data, model_path):
    """Computes Naturalness Image Quality Evaluator. [#f1]_

    Input a video of any quality and get back its distance frame-by-frame
    from naturalness.

    Parameters
    ----------
    input_video_data : ndarray
        Input video, ndarray of dimension (T, M, N, C), (T, M, N), (M, N, C), or (M, N),
        where T is the number of frames, M is the height, N is width,
        and C is number of channels. Here C is only allowed to be 1.
    model_path : str
        Path to model parameters, ie. the mat file

    Returns
    -------
    niqe_array : ndarray
        The niqe results, ndarray of dimension (T,), where T
        is the number of frames

    References
    ----------
    .. [#f1] Mittal, Anish, Rajiv Soundararajan, and Alan C. Bovik.
    "Making a 'completely blind' image quality analyzer."
    IEEE Signal Processing Letters 20.3 (2013): 209-212.

    """
    # cache
    patch_size = 96

    params = scipy.io.loadmat(model_path)
    pop_mu = np.ravel(params["pop_mu"])
    pop_cov = params["pop_cov"]

    # load the training data
    input_video_data = skvideo.utils.vshape(input_video_data)

    T, M, N, C = input_video_data.shape

    assert C == 1, "niqe called with videos containing %d channels. Please supply only the luminance channel" % (C,)
    assert M > (
            patch_size * 2 + 1), "niqe called with small frame size, " \
                                 "requires > 192x192 resolution video using current training parameters"
    assert N > (
            patch_size * 2 + 1), "niqe called with small frame size, " \
                                 "requires > 192x192 resolution video using current training parameters"

    niqe_scores = np.zeros(T, dtype=np.float32)

    for t in range(T):
        feats = skvideo.measure.get_patches_test_features(input_video_data[t, :, :, 0], patch_size)
        sample_mu = np.mean(feats, axis=0)
        sample_cov = np.cov(feats.T)

        X = sample_mu - pop_mu
        cov_mat = ((pop_cov + sample_cov) / 2.0)
        pinv_mat = scipy.linalg.pinv(cov_mat)
        niqe_scores[t] = np.sqrt(np.dot(np.dot(X, pinv_mat), X))

    return niqe_scores
