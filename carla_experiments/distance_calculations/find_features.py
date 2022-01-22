import cv2
import numpy as np
import math
import json

def return_feature_vector(main_image_file, lesion_mask_file, details_file):

    with open(details_file, 'r') as infile:
        details =  json.load(infile)

    eps = 1.0
    return_features = np.zeros(9, dtype = float)

    image = cv2.imread(main_image_file, cv2.IMREAD_COLOR)

    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    L_img = np.zeros((image.shape[0], image.shape[1]))
    L_img[:, :] = image_lab[:, :, 0]


    lesion_mask = cv2.imread(lesion_mask_file, cv2.IMREAD_GRAYSCALE)
    Pmean, Pstd = compute_background_info(L_img, lesion_mask)

    assert Pmean.shape == L_img.shape
    assert Pstd.shape == L_img.shape

    lesion_masked = np.ma.masked_equal(lesion_mask, 0) # Ignore background
    image_masked = np.ma.array(L_img, mask = lesion_masked.mask)

    if not (image_masked.all() is np.ma.masked) :
    
        seg_area = details["shape"][0] * details["shape"][1]
        seg_mean = image_masked.mean()
        seg_min = image_masked.min()
        seg_max = image_masked.max()
        seg_std = image_masked.std()

        x,y,w,h = cv2.boundingRect(lesion_mask)
        cX = x + int(float(w)/2.0)
        cY = y + int(float(h)/2.0)

        bg_mean = Pmean[cY, cX]
        bg_std = Pstd[cY, cX]

        seg_contrast = seg_max - bg_mean
        seg_prop = seg_mean/(bg_mean + eps)

        if seg_mean < (bg_mean+bg_std) or seg_contrast < 0.15 :
            seg_constrast = 0.0
            seg_prop = 0.0

        return_features[0] = float(cX) / float(L_img.shape[0])
        return_features[1] = float(cY) / float(L_img.shape[1])
        return_features[2] = float(seg_min) / 255.0
        return_features[3] = float(seg_max) / 255.0
        return_features[4] = float(seg_mean) / 255.0
        return_features[5] = float(seg_area) / float(L_img.shape[0] * L_img.shape[1])
        return_features[6] = seg_std / 255.0
        return_features[7] = bg_mean / 255.0
        return_features[8] = seg_contrast / 255.0

    return return_features

def compute_background_info(image, lesion_mask, nrows = 25, ncols = 20):

    assert image.shape == lesion_mask.shape
    

    Pmean = np.zeros(image.shape, dtype = float)
    Pstd = np.zeros(image.shape, dtype = float)

    sub_size_row = math.ceil(float( image.shape[0]) / float(nrows))
    sub_size_col = math.ceil(float( image.shape[1]) / float(ncols))

    row_start = 0
    row_end = 0
    while row_end < image.shape[0] :

        row_end = row_start + sub_size_row
        if row_end > image.shape[0]:
            row_end = image.shape[0]

        col_start = 0
        col_end = 0
        while col_end < image.shape[1]:
            col_end = col_start + sub_size_col
            if col_end > image.shape[1]:
                col_end = image.shape[1]

            BG_frame = image[row_start : row_end, col_start : col_end]
            lesion_frame = lesion_mask[row_start : row_end, col_start : col_end]

            BG_frame = BG_frame.astype(float)
            lesion_frame = lesion_frame.astype(float)

            frame_masked = np.ma.masked_equal(lesion_frame, 255) # Ignoring the lesion regions

            if not (frame_masked.all() is np.ma.masked) :

                masked_image = np.ma.array(BG_frame, mask = frame_masked.mask)
                Pmean[row_start : row_end, col_start : col_end] = masked_image.mean()
                Pstd[row_start : row_end, col_start : col_end] = masked_image.std()

            col_start += sub_size_col
        row_start += sub_size_row

    return Pmean, Pstd

def calculate_dist(seg_feature,mem_feature):
    seg_feature = seg_feature[2:]
    mem_feature = mem_feature[2:]
    dist_ = math.sqrt((0.05*((seg_feature[0]-mem_feature[0])**2)+0.05*((seg_feature[1]-mem_feature[1])**2)+0.1*((seg_feature[2]-mem_feature[2])**2) \
                +0.4*((seg_feature[3]-mem_feature[3])**2)**2+0.1*((seg_feature[4]-mem_feature[4])**2)+0.1*((seg_feature[5]-mem_feature[5])**2) \
                +0.2*((seg_feature[6]-mem_feature[6])**2)))
    return dist_

if __name__ == "__main__": 
    imagefile_1 = ["./temp/20_1.png", "./temp/20_1_mask.png", "./temp/20_1.json"]
    imagefile_2 = ["./temp/20_2.png", "./temp/20_2_mask.png", "./temp/20_2.json"]
    imagefile_3 = ["./temp/35_1.png", "./temp/35_1_mask.png", "./temp/35_1.json"]
    imagefile_4 = ["./temp/35_2.png", "./temp/35_2_mask.png", "./temp/35_2.json"]
    imagefile_5 = ["./temp/60_1.png", "./temp/60_1_mask.png", "./temp/60_1.json"]

    features_1 = return_feature_vector(imagefile_1[0], imagefile_1[1], imagefile_1[2])
    features_2 = return_feature_vector(imagefile_2[0], imagefile_2[1], imagefile_2[2])
    features_3 = return_feature_vector(imagefile_3[0], imagefile_3[1], imagefile_3[2])
    features_4 = return_feature_vector(imagefile_4[0], imagefile_4[1], imagefile_4[2])
    features_5 = return_feature_vector(imagefile_5[0], imagefile_5[1], imagefile_5[2])

    print("Feature vector for image - ", imagefile_1[0], " is - ", features_1)
    print("Feature vector for image - ", imagefile_2[0], " is - ", features_2)
    print("Feature vector for image - ", imagefile_3[0], " is - ", features_3)
    print("Feature vector for image - ", imagefile_4[0], " is - ", features_4)
    print("Feature vector for image - ", imagefile_5[0], " is - ", features_5)
    print(calculate_dist(features_1,features_2))
    print(calculate_dist(features_3,features_4))
    print(calculate_dist(features_1,features_3))
    print(calculate_dist(features_2,features_4))
    print(calculate_dist(features_1,features_5))
