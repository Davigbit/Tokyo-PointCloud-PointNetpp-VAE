# Tokyo-PointCloud-PointNetpp-VAE
Project is not closed, there will be improvements in the near future.

# Table of contents
1. [Data](##Data)
2. [Model](#Model)<br>
## Introduction to the problem at hand
We find classic buildings boring, so what if we could create a AI algorithm to add funky elements to existing building design, or better yet give us new buildings from nothing. <br>
Enter Variational Autoencoders (VAEs). We started out thinking about wake-sleep networks, however VAEs are more modern, and they are easier to find resources about. 

## Data
We are using the Tokyo 3D Point Cloud Dataset. It is a dataset of 3D point clouds of buildings in Tokyo. The dataset is available at: https://3dview.tokyo-digitaltwin.metro.tokyo.lg.jp/
There are multiple version of the dataset, the one I downloaded came in the following form:<br>
dataset: <br>
&nbsp;&nbsp;&nbsp;&nbsp;- ku (district)1 <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        - data <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            - data0.b3dm (it is a 3D mesh of a small part of the district, lets call them blocks, included many buildings inside) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            - data1.b3dm   <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        - tileset.json <br>
&nbsp;&nbsp;&nbsp;&nbsp;    - ku (district)2 <br>
&nbsp;&nbsp;&nbsp;&nbsp;  - ...  <br>
<br>
### dataset to master_b3dm
I copied all of the b3dm files for all blocks under the same folder using dataset2master.py so iteration is simpler <br>


https://github.com/user-attachments/assets/e251dedc-121f-439a-a7b0-e079c91dee02


### master_b3dm to master_glb
Our end goal is to have a dataset of 3D point clouds, but there is no real way (at least that I know of) converting from b3dm directly to .ply so we need to convert the b3dm files to glb files. <br>
I did this using Cesium GS's 3d-tiles-tools, you can see the code under b3dm2glb.py <br>

### master_glb to blocks_mesh_ply
My b3dm2ply and glb2ply script failed due to a processing issue with the trimesh library, so I used aspose 3ds glb to ply converter. <br>

### blocks_mesh_ply to buildings_mesh_ply
I used block2building.ipynb to seperate buildings in each block so we could feed individual buildings to our NN. <br> 
I first tried seperating the mesh into connected components and saving them. Didn't work, it instead gave me a single wall for a building. The results:

https://github.com/user-attachments/assets/5d4b216f-4fa4-4ced-b4e4-d3edee2dd1ef
 <br>
I tried using the trimesh library's fill holes function but it failed. <br>
I then clustered faces based on the center of each triangle (the building block of a mesh) and used sklearn's DBSCAN algorithm to cluster them. Didn't work. The results: 

https://github.com/user-attachments/assets/28951a53-6f29-483f-afb4-77453418d2cd

<br>
Finally, I clustered based on edge proximity. To find the min edge distance between 2 components, we created a distance matrix for every possible combination of componenti.vertexa and componentj.vertexb and found the distance for all combinations. <br>
We used DBSCAN again with epsilon = 0.5 and joined the walls that are clustered together and saved them to buildings_mesh_ply
<br> Worked.  The results:

https://github.com/user-attachments/assets/a086d58b-de5c-403e-82fd-2dfc1a092018
 <br>

### buildings_mesh_ply to buildings_pointcloud_ply
I used the mesh2pointcloud_ply.py to convert the buildings to point clouds by using open3D's poisson sampling dots on the surfaces of the mesh. 

https://github.com/user-attachments/assets/86716259-e910-4528-bbfe-55ea7f34884e

<br>


## Model
I tried 3 version of VAEs, all of them combined with PointNet++ architecture. 
This is the architecture ![Tokyo PP_VAE Architecture](https://github.com/user-attachments/assets/be2c2c51-1d47-488b-9821-8d7515cfbf1b)

<br> 
1) Classic VAE with Chamfers Distance and KL Divergence <br>
The results (the red points are the input, green is the predicted output): 

https://github.com/user-attachments/assets/1e2a93a4-bee0-45a6-882e-776aefc3ca94

2) Disentangled VAE with Beta=3, Chamfers Distance and KL Divergence <br>
The results: 

https://github.com/user-attachments/assets/96525ea0-52af-4ac6-93a3-6b7b90d19f50

3) Classic VAE with Chamfers Distance, KL Divergence, and a loss function I desinged (Distance Between 2 Closest Points)  <br>
The results: 


https://github.com/user-attachments/assets/43b276a2-5df0-4e72-b2d8-3127477169a0

<br>
To Dos and Observations:
- We see that first model's output is very scattered, custom lost function in the 3rd helps us out, but not good enough. Modify the last layer to improve the point distribution. 
- In the second model, we see that the model predicts a unit cube. Train models without standarization. 
- Train models with data augmentation.
- Make your model bigger if necessary.
