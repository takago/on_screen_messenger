from whisper_mic.whisper_mic import WhisperMic

mic = WhisperMic(model='small',device='cuda', pause=0.7)
mic.listen_loop()
