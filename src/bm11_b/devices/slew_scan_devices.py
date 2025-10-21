from ophyd import Component as Cpt, Device, EpicsSignal, EpicsSignalRO, Signal
from ophyd.status import SubscriptionStatus
from ophyd.signal import UNSET_VALUE

class SlewDevice(Device):
    scan_complete = Cpt(EpicsSignalRO, "slew.SMSG", kind="omitted")
    scan_faze = Cpt(EpicsSignalRO, "slew.FAZE", kind="omitted", string=True)

    startN = Cpt(EpicsSignal, "slew_startN.PROC", kind="omitted")

    startTTH = Cpt(EpicsSignal, "slew_setup.A", kind="config")
    endTTH = Cpt(EpicsSignal, "slew_setup.B", kind="config")
    stepTTH = Cpt(EpicsSignal, "slew_setup.D", kind="config")
    timeStep = Cpt(EpicsSignal, "slew_setup.H", kind="config")

    sampleName = Cpt(EpicsSignal, "userHolder1", kind="config")
    formula = Cpt(EpicsSignal, "userHolder2", kind="config")
        # epics.caput("11bmb:userHolder4.VAL",self.email)
        # epics.caput("11bmb:userHolder8.VAL",self.barcode)

    scanComment = Cpt(EpicsSignal, "saveData_comment1", kind="config")
    sampleComment = Cpt(EpicsSignal, "saveData_comment2", kind="config")

    mda_root = Cpt(Signal, value='/net/s11bmsrv1/', kind='normal', string=True)
    mda_file = Cpt(EpicsSignal, "saveData_fileName", kind="normal", string=True)
    mda_path = Cpt(EpicsSignal, "saveData_fullPathName", kind="normal", string=True)

    def trigger(self):
        def cb(value, old_value, **kwargs):
            print(f"{value=!r}, {old_value=!r}")
            if value == 'IDLE' and old_value not in {'IDLE', UNSET_VALUE}:
                return True
            return False
        sts = SubscriptionStatus(self.scan_faze, cb, run=False)

        self.startN.put(1)

        return sts
    

class SpyLambda(Device):
    fname = Cpt(EpicsSignalRO,'HDF1:FullFileName_RBV')
    save_state = Cpt(EpicsSignalRO, "HDF1:WriteFile", string=True)

    def trigger(self):
        def cb(value, old_value, **kwargs):
            print(f"{value=!r}, {old_value=!r}")
            if value == 'DONE' and old_value == 'WRITING':
                return True
            return False
        sts = SubscriptionStatus(self.save_state, cb, run=False)

        return sts