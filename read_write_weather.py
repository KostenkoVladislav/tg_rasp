def weather_file(mode, id_tg=None, wt_time=None):
    if mode == 'a': ## append
        with open('data/weather_id.txt', 'a') as f:
            f.write('\n' + id_tg + ' '+ wt_time)
    if mode == 'r': ## read all
        with open('data/weather_id.txt', 'r') as f:
            content = f.read()
    if mode == 'c':  ## check id_tg
        with open('data/weather_id.txt', 'r') as f:
            content = f.read()

        return content.split(sep='\n')


