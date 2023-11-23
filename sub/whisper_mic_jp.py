from whisper_mic.whisper_mic import WhisperMic

mic = WhisperMic(model='small',device='cuda', pause=1.0)
mic.listen_loop()
