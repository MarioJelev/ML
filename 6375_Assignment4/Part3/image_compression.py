import numpy as np
from scipy import linalg
import imageio

import random



def compress(image, numPc, totalComponents):
	# computing eigenvalues and eigenvectors of covariance matrix
	M = (image-np.mean(image.T,axis=1)).T 
	[latent,coeff] = linalg.eig(np.cov(M))

	# sorting the eigenvalues
	idx = np.argsort(latent) 
	idx = idx[::-1]
	# sorting eigenvectors according to the sorted eigenvalues
	coeff = coeff[:,idx]

	# remove extraneous components
	if numPc < totalComponents:
			coeff = coeff[:,range(numPc)]
	# move data to new space
	score = np.dot(coeff.T,M) 
	image_reconstr = np.dot(coeff,score).T+np.mean(image,axis=0)
	return image_reconstr

num_PC = [200, 100, 500]
og_images = ['image4.jpg', 'image5.jpg', 'image1.jpg']
for image_name in og_images:
	count_PC = random.choice(num_PC)
	raster = np.mean(imageio.imread(image_name), 2)
	totalPC = np.size(raster, axis = 1)
	print ('Total PC in image: ' + str(totalPC))
	compressedImage = compress(raster, count_PC, totalPC)
	print ('Using ' + str(count_PC) + ' principal components')
	imageio.imsave('compressed_'+ image_name, compressedImage);
	print ('Done compressing ' + image_name)