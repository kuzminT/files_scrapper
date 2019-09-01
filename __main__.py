from classmodule import FilesScrapper
import time

main_url = 'https://mmgp.com/showthread.php?t=8785'

if __name__ == '__main__':
    start_time = time.time()
    scrapper = FilesScrapper()
    elapsed_time = round(time.time() - start_time, 2)
    m = round(elapsed_time / 60, 4)
    print('Время работы программы: {min} минут или {sec} секунд'.format(min=m, sec=elapsed_time))
    print('Downloaded files: {count}'.format(count=len(scrapper.finished_files)))

