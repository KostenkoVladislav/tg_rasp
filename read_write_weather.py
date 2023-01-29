def weather_file(mode, id_tg=None, wt_time=None):
    if mode == 'a':  # append
        with open('data/weather_id.txt', 'a') as f:
            f.write(f'{id_tg}\n')
    if mode == 'r':  # read all
        with open('data/weather_id.txt', 'r') as f:
            content = f.read()
            return content.split(sep='\n')
    if mode == 'c':  # check id_tg
        with open('data/weather_id.txt', 'r') as f:
            content = f.read()
        if str(id_tg) in content.split(sep='\n'):
            return True
        else:
            return False
    if mode == 'd':  # delete
        with open('data/weather_id.txt', 'r+') as f:
            content = f.read().split(sep='\n')
            try:
                content.remove(str(id_tg))
            except ValueError:
                return 0
            f.seek(0)
            for i in content:
                f.write(i + '\n')
            f.truncate()
            f.close()

