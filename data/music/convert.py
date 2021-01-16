import sys
import os

conversions = [r'fluidsynth -i -o synth.cpu-cores=2 -T oga -F {}_fb.ogg ../SoundFonts/FatBoy-v0.790.sf2 {}.mid',
               r'fluidsynth -i -o synth.cpu-cores=2 -T oga -F {}_gu.ogg ../SoundFonts/GeneralUser\ GS\ v1.471.sf2 {}.mid']


for f in os.listdir():
	#try:
		if f[-4:] == '.mid':
			song_name = f[:-4]
			for cmdstring in conversions:
				command = cmdstring.format(song_name, song_name)
				os.system(command)
	#except:
		#print('Error with {}'.format(f))
