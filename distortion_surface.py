# import requests
import rew_client
import json
import time

# Using third octave frequencies above 20hz
_FREQUENCIES = [20, 25, 31.5, 40, 50, 63, 80, 
                100, 125, 160, 200, 250, 315, 400, 500, 
                630, 800, 1000, 1250, 1600, 2000, 2500, 
                3150, 4000, 5000, 6300, 8000, 10000, 
                12500, 16000, 20000]

_TEST_FREQUENCIES = [1000]

_LEVEL_START = -30
_LEVEL_INTERVAL = 2.5
_LEVEL_MAX = 10
_LEVEL_UNITS = 'dBu'

def get_distortion(frequency, level, units=""):
    if units == "":
        units = _LEVEL_UNITS
    rew_client.generator_set_freq(frequency)
    rew_client.generator_set_level(level, units)
    rew_client.generator_start()
    rew_client.rta_start()
    rew_client.rta_wait_status(True)
    rew_client.rta_wait_status(False)
    rew_client.generator_stop()
    dist = rew_client.rta_get_distortion()
    if len(dist) > 1:
        raise Exception('More than 1 input detected in RTA, a single input should be used')
    dist = dist[0]
    # keep file size down, only taking data we want
    reduced_dist = {}
    reduced_dist["thdPlusN"] = dist.get("thdPlusN").get("value")
    if "thd" in dist:
        reduced_dist["thd"] = dist.get("thd").get("value")
    if "rmsNandNHDdBFS" in dist:
        reduced_dist["NandNHD"] = dist.get("rmsNandNHDdBFS")
    h_count = 2
    for harmonic in dist.get("harmonics"):
        reduced_dist[f'H{h_count}'] = harmonic.get("value")
        h_count += 1
    return reduced_dist

def start_sweep(frequency_values):
    print('Starting sweeps')
    start_time = time.time()

    THD_VALUES = {}
    for freq in frequency_values:
        cur_level = _LEVEL_START
        levels = {}
        while cur_level <= _LEVEL_MAX:
            print(f'Measuring {freq} Hz at {cur_level} {_LEVEL_UNITS}')
            dist = get_distortion(freq, cur_level)
            levels[cur_level] = dist
            if cur_level == _LEVEL_MAX: break
            cur_level += _LEVEL_INTERVAL
            if cur_level > _LEVEL_MAX: cur_level = _LEVEL_MAX
        THD_VALUES[freq] = levels

    end_time = time.time()

    print(f'Sweep ran in {end_time-start_time} seconds')

    with open(f'thd-data-{_LEVEL_UNITS}.json', 'w') as f:
        json.dump(THD_VALUES, f)



start_sweep(_FREQUENCIES)
# start_sweep(_TEST_FREQUENCIES)