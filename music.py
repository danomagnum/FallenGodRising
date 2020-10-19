'''
The interface for the music library requires a thread(queue) routine that takes a multiprocessing queue as its argument and listens for
the following messages.  All messages are lists where the zeroth item is the command and the rest of the items are the parameters.
['play', 'filename']: start playing the file 'filename'.  If already playing a song, switch.
['fadeout']: fadeout the current playing song.
['quit']: return from the function


A shutdown routine is also required that takes the process object returned by multiprocessing as well as the queue for that process as arguments.

'''

def thread(queue):
	import pygame

	pygame.mixer.init()
	while True:
		msg = queue.get()
		if msg[0] == 'play':
			pygame.mixer.music.load(msg[1])
			pygame.mixer.music.play(loops = -1, start=0.0, fade_ms=1000)
		elif msg[0] == 'fadeout':
			pygame.mixer.music.fadeout(1000)
		elif msg[0] == 'quit':
			return

def shutdown(process, queue):
	queue.put(['quit'])
	process.join(timeout=0.2)
	if process.is_alive():
		process.kill()
