import pyaudio

class StreamManager():
  FORMAT = pyaudio.paInt16
  CHANNELS = 2
  RATE = 44100
  CHUNK = 1024
  audio = pyaudio.PyAudio()
 
  @staticmethod
  def startStream(isInput: bool):
    return (StreamManager.audio.open(format=StreamManager.FORMAT, channels=StreamManager.CHANNELS,
      rate=StreamManager.RATE, input=True,
      frames_per_buffer=StreamManager.CHUNK) if isInput else StreamManager.audio.open(format=StreamManager.FORMAT, channels=StreamManager.CHANNELS,
      rate=StreamManager.RATE, output=True,
      frames_per_buffer=StreamManager.CHUNK))
  
# start Recording

if __name__ == '__main__':
  inStream = StreamManager.startStream(True)
  outStream = StreamManager.startStream(False)
  while True:
    data = inStream.read(StreamManager.CHUNK)
    outStream.write(data)  
