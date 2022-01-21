from PIL import Image
import sys
import os
import numpy as np
from torchvision import transforms, datasets
import torch
import cv2
import time
from scipy.ndimage import rotate, shift
import json
import math
sys.path.append("./distance_calculations")
# print(sys.path)
import find_features
from pytorch_modified_msssim import ssim, ms_ssim, SSIM, MS_SSIM

def shift_image(input_PIL, shift = [3,3]):
    np_I = np.asarray(input_PIL)
    trans_I = np.zeros_like(np_I)
    shape = np_I.shape

    #print("Shape - ", np_I)

    row_low = max(shift[0], 0)
    row_high = min(shape[0] + shift[0], shape[0])

    col_low = max(shift[1], 0)
    col_high = min(shape[1] + shift[1], shape[1])

    for r in range(row_low, row_high):
        for c in range(col_low, col_high):
            trans_I[r, c] = np_I[r, c]

    # print("Output shape - ", trans_I.shape)
    return_image = Image.fromarray(np.uint8(trans_I))
    return return_image

#load memories saved in directory
def load_memory(memory_folder,size,device,shift_range=2,shift_delta=1,angle_range=30,angle_delta=2):
    memories=[]
    jsons = []
    for root, dirs, files in os.walk(memory_folder):
        dirs.sort(key=int)
        for file in files:
            if(file.endswith(".png") or file.endswith(".ppm") or file.endswith(".jpg") or file.endswith(".jpeg")):
                memories.append(os.path.join(root, file))
            if(file.endswith(".json")):
                jsons.append(os.path.join(root, file))
    memory_lists=[]
    memory_features=[]
    #print(len(memories))
    for memory,json_ in zip(memories,jsons):
        im = Image.open(memory)
        #image_lab = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2LAB)
        #im = np.zeros((image_lab.shape[0], image_lab.shape[1]))
        #im[:, :] = image_lab[:, :, 0]
        im = transforms.ToTensor()(im).to(device)
        memory_lists.append(im)
        memory_split=memory.split("/")
        f = open(json_)
        data = json.load(f)
        for i in data:
            label_=int(i["img"].split("/")[-2])
            if(float(i['dist'])==0.032):
                memory_label = label_
        mask_path="./mask"+"/"+str(memory_label)+"/"+memory_split[-1][:-4]+"_mask.png"
        json_path="./lesion_images"+"/"+str(memory_label)+"/"+memory_split[-1][:-4]+".json"
        mem_feature = return_feature_vector(memory,mask_path,json_path)
        memory_features.append(mem_feature[2:])
    memory_features=torch.tensor(memory_features,dtype=torch.float32).to(device)
    memory_lists=torch.stack(memory_lists, dim=0).to(device)
    print(memory_lists.shape)
    return memory_lists,memory_features

def read_json(path):
    path=path.split("/")
    path="./lesion_images"+"/"+path[-2]+"/"+path[-1][:-4]+".json"
    f = open(path)
    data = json.load(f)
    size= data["shape"][0]*data["shape"][1]
    return size
#compute distance between one memory and other images
def compute_distance(memory_idx,memory_path, solved_imgs_list, unsolved_imgs_list,saved_dict,threshold,device,unsolved=False,size=32,padding=False):
    if unsolved:
        imgs_list = unsolved_imgs_list.copy()
    else:
        imgs_list = solved_imgs_list.copy()
    x_list = []
    for path in imgs_list:
        im = np.array(Image.open(path))
        #image_lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
        #im = np.zeros((image_lab.shape[0], image_lab.shape[1]))
        #im[:, :] = image_lab[:, :, 0]
        #im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
        if padding:
            im = cv2.copyMakeBorder(im,10,10,10,10,cv2.BORDER_CONSTANT,value=[0,0,0])
        im = transforms.ToTensor()(im)
        x_list.append(im)

    if len(x_list)==0:
        return solved_imgs_list, unsolved_imgs_list, saved_dict
    x_list=torch.stack(x_list, dim=0).to(device)

    unsolved_imgs = []
    unsolved_imgs = np.array(unsolved_imgs)
    unsolved_imgs_list = unsolved_imgs_list.copy()

    for split in range(0,len(imgs_list),100):
        img_size=[]
        if (len(imgs_list) - split < 100):
            end_idx = len(imgs_list)
        else:
            end_idx = split + 100
        memory = np.array(Image.open(memory_path))
        #image_lab = cv2.cvtColor(memory, cv2.COLOR_BGR2LAB)
        #memory = np.zeros((memory.shape[0], memory.shape[1]))
        #memory[:, :] = image_lab[:, :, 0]
        #memory = cv2.normalize(memory,None, 0, 255, cv2.NORM_MINMAX)
        if padding:
            memory = cv2.copyMakeBorder(memory,10,10,10,10,cv2.BORDER_CONSTANT,value=[0,0,0])
        memory = transforms.ToTensor()(memory)
        memory_list = memory.repeat([end_idx-split,1,1,1]).to(device)
        memory_split=memory_path.split("/")
        mask_path="./mask"+"/"+memory_split[-2]+"/"+memory_split[-1][:-4]+"_mask.png"
        json_path="./lesion_images"+"/"+memory_split[-2]+"/"+memory_split[-1][:-4]+".json"
        mem_feature = return_feature_vector(memory_path,mask_path,json_path)
        mem_feature = mem_feature[2:]
        #mem_shape = torch.full((end_idx-split,1), read_json(memory_path),dtype=torch.float32).to(device)
        mem_shape = torch.tensor(mem_feature,dtype=torch.float32).to(device).repeat((end_idx-split,1))
        seg_dist=[]
        seg_features=[]
        for img_path in imgs_list[split:end_idx]:
            #img_size.append(read_json(img_path))
            img_path_=img_path.split("/")
            mask_path="./mask"+"/"+img_path_[-2]+"/"+img_path_[-1][:-4]+"_mask.png"
            json_path="./lesion_images"+"/"+img_path_[-2]+"/"+img_path_[-1][:-4]+".json"
            seg_feature = return_feature_vector(img_path,mask_path,json_path)
            seg_feature = seg_feature[2:]
            seg_features.append(seg_feature)
            #seg_dist.append(np.linalg.norm(seg_feature-mem_feature))
            #dist_ = math.sqrt((0.05*((seg_feature[0]-mem_feature[0])**2)+0.05*((seg_feature[1]-mem_feature[1])**2)+0.1*((seg_feature[2]-mem_feature[2])**2) \
            #    +0.4*((seg_feature[3]-mem_feature[3])**2)**2+0.1*((seg_feature[4]-mem_feature[4])**2)+0.1*((seg_feature[5]-mem_feature[5])**2) \
            #    +0.2*((seg_feature[6]-mem_feature[6])**2)))
            #seg_dist.append(dist_)

        seg_features = torch.tensor(seg_features,dtype=torch.float32).to(device)
        weight_vector = torch.tensor([0.05,0.05,0.1,0.4,0.1,0.1,0.2],dtype=torch.float32).to(device)
        seg_dist=torch.sum(weight_vector*(seg_features-mem_shape)*(seg_features-mem_shape),1)
        seg_dist = torch.squeeze(seg_dist).detach().cpu()
        #size_dist = torch.tanh(torch.div(torch.abs(mem_shape-img_shape),torch.min(mem_shape,img_shape))).detach().cpu()
        ssim_val = ssim(memory_list, x_list[split:end_idx], data_range=1, size_average=False).detach().cpu() # return (N,)
        add_dist = np.asarray(ssim_val+seg_dist)
        solved_list = (add_dist < 1.0).nonzero()[0]
        for i in solved_list:
            saved_dict.append({"img":imgs_list[split+i],"dist":round(ssim_val[i].item(),3)})
            if unsolved:
                solved_imgs_list=np.append(solved_imgs_list,imgs_list[split+i])

        if unsolved:
            unsolved_imgs = np.append(unsolved_imgs,np.delete(unsolved_imgs_list[split:end_idx], solved_list, None))
    return solved_imgs_list, unsolved_imgs,saved_dict

def compute_distance_rotation(memory_folder,threshold,img_list,count=1,delta=5,size=32):
    device = torch.device('cuda:3') if torch.cuda.is_available() else 'cpu'
    best_angle = 0
    angle = count*delta
    angles = []
    memories = []
    result=[]
    idx = 0
    for i in range(count*2+1):
        angles.append(angle)
        angle=angle-delta
    for root, dirs, files in os.walk(memory_folder):
        for file in files:
            if(file.endswith(".ppm")or file.endswith(".png")):
                memories.append(os.path.join(root, file))

    memory_lists=[]
    for memory in memories:
        im = np.array(Image.open(memory).resize((size,size)))
        im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
        im = transforms.ToTensor()(im)
        memory_list = im.repeat([len(angles),1,1,1]).to(device)
        memory_lists.append(memory_list)

    for im_path in img_list:
        print("Currently solve image - ",idx)
        idx+=1
        mapping_res=[]
        rotate_res=[]
        rotated_im=[]
        im = np.array(Image.open(im_path).resize((size,size)))
        im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
        for i in angles:
            im_ = rotate(im, angle=i, reshape=False)
            im_ = transforms.ToTensor()(im_).to(device)
            rotated_im.append(im_)
        rotated_im=torch.stack(rotated_im, dim=0).to(device)
        memory_idx = 1
        for memory_list in memory_lists:
            ssim_val = ssim(memory_list, rotated_im, data_range=1, size_average=False).detach().cpu() # return (N,)
            best_angle_index = torch.argmax(ssim_val).item()
            max_dist = torch.max(ssim_val).item()
            best_angle = angles[best_angle_index]
            if (max_dist>threshold):
                mapping_res.append([str(memory_idx),str(round(max_dist,3))])
                rotate_res.append([str(memory_idx),str(best_angle)])
            memory_idx += 1
        result.append({"name": im_path,"memory":mapping_res,"rotate_angle":rotate_res})

    return result

def compute_distance_translation(memory_folder,threshold,img_list,device,count=1,delta=1,size=32):
    best_angle = 0
    angle = count*delta
    angles = []
    memories = []
    result=[]
    idx = 0
    for i in range(count*2+1):
        angles.append(angle)
        angle=angle-delta
    for root, dirs, files in os.walk(memory_folder):
        for file in files:
            if(file.endswith(".ppm")or file.endswith(".png")):
                memories.append(os.path.join(root, file))

    memory_lists=[]
    for memory in memories:
        im = np.array(Image.open(memory).resize((size,size)))
        im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
        im = transforms.ToTensor()(im).to(device)
        memory_list = im.repeat([len(angles)*len(angles),1,1,1])
        memory_lists.append(memory_list)

    for im_path in img_list:
        print("Currently solve image - ",idx)
        idx+=1
        mapping_res=[]
        translated_res=[]
        translated_im=[]
        translated_pair=[]
        im = np.array(Image.open(im_path).resize((size,size)))
        im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
        for i in angles:
            for j in angles:
                im_ = shift(im, shift=[i,j,0])
                im_ = transforms.ToTensor()(im_)
                translated_im.append(im_)
                translated_pair.append([i,j,0])
        translated_im=torch.stack(translated_im, dim=0).to(device)
        memory_idx = 1
        for memory_list in memory_lists:
            ssim_val = ssim(memory_list, translated_im, data_range=1, size_average=False).detach().cpu() # return (N,)
            best_index = torch.argmax(ssim_val).item()
            max_dist = torch.max(ssim_val).item()
            best_translation = translated_pair[best_index]
            if (max_dist>threshold):
                mapping_res.append([str(memory_idx),str(round(max_dist,3))])
                translated_res.append([str(memory_idx),best_translation])
            memory_idx += 1
        result.append({"name": im_path,"memory":mapping_res,"translated_res":translated_res})

    return result

def memory_check(memory_list,threshold,img_list,device,size=32):
    # calculate ssim for each image
    #print(memory_list.shape)
    result = []
    idx = 0
    for im_path in img_list:
        print("Currently solve image - ",idx)
        mapping_res=[]
        im = np.array(Image.open(im_path).resize((size,size)))
        im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
        im = cv2.copyMakeBorder(im,20,20,20,20,cv2.BORDER_CONSTANT,value=[0,0,0])
        im = transforms.ToTensor()(im).to(device)
        x_list = im.repeat([memory_list.shape[0],1,1,1])
        ssim_val = ssim(memory_list, x_list, data_range=1, size_average=False).detach().cpu()
        qualified_list = (np.asarray(ssim_val) > threshold).nonzero()[0]
        idx += 1
        for i in qualified_list:
            mapping_res.append([str(i+1),str(round(ssim_val[i].item(),3))])
        result.append({"name": im_path,"memory":mapping_res})
    return result


#test stage: to pair up the test image with a memory
def memory_check_single_image(memory_list,memory_features,img_path,threshold,device,size=32):
    #innput image is in PIL image format
    # calculate ssim for each image
    #print(memory_list.shape)
    result = []
    mapping_res=[]
    im = np.asarray(Image.open(img_path))
    #image_lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
    #im = np.zeros((image_lab.shape[0], image_lab.shape[1]))
    #im[:, :] = image_lab[:, :, 0]
    #im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
    im = transforms.ToTensor()(im)
    x_list = im.repeat([memory_list.shape[0],1,1,1]).to(device)
    img_path_=img_path.split("/")
    mask_path="./mask"+"/"+img_path_[-2]+"/"+img_path_[-1][:-4]+"_mask.png"
    json_path="./lesion_images"+"/"+img_path_[-2]+"/"+img_path_[-1][:-4]+".json"
    seg_feature = return_feature_vector(img_path,mask_path,json_path)
    seg_feature = seg_feature[2:]

    seg_features = torch.tensor(seg_feature,dtype=torch.float32).to(device)
    seg_features= seg_features.repeat([memory_list.shape[0],1])

    weight_vector = torch.tensor([0.05,0.05,0.1,0.4,0.1,0.1,0.2],dtype=torch.float32).to(device)
    seg_dist=torch.sum(weight_vector*(seg_features-memory_features)*(seg_features-memory_features),1)
    seg_dist = torch.squeeze(seg_dist).detach().cpu()

    #print(x_list.shape)
    ssim_val = ssim(memory_list, x_list, data_range=1, size_average=False).detach().cpu()
    add_dist = np.asarray(ssim_val+seg_dist)
    qualified_list = (np.asarray(add_dist) < 1.0).nonzero()[0]
    for i in qualified_list:
        mapping_res.append([str(i+1),str(round(add_dist[i].item(),3))])
    result.append({"memory":mapping_res,"rotate_angle":[],"translated_res":[]})
    return result

def memory_check_single_image_rotation(memory_list,img,threshold,device,count=30,delta=1,size=32):
    #innput image is in PIL image format
    # calculate ssim for each image
    best_angle = 0
    angle = count*delta
    angles = []
    rotated_im=[]
    result=[]
    mapping_res=[]
    idx = 0

    for i in range(count*2+1):
        angles.append(angle)
        angle=angle-delta
    #print(memory_list.shape)

    im = np.array(img.resize((size,size)))
    im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
    #im = cv2.copyMakeBorder(im,20,20,20,20,cv2.BORDER_CONSTANT,value=[0,0,0])

    for i in angles:
        im_ = rotate(im.copy(), angle=i, reshape=False)
        im_ = transforms.ToTensor()(im_)
        rotated_im.append(im_)
    rotated_im=torch.stack(rotated_im, dim=0).to(device)

    mapping_res=[]
    rotate_res =[]
    mem_index=1
    for memory in memory_list:
        memories = memory.repeat([len(angles),1,1,1])
        ssim_val = ssim(memories, rotated_im, data_range=1, size_average=False).detach().cpu() # return (N,)
        best_angle_index = torch.argmax(ssim_val).item()
        max_dist = torch.max(ssim_val).item()
        best_angle = angles[best_angle_index]

        if (max_dist>threshold):
            mapping_res.append([str(mem_index),str(round(max_dist,3))])
            rotate_res.append([str(mem_index),str(best_angle)])
        mem_index +=1

    result.append({"memory":mapping_res,"rotate_angle":rotate_res,"translated_res":[]})
    return result

def memory_check_single_image_translation(memory_list,img,threshold,device,count=4,delta=1,size=32):
    #innput image is in PIL image format
    # calculate ssim for each image
    best_translation = 0
    total_shift = count*delta
    x_shift = []
    y_shift = []
    translated_im=[]
    result=[]

    for i in range(count*2+1):
        x_shift.append(total_shift)
        y_shift.append(total_shift)
        total_shift=total_shift-delta

    mapping_res=[]
    translated_pair=[]
    translated_res = []

    im = np.array(img.resize((size,size)))
    im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)

    mapping_res = []
    mem_index=1
    translated_mem=[]
    translated_pair =[]
    for i in x_shift:
        for j in y_shift:
            if (len(np.asarray(im).shape)==2):
                translated_pair.append([i,j])
                img_t = shift(im.copy(),[i,j])
            else:
                translated_pair.append([i,j,0])
                img_t = shift(im.copy(),[i,j,0])
            img_t = transforms.ToTensor()(img_t)
            translated_mem.append(img_t)
    translated_mem=torch.stack(translated_mem, dim=0).to(device)
    for memory in memory_list:
        x_list=memory.repeat([len(x_shift)*len(y_shift),1,1,1]).to(device)
                #print(translated_im.shape,memories.shape)
        ssim_val = ssim(translated_mem, x_list, data_range=1, size_average=False).detach().cpu() # return (N,)
        best_index = torch.argmax(ssim_val).item()
        max_dist = torch.max(ssim_val).item()
        best_translation = translated_pair[best_index]
        if (max_dist>threshold):
            mapping_res.append([str(mem_index),str(round(max_dist,3))])
            translated_res.append([str(mem_index),best_translation])
        mem_index += 1

    result.append({"memory":mapping_res,"rotate_angle":[],"translated_res":translated_res})
    #print(result)
    return result

def memory_check_single_image_translation_n_rotation(memory_list,img,threshold,device,shift_range=4,shift_delta=1,angle_range=30, angle_delta=1, size=32, padding=False):
    #innput image is in PIL image format
    # calculate ssim for each image
    total_shift = shift_range

    angle=angle_range
    x_shift = []
    y_shift = []
    angles=[]
    translated_im=[]
    result=[]

    for i in range(-1*shift_range,shift_range+1,shift_delta):
        x_shift.append(total_shift)
        y_shift.append(total_shift)
        total_shift=total_shift-shift_delta

    for i in range(-1*angle_range,angle_range+1,angle_delta):
        angles.append(angle)
        angle=angle-angle_delta

    mapping_res=[]
    translated_res = []
    rotated_res = []
    img_ = img.copy()

    max_dist = 0
    mem_index=1

    translated_pair =[]
    rotated_angles = []
    translated_im=[]

    im = np.array(img_.resize((size,size)))
    im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)

    for i in x_shift:
        for j in y_shift:
            for k in angles:
                rotated_angles.append(k)
                rotated_img = rotate(im.copy(), angle=k, reshape=False)
                if (len(np.asarray(img_).shape)==2):
                    translated_pair.append([i,j])
                    img_t = shift(rotated_img.copy(),[i,j])
                else:
                    translated_pair.append([i,j,0])
                    img_t = shift(rotated_img.copy(),[i,j,0])
                img_t = transforms.ToTensor()(img_t)
                translated_im.append(img_t)
    translated_im=torch.stack(translated_im, dim=0).to(device)
    for memory in memory_list:
        memories=memory.repeat([len(x_shift)*len(y_shift)*len(angles),1,1,1]).to(device)
        #print(translated_im.shape,memories.shape)
        ssim_val = ssim(memories, translated_im, data_range=1, size_average=False).detach().cpu() # return (N,)
        best_index = torch.argmax(ssim_val).item()
        max_dist = torch.max(ssim_val).item()
        best_translation = translated_pair[best_index]
        best_angle = rotated_angles[best_index]
        if (max_dist>threshold):
            mapping_res.append([str(mem_index),str(round(max_dist,3))])
            translated_res.append([str(mem_index),best_translation])
            rotated_res.append([str(mem_index),best_angle])
            #print("each memory ",mem_index,max_dist,best_angle,best_translation)
        mem_index += 1

    result.append({"memory":mapping_res,"rotate_angle":rotated_res,"translated_res":translated_res})
    return result

def memory_check_single_image_translation_n_rotation_best_mem(memory_list,img,threshold,device,shift_range=4,shift_delta=1,angle_range=30, angle_delta=1, size=32, padding=False):
    #innput image is in PIL image format
    # calculate ssim for each image
    total_shift = shift_range

    angle=angle_range
    x_shift = []
    y_shift = []
    angles=[]
    translated_im=[]
    result=[]

    for i in range(-1*shift_range,shift_range+1,shift_delta):
        x_shift.append(total_shift)
        y_shift.append(total_shift)
        total_shift=total_shift-shift_delta

    for i in range(-1*angle_range,angle_range+1,angle_delta):
        angles.append(angle)
        angle=angle-angle_delta

    mapping_res=[]
    translated_pair=[]
    rotated_angles = []
    translated_res = []
    rotated_res = []
    img_ = img.copy()
    #im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX)
    #im = transforms.ToTensor()(img)
    im = transforms.ToTensor()(img_)
    x_list = im.repeat([memory_list.shape[0],1,1,1]).to(device)
    #print(x_list.shape)
    ssim_val = ssim(memory_list, x_list, data_range=1, size_average=False).detach().cpu()
    for i,j in enumerate(ssim_val):
        mapping_res.append([str(i+1),str(round(j.item(),3))])

    mapping_res.sort(key=lambda x: x[1])
    selected_memories = []
    selected_indices = []
    for i in mapping_res[-10:]:
        best_mem_index = int(i[0])-1
        memory = memory_list[best_mem_index]
        selected_memories.append(memory)
        selected_indices.append(best_mem_index)

    max_dist = 0
    #print(memory_list.shape,translated_im.shape)
    #ssim_val = ssim(memory_list, translated_im, data_range=1, size_average=False).detach().cpu()

    mapping_res=[]

    #com_list = im.repeat([len(x_shift)*len(y_shift)*len(angles),1,1,1]).to(device)
    for memory_,best_mem_index in zip(selected_memories,selected_indices):
        memories=[]
        rotated_angles=[]
        translated_pair=[]
        memory_c = transforms.ToPILImage()(memory_)
        for i in x_shift:
            for j in y_shift:
                for k in angles:
                    rotated_memory = memory_c.copy().rotate(k)
                    rotated_angles.append(k)
                    memory_t = shift_image(rotated_memory.copy(),[i,j])
                    translated_pair.append([i,j])
                    memory_t = transforms.ToTensor()(memory_t)
                    memories.append(memory_t)
        memories=torch.stack(memories,dim=0).to(device)
        im_ = transforms.ToTensor()(img_)
        translated_im = im_.repeat([memories.shape[0],1,1,1]).to(device)
        #print(translated_im.shape,memories.shape)
        ssim_val = ssim(memories, translated_im, data_range=1, size_average=False).detach().cpu() # return (N,)
        best_index = torch.argmax(ssim_val).item()
        best_translation=translated_pair[best_index]
        best_angle=rotated_angles[best_index]
        max_dist = torch.max(ssim_val).item()
        if (max_dist>threshold):
            mapping_res.append([str(best_mem_index+1),str(round(max_dist,3))])
            translated_res.append([str(best_mem_index+1),best_translation])
            rotated_res.append([str(best_mem_index+1),best_angle])

    result.append({"memory":mapping_res,"rotate_angle":rotated_res,"translated_res":translated_res})
    return result
