import shelve
from time import strftime

today = strftime("%Y.%m.%d")
log_path = '/var/log/dokebi/logs'
def get_log(init_log=None, date=today):
    logs = shelve.open(log_path)
    try:
        log = logs[date]
    except KeyError:
        print "Creating todays log"
        if init_log != None:
            log = init_log()
        else:
            raise KeyError
    logs.close()
    return log

def save_log(log, date=today):
    logs = shelve.open(log_path)
    logs[date] = log
    logs.close()
