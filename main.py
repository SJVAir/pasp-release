import gc
import machine
import time

import uasyncio as asyncio
import ulogging as logging

from pasp import ota, plug, pm25, web, wifi, system
from pasp.beacon import beacon
from pasp.collector import collector
from pasp.config import settings
from pasp.controller import controller
from pasp.beacon import beacon

gc.collect()

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
log = logging.getLogger('main')


async def collect_garbage():
    while True:
        gc.collect()
        await asyncio.sleep(5)


def main():
    log.info(f'PASP Version: {system.version()}')
    log.info(f'Wemos C3-Mini: {system.board_version()}')

    # Signal that we've started.
    beacon.off()
    asyncio.run(beacon.animate())

    # Wifi, OTA, and AP setup.
    asyncio.run(wifi.connect())
    ota.check_for_updates()
    asyncio.run(wifi.ap_setup())

    # Core functionality.
    collector.run()
    controller.run()
    web.run()

    # Automatic garbage collection.
    asyncio.create_task(collect_garbage())

    # Let's get to work!
    asyncio.run(beacon.animate())
    asyncio.run(beacon.pulse(delay=69))
    beacon.on()

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except:
        loop.stop()
        loop.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        log.error(str(err))
        for x in range(20):
            beacon.on()
            time.sleep(.5)
            beacon.off()
            time.sleep(.5)
        machine.reset()
