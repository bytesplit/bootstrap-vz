from bootstrapvz.base import Task
from .. import phases
import os
import shutil


class ClearMOTD(Task):
    description = 'Clearing the MOTD'
    phase = phases.system_cleaning

    @classmethod
    def run(cls, info):
        with open('/var/run/motd', 'w'):
            pass


class CleanTMP(Task):
    description = 'Removing temporary files'
    phase = phases.system_cleaning

    @classmethod
    def run(cls, info):
        tmp = os.path.join(info.root, 'tmp')
        for tmp_file in [os.path.join(tmp, f) for f in os.listdir(tmp)]:
            if os.path.isfile(tmp_file):
                os.remove(tmp_file)
            else:
                shutil.rmtree(tmp_file)

        log = os.path.join(info.root, 'var/log/')
        os.remove(os.path.join(log, 'bootstrap.log'))
        os.remove(os.path.join(log, 'dpkg.log'))


class ClearMachineId(Task):
    description = 'Clearing the Machine ID'
    phase = phases.system_cleaning

    @classmethod
    def run(cls, info):
        import logging
        log = logging.getLogger(__name__)
        for machineid_file in [os.path.join(info.root, f) for f in ['etc/machine-id', 'var/lib/dbus/machine-id']]:
            if os.path.isfile(machineid_file):
                log.debug(machineid_file + ' found, clearing')
                with open(machineid_file, 'w'):
                    pass
            else:
                log.debug(machineid_file + ' not found, not clearing')
