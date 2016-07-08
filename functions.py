import config


def fit_schedule(bus_time):
    from datetime import datetime

    current_hour = datetime.now().hour
    current_min = datetime.now().minute
    int_current_time = current_hour * 60 + current_min

    fit_time = []

    for t in bus_time:
        int_t = int(t[:2]) * 60 + int(t[-2:])
        if int_current_time < int_t:
            fit_time.append(t)
    if len(fit_time) > 0:
        return fit_time
    else:
        return None


def find_nerest(bus_time):
    fit_time = fit_schedule(bus_time)
    if fit_time:
        return fit_time[0]
    else:
        return "%s" % config.NO_BUS_AVAILABLE


def schedule(bus_schedule):
    return bus_schedule

