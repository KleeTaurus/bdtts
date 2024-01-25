import wave

infiles = [
    "2024-01-25_13-21-32.wav",
    "2024-01-25_13-21-39.wav",
    "2024-01-25_13-21-51.wav",
    "2024-01-25_13-22-04.wav",
    "2024-01-25_13-22-12.wav",
    "2024-01-25_13-22-24.wav",
    "2024-01-25_13-22-36.wav",
    "2024-01-25_13-22-46.wav"]
outfile = "sounds.wav"

data= []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()
    
output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()