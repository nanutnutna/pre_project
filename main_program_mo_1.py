import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mipmg
import glob
import os
from sklearn import neighbors


new_image = []
result = []
crop = []
path1 = 'C:\\Users\\59010374\\Desktop\\New folder (3)'
path2 = '/*.png'
T_path = path1 + path2
images = [cv2.imread(file) for file in glob.glob(T_path)]
#image = cv2.imread("D:/Ionogram/201001/01/ionogram_10c/20100101024000.png")
for image in images:
    crop_image = image[20:490,17:600]
    crop.append(crop_image)
    height, width,channels = crop_image.shape
    gray_image = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
    gray_image[0:497,200::] = 255 #ลบส่วนทั้ไม่ใช้ออก
    gray_image[400::] = 255
    for i in range(0,height) :
        for j in range(0,width) :
            if gray_image[i,j] > 80 :
                gray_image[i,j] = 255
            else :
                gray_image[i,j] = 0
    for i in range(0,80):
        for j in range(0,width):
            if gray_image[i,j] == 0 :
                gray_image[i:height,j] = 255
    RGB_black = []
    for i in range(0,200):
        lst = gray_image[0:height,i]
        for j in lst :
            if j == 0 :
                RGB_black.append(j)
        if len(RGB_black) >= 10 :
            gray_image[0:height,i] = 255
        RGB_black.clear()
    round_for_remove_noise = 0
    while round_for_remove_noise <= 3 :
        for i in range(0,height):
            for j in range(0,200):
                if gray_image[i,j] == 0 and gray_image[i,j-1] == 255 and gray_image[i,j+1] == 255 :
                    if gray_image[i-1,j] == 255 and gray_image[i-1,j-1] == 255 and gray_image[i-1,j+1] == 255 :
                        if gray_image[i+1,j] == 255 and gray_image[i+1,j-1] == 255 and gray_image[i+1,j+1] == 255 :
                            gray_image[i,j] = 255
                else :
                    continue
        for i in range(0,height):
            for j in range(0,200):
                if gray_image[i,j] == 0 and gray_image[i+1,j] == 0 and gray_image[i+2,j] == 255 and gray_image[i-1,j] == 255 :
                    if gray_image[i,j-1] == 255 and gray_image[i+1,j-1] == 255 and gray_image[i+2,j-1] == 255 and gray_image[i-1,j-1] == 255 :
                        if gray_image[i,j+1] == 255 and gray_image[i+1,j+1] == 255 and gray_image[i+2,j+1] == 255 and gray_image[i-1,j+1] == 255 :
                            gray_image[i,j] = 255
                else :
                    continue
        
        round_for_remove_noise += 1
    #Detect line
    detect = []
    for i in range(5,370):
        for j in range(5,200):
            if gray_image[i,j] == 0 and gray_image[i+1,j+1] == 0 and gray_image[i+2,j+2] == 0 :
                detect.append(True)
                gray_image[350,350] = 0
            elif gray_image[i,j] == 0 and gray_image[i,j+1] == 0 and gray_image[i+1,j+2] == 0 and gray_image[i+1,j+3] == 0 and gray_image[i+2,j+4] == 0 and gray_image[i+2,j+5] == 0 :
                detect.append(True)
                gray_image[350,350] = 0
            elif gray_image[i,j] == 0 and gray_image[i,j+1] == 0 and gray_image[i+1,j+1] == 0 and gray_image[i+1,j+2] == 0 and gray_image[i+2,j+2] == 0 and gray_image[i+2,j+3] == 0:
                detect.append(True)
                gray_image[350,350] = 0
            elif gray_image[i,j] == 0 and gray_image[i+1,j] == 0 and gray_image[i+2,j+1] == 0 and gray_image[i+3,j+1] == 0  and gray_image[i+4,j+2] == 0 and gray_image[i+5,j+2] == 0 :
                detect.append(True)
                gray_image[350,350] = 0
            elif gray_image[i,j] == 0 and gray_image[i,j+1] == 0 and gray_image[i,j+2] == 0 :
                for i in range(350,height):
                    lst = gray_image[0:width,i]
                    for j in lst :
                        if j == 0 :
                            RGB_black.append(j)
                    if len(RGB_black) >= 4 :
                        detect.append(False)
                    RGB_black.clear()
            else :
                detect.append(False)
    #font = cv2.FONT_HERSHEY_SIMPLEX    
    result = []    
    if True in detect :
        #cv2.putText(gray_image,'Have line',(250,150),font,1,(0,0,255),1,cv2.LINE_AA)
        find_spread_image = []
        for i in range(200,370):
            for j in range(0,120):
                if gray_image[i,j] == 0 and gray_image[i-1,j] == 255 and gray_image[i,j+1] == 255 and gray_image[i,j-1] == 255 and gray_image[i+1,j] == 255 :
                    find_spread_image.append(True)
        if len(find_spread_image) >= 8 :
            #cv2.putText(gray_image,'Space image',(250,250),font,1,(0,0,255),1,cv2.LINE_AA)
            result.append('No')
            #plt.imshow(gray_image,cmap='Greys_r')
            #plt.show()
        else :
            #cv2.putText(gray_image,'No sapce',(250,200),font,1,(0,0,255),1,cv2.LINE_AA)
            gray_image[350,350] = 0
            #plt.imshow(gray_image,cmap='Greys_r')
            #plt.show()

    elif True not in detect :
        #cv2.putText(gray_image,'Not Found',(250,150),font,1,(0,0,0),1,cv2.LINE_AA)
        result.append('No')
    new_image.append(gray_image)

#print(len(new_image))
#print(len(result)) #ดูว่ามีรูปที่ไม่ได้ใช้กี่รูป 

#for i in new_image:
 #   cv2.imshow('test',i)
  #  cv2.waitKey()
#    plt.imshow(gray_image,cmap='Greys_r')
 #   plt.show()


def find_hF_foF2():
    #Find h'f
    fof2_y = []
    fof2_x = []
    hf = []
    for photo in new_image :
        if photo[350,350] == 0 :
            photo[350,350] =255
            img = photo
            img_00 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
            img_01 = img_00[1]/255
            n = 0
            i = 0
            k = 0
            Xaxis = []
            Yaxis = []
            y_ = []
            T = np.linspace(0, 582,583)[:, np.newaxis]

            for k in img_01 :
                for i in k :
                    n += 1
                    if i == 0 :
                        x = [int(n % 583)-1]
                        yy = abs((n/583)-470)
                        y = [int(yy)]
                        Xaxis.append(x)
                        Yaxis.append(y)
                
            n_neighbors = 12

            for i, weights in enumerate(['uniform']):
                knn = neighbors.KNeighborsRegressor(n_neighbors, weights)
                y_ = knn.fit(Xaxis,Yaxis).predict(T)
                #plt.scatter(Xaxis, Yaxis, c='k', label='data')
                #plt.scatter(T,y_, c='g', label='prediction')
                #plt.axis('tight')
                #plt.legend()
                #plt.show()
                maxv = y_[582]
                num_ii = 0
    
            for ii in y_:
                if ii == maxv:
                    #print (num_ii)
                    if  ii == maxv:
                        break
                num_ii += 1
            img[350,350] = 0
            lower = min(y_)
            new_lower = [lower[0],lower[0]*(1000/470)]
            #print ("foF2 in pixel is " + str(num_ii)) 
            #print ("h'F in pixel is " + str(new_lower[0]))
            fof2_MHz = (num_ii*27.5)/583
            fof2_km = y_[num_ii]*1000/470
            foF2 = fof2_km[0]*(1000/470)
            new_fof2_MHz = "{0:.3f}".format(fof2_MHz)
            fof2_x.append(new_fof2_MHz)
            #new_fof2_km = "{0:.3f}".format(fof2_km)
            fof2_y.append(foF2)
            new_hf = "{0:.3f}".format(new_lower[1])
            hf.append(new_hf)
            #print ("A value foF2 is " + str(fof2_MHz) + " MHz")
            #print ("h'F is " + str(new_lower[1]) + " km")
            #cv2.putText(img,'foF2 is ' + str(fof2_MHz) +' MHz',(250,300),font,1,(0,0,255),1,cv2.LINE_AA)
            #cv2.putText(img,"h'F is " + str(new_hf) + ' km',(250,200),font,1,(0,0,255),1,cv2.LINE_AA)
            #show_image.append(img)
            #cv2.imshow('test',img)
            #cv2.waitKey()
    #plot foF2
    #print(fof2_x)
    #print(fof2_y)
    #plt.scatter(fof2_x,fof2_y)
    #plt.plot(fof2_x,fof2_y)
    #plt.show()
        else :
            hf.append('NaN\t')
            fof2_x.append('NaN\t')
    return  hf,fof2_x

def write_text_file():
    hf,fof2_x = find_hF_foF2()
    location_save =  'C:\\Users\\59010374\\Desktop\\Text\\'
    surname = '.txt'
    dirs = os.listdir(path1)
    date_time = []
 
    for i in dirs :
        i = i[:-4]
        file_name = i[6:14]
        date_time.append(i)

    name =  location_save + file_name + surname
    f = open(name,'w')
    for i in range(len(date_time)):
        line  = str(date_time[i]) + '\t' + 'hF '+ str(hf[i]) + '\tfoF2 ' + str(fof2_x[i]) + '\n'
        f.write(line)
    f.close()   





find_hF_foF2()
write_text_file()
