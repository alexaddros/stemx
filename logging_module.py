from datetime import datetime as dt
import telebot
import threading as th

class Logger:
    def __init__(self, filename='log.txt', output=True, to_telegram=True) -> None:
        self.output = output
        self.filename = filename
        self.to_telegram = to_telegram
        self.bot = telebot.TeleBot('2050656491:AAHMhz2pZlouTvo6y4TgML1VDwUjqzT1cI4')
        self.recievers_id = [1834907685, 413813117, 1220999, 683815202]      # можно добавить ID получателей через запятую c пробелом
        self.telegram_life_thread = th.Thread(target=self.bot.polling, args=[True])
        self.telegram_life_thread.start()

    def log(self, data, category='INFO'):
        if self.output:
            print(f'[{category}] [{str(dt.now())[:19]}] - {data}')
            with open(self.filename, 'a') as log_file:
                log_file.write(f'[{category}] [{str(dt.now())[:22]}] - {data}\n')
        else:
            with open(self.filename, 'a') as log_file:
                log_file.write(f'[{category}] [{str(dt.now())[:22]}] - {data}\n')
        
        if self.to_telegram:
            self.send_message(data)

    def send_message(self, data):
        for ident in self.recievers_id:
            self.bot.send_message(ident, data)