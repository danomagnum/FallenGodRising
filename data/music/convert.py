import sys
import os

cmdstring = 'fluidsynth -nli -r 48000 -o synth.cpu-cores=2 -T oga -F {}.ogg ../SoundFonts/FatBoy-v0.790.sf2 {}.mid'


for f in os.listdir():
	#try:
		if f[-4:] == '.mid':
			song_name = f[:-4]
			command = cmdstring.format(song_name, song_name)
			os.system(command)
	#except:
		#print('Error with {}'.format(f))
