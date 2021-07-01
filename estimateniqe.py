import os
import shutil
import numpy as np
import skimage.io
import scipy.ndimage
import skvideo.measure
import skvideo.utils



# imresize lifted from scikit-video package
# scikit-image documentation https://scikit-image.org/docs/stable/genindex.html
# numpy to python http://mathesaurus.sourceforge.net/matlab-numpy.html
# code in question https://github.com/utlive/niqe/blob/main/estimatemodelparam.m
# os package
# https://www.freecodecamp.org/news/python-list-files-in-a-directory-guide-listdir-vs-system-ls-explained-with-examples/
# matlab : is 1-indexing + inclusive


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


def estimate_model_param(folder_path, block_size_row=96, block_size_col=96,
                         block_row_overlap=0, block_col_overlap=0, sharp_threshold=0.75):
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
        block_row_overlap : int
            Amount of vertical overlap between blocks
        block_col_overlap : int
            Amount of horizontal overlap between blocks
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
        .. [#f1] Mittal, Anish, Rajiv Soundararajan, and Alan C. Bovik. "Making a 'completely blind' image quality analyzer." IEEE Signal Processing Letters 20.3 (2013): 209-212.

        """
    # Example call
    #
    # [mu_prisparam cov_prisparam] = estimatemodelparam('pristine', 96, 96, 0, 0, 0.75);

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
    if os.path.isdir('local_risquee_prisfeatures'):
        shutil.rmtree('local_risquee_prisfeatures')
    os.mkdir('local_risquee_prisfeatures')
    # ---------------------------------------------------------------
    # Compute pristine image features
    for i in range(0, len(names)):
        print(i)
        im = skimage.io.imread(f'{folder_path}/{names[i]}', as_gray=True)
        row, col = im.shape
        block_row_num = row // block_size_row
        block_col_num = col // block_size_col
        im = im[:(block_row_num * block_size_row + 1), :(block_col_num * block_size_col + 1)]
        window = matlab_style_gauss2D()
        window = window / sum(sum(window))
        scale_num = 2
        # warning('off')
        feat = np.array(0)
        sharpness = 0

        for scale in range(0, scale_num):
            mu = scipy.ndimage.correlate(im, window, mode='nearest')
            mu_sg = mu * mu
            sigma = np.sqrt(abs(scipy.ndimage.correlate(im*im, window, mode='nearest') - mu_sg))
            struct_dis = np.array(im - mu) / (sigma + 1)
            feat_scale = skvideo.measure.extract_on_patches(struct_dis, 96)
            feat_scale = np.reshape(feat_scale, (feat_num, feat_scale.shape[0]*feat_scale.shape[1]/feat_num))
            print(feat_scale.shape)
            # feat_scale = reshape(feat_scale, [feat_num, .size(feat_scale, 1) * size(feat_scale, 2) / feat_num]);
            # feat_scale = feat_scale';
            #
            if scale == 0:
                sharpness = np.array(np.mean(sigma))
                print(sharpness)
                # sharpness = blkproc(sigma, [blocksizerow, blocksizecol], [blockrowoverlap, blockcoloverlap],
                #             @computemean);
                # compute mean of every value in array A
                # sharpness = sharpness(:);
                pass
            feat = np.append(feat, feat_scale)
            print(feat.shape)
            im = skvideo.utils.image.imresize(im, 0.5)
            break
        scipy.io.savemat(f'local_risquee_prisfeatures/prisfeatures_local{i}.mat', feat, sharpness)
        break

    # ----------------------------------------------
    # Load pristine image features
    prisparam = []
    current = os.getcwd()
    os.chdir('local_risquee_prisfeatures')
    names = os.listdir(os.getcwd())
    os.chdir(current)
    for i in range(0, len(names)):
        # Load the features and select the only features
        scipy.io.loadmat(f'local_risquee_prisfeatures/{names[i]}')
        # IX = find(sharpness(:) > sh_th * max(sharpness(:)));
        # feat = feat(IX,:);
        prisparam = np.hstack(prisparam, feat)
        break

    # ----------------------------------------------
    # Compute model parameters
    mu_prisparam = np.nanmean(prisparam)
    cov_prisparam = np.ma.cov(prisparam)

    # ----------------------------------------------
    # Save features in the mat file
    scipy.io.savemat('modelparameters_new.mat', mu_prisparam, cov_prisparam)
    return mu_prisparam, cov_prisparam
