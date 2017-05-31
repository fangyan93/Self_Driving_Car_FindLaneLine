# Self_Driving_Car_FindLaneLine
Project 1 for Udacity Self Driving car nano degree

## Pipeline
My pipeline consists of 6 steps. 
<figure>
 <img src="test_images/outputsolidYellowCurve2.jpg" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Original image </p> 
 </figcaption>
Step 1, convert the images converted to grayscale 
<figure>
 <img src="report_image/gray.jpg" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Grayscale image </p> 
 </figcaption>
Step 2, apply gaussian smoothing on grayscaled images 
Step 3, apply canny edge detection, obtain a set of edges
<figure>
 <img src="report_image/edges.jpg" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Edges afte edge detection </p> 
 </figcaption>
Step 4, apply region mask, select edges in desired region
<figure>
 <img src="report_image/masked_edges.jpg" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Edges after region mask </p> 
 </figcaption>
Step 5, use Hough transform to find and draw the lines
<figure>
 <img src="test_images/output_segment_solidYellowCurve2.jpg" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;">  Line Segment for lane line in original image </p> 
 </figcaption>
</figure>
 <p></p> 
Step 6, add the lines on original image
<figure>
 <img src="report_image/lines_edges.jpg" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> full text of line</p> 
 </figcaption>

## Revise Draw_line() function
In order to draw a single line on the left and right lanes, I modified the draw_lines() function by computing slop of each edge, grouping lines with similar slop, taking average on all negative slops to get the final slop for left lane line, obtaining the final slop for right lane line in the same way. Please see the code in "find_line_fangyan.ipynb" for details.

## Shortcomings with your current pipeline
The main restraint for my current pipeline lies in the draw_lines() function. 
First, since it is assumed that the left lane line lies in left half image and right lane lies in the right half, the draw_line function may become ineffective for those image in which lane lines are at other positions rather than the normal one.

Second, this program does not work on lane lines at a large angle turn on the road, where the lane line become far away from straight. 

Third, the output of video stream is actually not satisfying, because the final drawn line is obtained by averaging all the slops of hough transform output lines, even though it works fine for an image, for a series of image, the slops the drawn line does not fit the lane line perfectly like shown in P1_example.mp4. 

Besides, in some cases, the lane line become almost invisible after grayscale, like pictures shown below. In that case, this program even fail to find the left lane line, the tuning of parameters of canny and Hough transform does not helpful on this either. 

## Possible improvement
For the first 3 shortcomings, I have spent a day to try seraval methods to overcome the current shortcomings, one way I have tried is to draw more than 1 lines at each half of image, but since the line segments of the lane line still have different slop, it is unreasonable to extrapolate each line to upper and lower bound of the region mask, other approaches also can not solve the problem on curve lines. 

One possible way to improve is that do not average the slops, instead, merge or connect the line segments using starting and ending points on the line, extrapolate the line which is closest to bottom of image to the region lower bound, and extrapolate the line closest to upper bound of region mask to the upper bound. The output may not be very straight, but it should fit the lane line better and works on curve lane.

For the 4th shortcoming, I have not tried it. But in order to improve this, some work has to be done before running grayscale() function. Maybe the color selection is helpful here, that is, only pixel close to yellow and white is reserved. 
