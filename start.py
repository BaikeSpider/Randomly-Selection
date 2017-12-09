import os
import threading


threading.Thread(target=os.system("python spider_main2.py"))
threading.Thread(target=os.system("python spider_main3.py"))
threading.Thread(target=os.system("python spider_main4.py"))
threading.Thread(target=os.system("python spider_main5.py"))
threading.Thread(target=os.system("python spider_main6.py"))

