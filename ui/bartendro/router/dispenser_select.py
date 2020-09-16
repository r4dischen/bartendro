#!/usr/bin/env python

import sys
import os
import logging
from time import sleep
# from bartendro.error import BartendroBrokenError
from bartendro import app

ROUTER_BUS = 1
ROUTER_ADDRESS = 4
ROUTER_SELECT_CMD_BEGIN = 0
ROUTER_CMD_SYNC_ON = 251
ROUTER_CMD_SYNC_OFF = 252
ROUTER_CMD_PING = 253
ROUTER_CMD_COUNT = 254
ROUTER_CMD_RESET = 255

log = logging.getLogger('bartendro')

try:
    import smbus

    smbus_missing = 0
except ImportError as e:
    if e.message != 'No module named smbus':
        raise
    smbus_missing = 1


class DispenserSelect(object):
    '''This object interacts with the bartendro router controller to select dispensers'''

    def __init__(self, max_dispensers, software_only):
        self.software_only = software_only
        self.max_dispensers = max_dispensers
        self.router = None
        self.num_dispensers = 3
        self.selected = 255

    def _write_byte_with_retry(self, address, byte):
        try:
            self.router.write_byte(address, byte)
        except IOError as e:
            # if we get an error, try again, just once
            try:
                log.error("*** router send: error while sending. Retrying. " + repr(e))
                self.router.write_byte(address, byte)
            except IOError:
                app.globals.set_state(fsm.STATE_ERROR)
                # raise BartendroBrokenError

    def reset(self):
        if self.software_only: return
        self._write_byte_with_retry(ROUTER_ADDRESS, ROUTER_CMD_RESET)
        sleep(.15)

    def select(self, dispenser):
        if self.software_only: return

        # NOTE: This code used to only send the select message if the dispenser changed.
        # but tracking which dispenser was last selected across many web server threads
        # is an extra pain I dont care to handle now. For now we'll just set the dispenser
        # for each packet we send.
        if dispenser < self.max_dispensers:
            self.selected = dispenser
            self._write_byte_with_retry(ROUTER_ADDRESS, dispenser)
            sleep(.01)

    def sync(self, state):
        if self.software_only: return
        try:
            if (state):
                self._write_byte_with_retry(ROUTER_ADDRESS, ROUTER_CMD_SYNC_ON)
            else:
                self._write_byte_with_retry(ROUTER_ADDRESS, ROUTER_CMD_SYNC_OFF)
        except IOError:
            app.globals.set_state(fsm.STATE_ERROR)
            # raise BartendroBrokenError

    def count(self):
        return self.num_dispensers

    def open(self):
        '''Open the i2c connection to the router'''

        if self.software_only: return

        if smbus_missing:
            log.error("You must install the smbus module!")
            sys.exit(-1)

        log.info("Opening I2C bus to router")
        try:
            self.router = smbus.SMBus(ROUTER_BUS)
        except IOError:
            app.globals.set_state(fsm.STATE_ERROR)
            # raise BartendroBrokenError
        log.info("Done.")


if __name__ == "__main__":
    ds = DispenserSelect(15, 0)
    ds.open()
    ds.reset()
