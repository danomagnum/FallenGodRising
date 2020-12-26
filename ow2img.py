from PIL import Image
import numpy as np


def gen_img(ow_zone):

	ts_img = Image.open('data/tileset1.png')

	ts_np = np.asarray(ts_img)

	#Qtile_img = Image.fromarray(ts_np, 'RGBA')
	#Qtile_img.show()
	#Qreturn ts_np
	ts_colors = np.zeros((16,16,4), dtype=np.uint8)


	#determine what color each cell should be by calculating its average color
	for col in range(16):
		for row in range(16):

			x0 = col * 16
			y0 = row * 16

			x1 = x0 + 16
			y1 = y0 + 16

			cell = ts_np[x0:x1, y0:y1]
			ts_colors[col,row] = np.mean(cell, axis=(0,1))

	#tile_img = Image.fromarray(ts_colors, 'RGBA')
	#tile_img.show()
	#tile_img.save('ts.png')
	#return ts_colors

	ts_colors = ts_colors[:,:,0:3]


	ts_img2 = Image.fromarray(ts_colors, mode='RGB')
	ts_img2.show()

	map_np = np.zeros((16 * 36, 16 * 60,3), dtype=np.uint8)


	for ow_x in range(16):
		for ow_y in range(16):
			#how far into the array we are
			ow_level = ow_y * 16 + ow_x
			ow_map = ow_zone.maps[ow_level]

			for map_x in range(60):
					for map_y in range(36):

						pic_x = ow_x * 60 + map_x
						pic_y = (15 - ow_y) * 36 + map_y

						#get the tile used at this map coordinate
						tile_val = ord(ow_map[map_y][map_x])
						#and convert it to an x,y offset into the tileset
						tile_y = tile_val // 16
						tile_x = tile_val % 16

						#Then apply that average color to the pixel
						map_np[pic_y, pic_x] = ts_colors[tile_y, tile_x]

	#np.save('out.dat', map_np)
	#map_np_rgb = map_np[:,:,0:3]
	#map_img = Image.fromarray(map_np_rgb, mode='RGB')
	map_img = Image.fromarray(map_np, mode='RGB')
	map_img.show()
	map_img.save('out.png')

					


