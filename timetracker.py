from time import sleep, strftime
from storage import get_log, save_log
from tabulate import tabulate
from subprocess import Popen, PIPE

getoutput = lambda x: Popen(x, stdout=PIPE).communicate()[0]
stripvarname = lambda x: x[int(x.index('='))+2:]

#TODO when stored on disk handle removal adding and renaming of workspaces

workspace_names_string = stripvarname(getoutput(("xprop", "-root", "_NET_DESKTOP_NAMES")).strip())
workspace_names = [name.strip('\" ') for name in  workspace_names_string.split(',')]

def get_workspace_number():
    workspace_number_string = stripvarname(getoutput(("xprop", "-root", "_NET_CURRENT_DESKTOP")).strip())
    workspace_number = int(workspace_number_string)
    return workspace_number

def current_workspace():
    return workspace_names[get_workspace_number()]

def format_time(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%d h %2d min %2d sec" % (h, m, s)

def init_log():
    log = {}
    for name in workspace_names:
        log[name] = 0
        log['Total'] = 0
    return log

def tabulate_log(log=get_log(init_log)):
    table = [[item[0], format_time(item[1])] for item in log.items() if item[0] != 'Total']
    table.append(['------', '-------------------'])
    table.append(['Total', format_time(log['Total'])])
    return tabulate(table, headers=['Workspace', 'Time'], tablefmt='simple')

def do_logging(step=1):
    """
    step: The time step between logging of state in seconds, default: log once a second
    """
    log = get_log(init_log)
    while True:
        start = int(strftime('%s'))
        sleep(step)
        end = int(strftime('%s'))
        span = end-start
        log[current_workspace()] += span
        log['Total'] += span
        save_log(log)
