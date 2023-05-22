from src.maze_generator import Maze
from src.Interface import *

config = Get_config()
maze = Maze(config["taille"], config["taille"])
level = maze.Get_fmaze()
lab = Lab(level, config)
camera_group = CameraGroup(lab)
lab.Set_Cam(camera_group)
lab.ajout_mur()
lab.Run()
