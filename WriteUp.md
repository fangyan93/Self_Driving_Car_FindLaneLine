# Self_Driving_Car_FindLaneLine
Project 1 for Udacity Self Driving car nano degree

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
