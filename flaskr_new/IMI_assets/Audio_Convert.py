import subprocess

subprocess.call(['ffmpeg', '-y', '-i', '118057.mp3', '-ar', '8000', '-ac', '1', '-b:a', "64k", 'test.wav'])