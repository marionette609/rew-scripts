import requests
import time

_HOST = '127.0.0.1'
_PORT = 4735
_POLL_INTERVAL = 1

def rta_start():
    requests.post(
        url=f'http://{_HOST}:{_PORT}/rta/command',
        json={"command":"Start"}
    )

# poll rta until it has stopped
# desired_status False for wait until rta is off
# desired_status True for wait until rta is on
def rta_wait_status(desired_status=False):
    while True:
        req = requests.get(
            url=f'http://{_HOST}:{_PORT}/rta/status'
        )
        status = req.json()
        if status.get('running') == desired_status:
            return
        time.sleep(_POLL_INTERVAL)

def rta_get_distortion(unit='dBFS'):
    req = requests.get(
        url=f'http://{_HOST}:{_PORT}/rta/distortion?unit={unit}',
    )
    return req.json()

def generator_start():
    requests.post(
        url=f'http://{_HOST}:{_PORT}/generator/command',
        json={"command":"Play"}
    )

def generator_stop():
    requests.post(
        url=f'http://{_HOST}:{_PORT}/generator/command',
        json={"command":"Stop"}
    )

def generator_set_freq(freq):
    requests.post(
        url=f'http://{_HOST}:{_PORT}/generator/signal/configuration',
        json={
            "frequency": freq,
            "lockFrequencyToRTAFFT": False,
            "addHarmonicDistortion": False,
            "addDither": True,
            "ditherBits": 24
        }
    )

def generator_set_level(value, unit='V'):
    requests.post(
        url=f'http://{_HOST}:{_PORT}/generator/level',
        json={
            "value": value,
            "unit": unit
        }
    )

