import esp
import gc
import machine

esp.osdebug(None)

# Take out the trash
gc.enable()
gc.collect()
