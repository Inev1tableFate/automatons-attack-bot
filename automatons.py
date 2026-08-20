from PIL import ImageGrab, ImageEnhance, ImageOps, Image
import time
import random
import pytesseract
import keyboard


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


bbox = (470 , 160, 1445 , 625)
threshold = 130


def get_dota_word():
    
    screenshot = ImageGrab.grab(bbox = bbox , include_layered_windows=False, all_screens=False, xdisplay=None, window=None, scale_down=False)
    screenshot = screenshot.convert('L')
    screenshot = screenshot.point(lambda p: 255 if p > threshold else 0)
    screenshot = ImageOps.invert(screenshot)
    w, h = screenshot.size
    screenshot = screenshot.resize((w * 3, h * 3), Image.Resampling.LANCZOS)

    #screenshot.save("testov.png")
    custom_config = r'--oem 1 --psm 11 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    text = (pytesseract.image_to_string ( screenshot, config = custom_config ))
    words = [w.strip().upper() for w in text.split() if len(w.strip()) > 2]
    if words:    
        return words[0]
    return None


def type_instant(input_word):
    
    if input_word not in history:
        history.add(input_word)
        keyboard.write(input_word.lower())        
        
        
def type_split(input_word):

    if input_word not in history:
        mid = len(input_word) // 2       
        part1 = input_word[:mid].lower()
        part2 = input_word[mid:].lower() 
        keyboard.write(part1)        
        keyboard.write(part2)

        
def type_straight(input_word):    
    
    if input_word not in history:
            for letter in input_word:
                keyboard.write(letter.lower())
                time.sleep(random.uniform(0.01 , 0.03))
                

option_num = input("Введите 1 для режима instant (мнгновенный ввод);\nВведите 2 для режима split (ввод по 50% слова);\nВведите 3 для режима straight (ввод по 1 букве с случайной задержкой).\n")
                  
            
if option_num == "1":
    chosen_function = type_instant
                 
elif option_num == "2":
    chosen_function = type_split

elif option_num == "3":
    chosen_function = type_straight

else:
    print ("Внимание ! Неверный ввод , автоматически выбран режим instant")
    chosen_function = type_instant


history = set()
start_time = time.time()              
time.sleep(2)
            
                       
while not keyboard.is_pressed('f10'):
    
    input_word = get_dota_word()
    
    
    if input_word is not None and input_word.strip() != " ":
        chosen_function(input_word)

    
    if time.time() - start_time >= 5.0:
        history.clear()
        start_time = time.time() 
print ("Программа остановлена.")