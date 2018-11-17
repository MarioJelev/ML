import numpy as np

import imageio
from sklearn import cluster
import random



def quantize(raster, n_colors):
    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = cluster.KMeans(n_clusters=n_colors)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    return quantized_raster

num_clusters = [5, 10, 12]
og_images = ['image4.jpg', 'image5.jpg', 'image1.jpg']
for image_name in og_images:
	raster = imageio.imread(image_name)
	k = random.choice(num_clusters)
	print ('Using K = ' + str(k))
	quantizedImage = quantize(raster, k)
	imageio.imsave('quantized_'+ image_name, quantizedImage);
	print ('Done compressing ' + image_name)