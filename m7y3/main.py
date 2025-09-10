import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from deep_translator import GoogleTranslator

duration = 5  # секунды записи
sample_rate = 44100

words_by_level = {
    "easy": ["кот", "собака", "молоко", "солнце"],
    "medium": ["банан", "школа", "окно", "жёлтый"],
    "hard": ["технология", "информация", "произношение", "воображение"]
}

def translator():
    user_answer = 'да'
    while user_answer == 'да':
        print("🎙 Говори сейчас...")
        recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,      
        channels=1,                  
        dtype="int16")              
        sd.wait()  

        wav.write("output.wav", sample_rate, recording)
        print("✅ Запись завершена, обрабатываем...")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("📝 Распознанный текст:", text)
        except sr.UnknownValueError:          
            print("❌ Не удалось распознать речь. Попробуйте еще раз!")
            continue
        except sr.RequestError as e:            
            print(f"❌ Ошибка сервиса: {e}")
            continue

        lang = input("🌍 На какой язык перевести? (например, 'en' - английский, 'es' - испанский, 'pt' - Португальский, 'id' - Индонезийский, 'pl' - Польский, 'it' - Итальянский, 'tr' - Турецкий): ")

        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(text)
            print("✅ Перевод:", translated)
        except Exception as e:
            print(f"❌ Ошибка перевода: {e}")
            
        user_answer = input('🔄 Хотите продолжить? (да/нет): ').lower()

def game():
    print("🎮 Добро пожаловать в игру 'Угадай перевод'!")
    level = input("📊 Выберите уровень сложности (easy, medium, hard): ").lower()

    if level not in words_by_level:
        print("❌ Неверный уровень сложности!")
        return

    mistakes = 0
    score = 0

    while mistakes < 3:
        word = random.choice(words_by_level[level])
        print(f"🔤 Слово для перевода: {word}")

        print("🎙 Произнесите перевод на английском...")
        recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,      
        channels=1,                  
        dtype="int16")              
        sd.wait()  
  
        wav.write("output.wav", sample_rate, recording)
        print("✅ Запись завершена, проверяем...")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            recognized_word = recognizer.recognize_google(audio, language="en-US")
            print("📝 Вы сказали:", recognized_word)
            word_en = GoogleTranslator(source='ru', target='en').translate(word)
            
            if recognized_word.lower() == word_en.lower():
                print("🎉 Правильно! +1 очко")
                score += 1
            else:
                print(f"❌ Неправильно! Правильный перевод: {word_en}")
                mistakes += 1
                print(f"⚠️ Ошибок: {mistakes}/3")
        
        except sr.UnknownValueError:          
            print("❌ Не удалось распознать речь. Попробуйте еще раз!")
            mistakes += 1
            print(f"⚠️ Ошибок: {mistakes}/3")
        except sr.RequestError as e:            
            print(f"❌ Ошибка сервиса: {e}")
            mistakes += 1
            print(f"⚠️ Ошибок: {mistakes}/3")

    print(f"🏁 Игра окончена! Ваш счет: {score}.")

print("👋 Привет! Выберите режим работы:")
choice = input("1 - Переводчик 🈯, 2 - Игра 🎮: ")
if choice == '1':
    translator()
elif choice == '2':
    game()
else:
    print("❌ Неверный ввод. Пожалуйста, введите 1 или 2.")