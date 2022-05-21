from osrparse import Replay, parse_replay_data
import cv2
import numpy as np
import configparser
import os

configParser = configparser.RawConfigParser()   
configFilePath = r'./config.txt'
configParser.read(configFilePath)

skin_name = configParser['DEFAULT']['skin']

# frame_size = (500, 500)

# img = np.zeros([frame_size[0], frame_size[1], 3])
# cv2.imwrite('img.jpg', img)
# cv2.imshow('image', img)
# cv2.waitKey()

# img = cv2.imread('./skin/' + skin_name)
# print(img)
fps = 60
transition_length = 50
np.set_printoptions(threshold=np.inf)

def render_count(number, offset):
	digits = len(str(number+1))
	frame = np.zeros((number_imgs[0].shape[0], number_imgs[0].shape[1]*digits, 4), dtype=np.uint8)

	# Convert number into list of digits
	num_list = np.asarray(list(str(number)), dtype=np.int8)
	if num_list.shape[0] < digits:
		tmp = np.zeros(digits, dtype=np.int8)
		tmp[1:] = num_list[:]
		num_list = tmp
	print(num_list.shape)
	if num_list[0] == 0:
		num_list[0] = -1
	print(num_list)

	next_num_list = np.asarray(list(str(number+1)), dtype=np.uint8)
	transition_prog = min(1, offset/transition_length)

	digit_width = number_imgs[0].shape[1]
	digit_height = number_imgs[0].shape[0]

	ver_offset = int(digit_height * transition_prog)
	for i in range(digits):
		hor_offset = digit_width * i
		if num_list[i] != next_num_list[i]:
			if num_list[i] != -1:
				frame[ver_offset:,hor_offset:hor_offset + digit_width] \
					= number_imgs[num_list[i]][:digit_height - ver_offset,:]

			frame[:ver_offset,hor_offset:hor_offset + digit_width] \
				= number_imgs[next_num_list[i]][digit_height - ver_offset:,:]
		else:
			frame[:,hor_offset:hor_offset + digit_width] \
					= number_imgs[num_list[i]][:,:]

	return frame
	# exit(0)

def show_img(img):
	print(img.shape)
	img_3ch = img[:,:,:3]
	if img.shape[2] == 4:
		for i in range(3):
			img_3ch[:,:,i] = img_3ch[:,:,i]*(img[:,:,3]/255)

		# img_3ch[:,:,:] = img_3ch[:,:,:]/255
	print(img_3ch.shape)

	cv2.imshow('image', img_3ch)
	cv2.waitKey()

skin_folder = os.path.join(os.getcwd(), 'skin')
skin_folder = os.path.join(skin_folder, skin_name)
# print(skin_folder)

number_gap = 10
number_imgs = []
for num in range(10):
	file_name = 'default-' + str(num) + '.png'
	file_path = os.path.join(skin_folder, file_name)
	img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

	# scale_percent = 70 # percent of original size
	# width = int(img.shape[1] * scale_percent / 100)
	# height = int(img.shape[0] * scale_percent / 100)
	# dim = (width, height)
	# resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	# cv2.imwrite(file_path, resized)

	img_4ch = np.empty((img.shape[0], img.shape[1], 4))
	if img.shape[2] == 4:
		img_4ch = img
	else:
		img_4ch[:,:,:3] = img[:,:,:]
	number_imgs.append(img_4ch)
render_count(3699, 400)



replay = Replay.from_path('test replay.osr')

frame = 0
cur_ms = 0
pre_event_ms = 0
event_index = 0
while True:
	cur_ms = frame/fps*1000

	next_event = replay.replay_data[event_index]
	print(int(next_event.keys), frame, cur_ms)
	if pre_event_ms + next_event.time_delta < cur_ms:
		event_index += 1
		pre_event_ms += next_event.time_delta
		cur_event = next_event
		# print(cur_ms - pre_event_ms)
	frame += 1

for replay_event in replay.replay_data:
	print(int(replay_event.keys))
# min_coor = [0, 0]
# max_coor = [0, 0]
# for replay_event in replay.replay_data:
# 	min_coor[0] = min(min_coor[0], replay_event.x)
# 	min_coor[1] = min(min_coor[1], replay_event.y)

# 	max_coor[0] = max(max_coor[0], replay_event.x)
# 	max_coor[1] = max(max_coor[1], replay_event.y)
# # print(min_coor, max_coor)

# print(replay.replay_data)