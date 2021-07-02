import estimateniqe
import scipy.io as sio

estimateniqe.estimate_model_param('pristine')
data = sio.loadmat('niqe_image_params.mat')
print(f"cov shape: {data['pop_cov'].shape}")