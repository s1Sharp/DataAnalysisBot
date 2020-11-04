import datetime


class Logger:
    def __init__(self, log_name):
        self.counter = 0
        self.log_name = log_name

        with open(self.log_name, 'w') as log_file:
            message = f'[{str(datetime.datetime.now())[:-7]}] script is running...\n'
            log_file.write(message)
            print(message, end='')

    def log(self, message):
        if self.counter == 1000:
            f = open(self.log_name, 'w')
            f.close()
            self.counter = 0

        result_message = f'[{str(datetime.datetime.now())[:-7]}] {message}\n'
        with open(self.log_name, 'a') as log_file:
            log_file.write(result_message)
        print(result_message, end='')
        self.counter += 1


LOGGER = Logger('log.txt')