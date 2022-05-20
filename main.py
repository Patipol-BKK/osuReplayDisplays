from osrparse import Replay, parse_replay_data
import cv2
import numpy as np

frame_size = (500, 500)

img = np.zeros([frame_size[0], frame_size[1], 3])
cv2.imwrite('img.jpg', img)
cv2.imshow('image', img)
cv2.waitKey()



replay = Replay.from_path('test replay.osr')
min_coor = [0, 0]
max_coor = [0, 0]
for replay_event in replay.replay_data:
	min_coor[0] = min(min_coor[0], replay_event.x)
	min_coor[1] = min(min_coor[1], replay_event.y)

	max_coor[0] = max(max_coor[0], replay_event.x)
	max_coor[1] = max(max_coor[1], replay_event.y)
print(min_coor, max_coor)
