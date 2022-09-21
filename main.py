import gc
import time

import uasyncio as asyncio
import ulogging as logging

from pasp import plug, pm25, web, wifi
from pasp.collector import collector
from pasp.config import settings
from pasp.controller import controller
from pasp.led import led
from pasp.ota import OTAUpdater

gc.collect()

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
log = logging.getLogger('main')


async def collect_garbage():
    while True:
        gc.collect()
        await asyncio.sleep(5)


def main():
    led.on()

    log.info('Pulse...')
    asyncio.run(led.fast_pulse())

    log.info('Connecting to wifi...')
    asyncio.run(wifi.connect())

    if wifi.sta.isconnected():
        log.info('Checking for updates...')
        ota = OTAUpdater()
        ota.autoupdate()

    log.info('AP Setup...')
    asyncio.run(wifi.ap_setup())

    log.info('Starting PM25 collector...')
    collector.run()

    log.info('Starting smart plug controller...')
    controller.run()

    log.info('Running web server...')
    web.run()

    log.info('Setting up garbage collection...')
    asyncio.create_task(collect_garbage())

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except:
        loop.stop()
        loop.close()


if __name__ == '__main__':
    main()
