from src.maze_generator import Maze
from src.Interface import Lab, CameraGroup

maze = Maze(30,30)
level = maze.Get_fmaze()
lab = Lab(level)
camera_group = CameraGroup(lab)
lab.Set_Cam(camera_group)
lab.ajout_mur()
lab.Run()