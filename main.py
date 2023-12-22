import speech_recognition as sr
from deep_translator import GoogleTranslator
import pygame

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def display_text(speech_text, translated_text):
    pygame.init()
    SIZE = WIDTH, HEIGHT = (1024, 720)
    FPS = 30
    yellow = (255, 255, 0)
    hot_pink = (255, 105, 180)
    font_speech = pygame.font.SysFont('Arial', 64)
    font_translation = pygame.font.SysFont('Verdana', 64)
    screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    screen.fill(pygame.Color('black'))
    blit_text(screen, speech_text, (20, 20), font_speech, color=yellow)
    blit_text(screen, translated_text, (20, 720//2), font_translation, color=hot_pink)
    pygame.display.update()

def translate_speech():
    r = sr.Recognizer()

    print("RECORDING IN ENGLISH...\n")
    print()

    while True:
        try:
            with sr.Microphone(device_index=1) as source:
                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                # Set noise threshold
                audio = r.listen(source)

            speech_text = r.recognize_google(audio)
            print(speech_text)

            translated_text = GoogleTranslator(
                source='auto', target='it').translate(speech_text)
            display_text(speech_text,translated_text)
            print(translated_text)
            print()

        except sr.UnknownValueError:
            print("[...* Speech not recognized *...]".upper())
        except sr.RequestError:
            print("[...* Connection error *...]".upper())
        except Exception as e:
            print(f"[...* An error occurred: {str(e)} *...]".upper())


if __name__ == "__main__":
    translate_speech()
