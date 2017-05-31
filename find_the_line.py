#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys
import math

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    
def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def Dis(p1, p2):
    return np.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def draw(y1, y2, slop, dis, img, color, thickness):
    print(slop, dis)
    xx1 = (y1 - dis) / slop
    yy1 = y1
    xx2 = (y2 - dis) / slop
    yy2 = y2
    cv2.line(img, (int(xx1), int(yy1)), (int(xx2), int(yy2)), color, thickness)

def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    """
    This function is used to draw the full extent of the lane, here we take all edges after
    canny edge detection and compute slop of each edge, group them 
    """
    width = img.shape[1]
    height = img.shape[0]

    upper_limit = 0.61 * height
    lower_limit = height

    x_left_down = 0.052 * width
    x_left_up = 0.448 * width
    x_right_up = 0.5625 * width
    x_right_down = 0.9375 * width

    slops = {} # key : (slop, dis), value: ((x1, y1), (x2, y2))
    slop_threshold = 0.006
    for line in lines:
        for x1,y1,x2,y2 in line:
            # for lines with simlar slop and intercept, only choose the pair of points with longest distance 
            slop = (y1 - y2) / (x1 - x2)
            dis = y1 - slop * x1
            
            insert = 0
            old_keys = slops.keys()
            for s in old_keys:
                if(abs(slop - s[0]) < slop_threshold or abs(dis - s[1]) < 10):
                        insert = 1
                        p1 = slops[s][0][0]
                        p2 = slops[s][0][1]
                        newP1 = ()
                        newP2 = ()
                        
                        # find a pair of points with longest distance
                        x_axis =[]
                        x_axis.append(x1)
                        x_axis.append(x2)
                        x_axis.append(p1[0])
                        x_axis.append(p2[0])
                        
                        points = []
                        points.append((x1, y1))
                        points.append((x2, y2))
                        points.append(p1)
                        points.append(p2)
                        
                        newP1_index = x_axis.index(min(x_axis))
                        newP2_index = x_axis.index(max(x_axis))
                        
                        # record the pair of points and current slop and intercept for computing average later
                        newP1 = points[newP1_index]
                        newP2 = points[newP2_index]

                        newSlop = slops[s][1][0][0] + slop
                        newDis = slops[s][1][0][1] + dis

                        num = slops[s][1][1] + 1
                        del slops[s]
                        slops[(slop, dis)] = ((newP1, newP2), ((newSlop, newDis), num))
                        insert = 1
                        break
            # insert the slop and dis if there is no similar previous one
            if(insert == 0) :
                slops[(slop, dis)] = (((x1, y1), (x2, y2)), ((slop, dis), 1))
                
    right_len = 0
    left_len = 0
    num1 = 0
    num2 = 0

    valid_slops_right = []
    valid_slops_left = []
    valid_dis_right = []
    valid_dis_left = []
    for s in slops.keys():
        
        p1 = slops[s][0][0]
        p2 = slops[s][0][1]
        slop_dis = slops[s][1][0]
        total = slops[s][1][1]
        # compute average slop
        if(p1[0] - p2[0] == 0):
            continue
        # slop =  ((p1[1] - p2[1]) / (p1[0] - p2[0]) + slop_dis[0]) / (total + 1)
        # dis = (p1[1] - slop * p1[0] + slop_dis[1]) / (total + 1)
        slop = slop_dis[0] / total 
        dis = slop_dis[1] / total

        # since the slops of two lane lines have opposite signs, we only need to decide 1 slop for each lane line
        # choose the slop of a line with longest length as the slop of the corresponding lane line
        # since the position of the lane line is relatively fixed, we can limit the value of slop to remove some noise
        leng = Dis(p1, p2)
        
        if((slop > 0.5 and slop < 0.8) or (slop > -0.8 and slop < -0.5)):
            # draw(upper_limit, lower_limit, slop, dis, img, color, thickness) 
            if(slop > 0 and p1[0] > (x_left_up + x_right_up) / 2):
                valid_slops_right.append(slop)
                valid_dis_right.append(dis)
            if(slop < 0 and p1[0] < (x_left_up + x_right_up) / 2):
                valid_slops_left.append(slop)
                valid_dis_left.append(dis)

    slop_right = 0
    dis_right = 0
    slop_left = 0
    dis_left = 0
    if(len(valid_slops_right) > 0):
        slop_right = np.sum(valid_slops_right) / len(valid_slops_right)
        dis_right = np.sum(valid_dis_right) / len(valid_dis_right)
    if(len(valid_slops_left) > 0):
        slop_left = np.sum(valid_slops_left) / len(valid_slops_left)
        dis_left = np.sum(valid_dis_left) / len(valid_dis_left)
    # for i in range(3):
    #     valid_slops_right.append(slop_right)
    #     valid_dis_right.append(dis_right)
    #     valid_slops_left.append(slop_left)
    #     valid_dis_left.append(dis_left)
    #     slop_right = np.sum(valid_slops_right) / len(valid_slops_right)
    #     dis_right = np.sum(valid_dis_right) / len(valid_dis_right)
    #     slop_left = np.sum(valid_slops_left) / len(valid_slops_left)
    #     dis_left = np.sum(valid_dis_left) / len(valid_dis_left)
    # draw the lines
    if(slop_right != 0):
        draw(upper_limit, lower_limit, slop_right, dis_right, img, color, thickness)
    print("ss ", slop_left)
    if(slop_left != 0):
        draw(upper_limit, lower_limit, slop_left, dis_left, img, color, thickness)  
    cv2.imshow('llinees', img)
    # cv2.waitKey(0)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)

import os
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoFileClip
from IPython.display import HTML

kernel_size = 3
low_threshold = 100
high_threshold = 200
path = "test_images/"
video_path = "test_videos/"

def find_line_in_image(image):
    width = image.shape[1]
    height = image.shape[0]
    # parameters for region mask
    upper_limit = 0.61 * height
    lower_limit = height

    x_left_down = 0.052 * width
    x_left_up = 0.448 * width
    x_right_up = 0.5625 * width
    x_right_down = 0.9375 * width

    cv2.imshow('origin', image)
    cv2.imwrite('corner.png', image)
	#printing out some stats and plotting
    print('This image is:', type(image), 'with dimensions:', image.shape)
    gray = grayscale(image)
    cv2.imwrite("gray_corner.png", gray)
    # cv2.imshow('gray', gray)
    blur = gaussian_blur(gray, kernel_size)
    # cv2.imwrite("blurr.jpg", blur)
    # cv2.imshow('blur', blur)
    edges = canny(blur, low_threshold, high_threshold)
    # cv2.imwrite("edges.jpg", edges)
    # cv2.imshow('edges', edges)
    
    vertices = np.array([[(x_left_down,lower_limit),(x_left_up, upper_limit), (x_right_up, upper_limit), (x_right_down,lower_limit)]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)
    # cv2.imwrite("masked_edges.jpg", masked_edges)
    rho = 1 # distance resolution in pixels of the Hough grid
    theta = 1.5 * np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 3     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 15 #minimum number of pixels making up a line
    max_line_gap = 10    # maximum gap in pixels between connectable line segments
    
    line_image = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)
    
    # Draw the lines on the edge image
    lines_edges = weighted_img(line_image, image, 0.8, 1., 0.)
    cv2.imshow('line_edges', lines_edges)
    # cv2.imwrite("lines_edges.jpg", lines_edges)
    # cv2.waitKey(0)
    return lines_edges

def for_lines():
    files = os.listdir(path)
    
    for file in files:
        if(file == '.DS_Store' or file == "."):
            continue
        print(file)
        file = os.path.join(path, file)
        
        image = cv2.imread(file)
        find_line_in_image(image)



def for_video(name):
    input_video = name
    output_video = "output" + name
    white_output = os.path.join(video_path, output_video)
    white_input = os.path.join(video_path, input_video)
    print(white_input)
    clip1 = VideoFileClip(white_input)
    white_clip = clip1.fl_image(find_line_in_image) #NOTE: this function expects color images!!
    white_clip.write_videofile(white_output, audio=False)
    HTML("""
    <video width="960" height="540" controls>
      <source src="{0}">
    </video>
    """.format(white_output))


def single_image(name):
    file = os.path.join(path, name)
    image = cv2.imread(file)
    print(file)
    result = find_line_in_image(image)
    cv2.imshow('result', result)
    output_file = os.path.join(path, "output_segment_" + name)
    # cv2.imwrite(output_file,result)
    cv2.waitKey(0)

if __name__ == "__main__":
	for_video("solidYellowLeft.mp4")
    # for_video("solidWhiteRight.mp4")
    # for_video("challenge.mp4")
    # single_image("challenge.png")
    # single_image("solidWhiteRight.jpg")
    # for_lines()
    
