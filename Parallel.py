import sys

currentPath = "/nfs/dust/cms/user/shwillia/Moriond/LimitProjection/"

sys.path.append(currentPath)

from ProjectionManager import ProjectionManager

Projection=ProjectionManager(currentPath)
Projection.RunProjection(int(sys.argv[1]))

