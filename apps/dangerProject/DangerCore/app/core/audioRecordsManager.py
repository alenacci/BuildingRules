import os

class AudioRecordsManager:

	def __init__(self):
		self.AUDIO_DIR = "audioUploads/"
		self.clean_directory()
		self.samplesCount = 0

	def clean_directory(self):
		for the_file in os.listdir(self.AUDIO_DIR):
			file_path = os.path.join(self.AUDIO_DIR, the_file)
			try:
				os.unlink(file_path)
			except Exception, e:
				print(e)

	def get_new_filename(self,original):
		self.samplesCount += 1
		return "audioSample" + str(self.samplesCount) + os.path.splitext(original)[1]

	#dumb function which returns the last audio file XXX
	def get_file(self):
		if len(os.listdir(self.AUDIO_DIR)) > 0:
			filename = max(os.listdir(self.AUDIO_DIR))
			return os.path.join("../" + self.AUDIO_DIR, filename)
		else:
			return None

