import os
import trimesh
import open3d as o3d

directory = r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\buildings_mesh_ply"
output_directory = r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\buildings_pointcloud_ply"
i = 1

for file in os.listdir(directory):
    mesh = o3d.io.read_triangle_mesh(os.path.join(directory, file))
    mesh.compute_vertex_normals()

    pointcloud = mesh.sample_points_poisson_disk(number_of_points=4096, init_factor=5)
    o3d.io.write_point_cloud(fr"{output_directory}\{file}", pointcloud)
    print(f"{i}th file has been converted to point cloud")
    i += 1


# mesh = trimesh.load(r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\buildings_mesh_ply\block1_building0.ply")
# # mesh.show(resolution=(600, 600))
# pointcloud = mesh.sample(4096)
# pointcloud.show()
# pointcloud.export(r"trail.ply")

# mesh = o3d.io.read_triangle_mesh(r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\buildings_mesh_ply\block1_building0.ply")
# mesh.compute_vertex_normals()
#
# pcd = mesh.sample_points_poisson_disk(number_of_points=4096, init_factor=5)
# # o3d.visualization.draw_geometries([pcd])
#
# o3d.io.write_point_cloud("trial_point_cloud.ply", pcd)
# # o3d.visualization.draw_geometries([pcd])