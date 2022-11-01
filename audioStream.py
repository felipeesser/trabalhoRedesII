import pyaudio

class StreamManager():
  FORMAT = pyaudio.paInt16
  CHANNELS = 2
  RATE = 44100
  CHUNK = 1024
  audio = pyaudio.PyAudio()
 
  def startStream(self, isInput: bool):
    return (self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
      rate=self.RATE, input=True,
      frames_per_buffer=self.CHUNK) if isInput else self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
      rate=self.RATE, output=True,
      frames_per_buffer=self.CHUNK))
  
# start Recording

if __name__ == '__main__':
  streamManager = StreamManager()
  inStream = streamManager.startStream(True)
  outStream = streamManager.startStream(False)
  while True:
    data = inStream.read(streamManager.CHUNK)
    outStream.write(data)  
