import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

class SpeechProcessing:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as micinput:
            self.recognizer.adjust_for_ambient_noise(micinput, duration=1)
            
            text = ""
            audio = None
            try:   
                print("Listening...")
                audio = self.recognizer.listen(micinput, timeout=5)
            except sr.WaitTimeoutError as error:
                print("WaitTimeoutError occurred:", error)
                return text
            except Exception as error:
                print("Exception occurred:", error)
                return text

            try:
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"User said: {text}")
            except sr.UnknownValueError as error:
                print("UnknownValueError occurred:", error)
            except sr.RequestError as error:
                print("RequestError occurred:", error)
            except Exception as error:
                print("Exception occurred:", error)
            return text
        
    def speak(self):
        audio = AudioSegment.from_file("temp.mp3", format="mp3")
        play(audio)