from bluesky import plan_stubs as bps
from apsbits.core.instrument_init import oregistry
import  bluesky.preprocessors as bpp
import datetime, time

def slew_scan(start=-6.0, end=28.0, step=0.001, timeStep=0.1):
    """under development"""
    # epics.caput("11bmb:slew_setup.A",self.startTTH)
    # epics.caput("11bmb:slew_setup.B",self.endTTH)
    # epics.caput("11bmb:slew_setup.D",self.stepTTH)
    # epics.caput("11bmb:slew_setup.H",self.timeStep)
    # epics.caput("11bmb:userHolder1.VAL",self.sampleName)
    # epics.caput("11bmb:userHolder2.VAL",self.formula)
    # epics.caput("11bmb:saveData_comment1",self.scanComment)
    # epics.caput("11bmb:saveData_comment2",self.sampleComment)
    # epics.caput("11bmb:userHolder4.VAL",self.email)
    # epics.caput("11bmb:userHolder8.VAL",self.barcode)
    slew = oregistry["slew"]
    tth = oregistry["tth"]
    spy_lambda = oregistry["spy_lambda"]
    yield from bps.mv(
        slew.startTTH, start,
        slew.endTTH, end,
        slew.stepTTH, step,
        slew.timeStep, timeStep
    )

    # scan_complete = Cpt(EpicsSignalRO, "slew.SMSG", kind="omitted")

    # startN = Cpt(EpicsSignal, "slew_startN.PROC", kind="omitted")

    # directories, T, spinner, etc...

    # run the scan
    yield from bps.mv(tth, start)

    @bpp.run_decorator()
    def inner():
        yield from bps.trigger_and_read([spy_lambda, slew])


    return (yield from inner())
    
    # epics.caput("11bmb:slew_startN.PROC",True,wait=True)
    # done=False
    # while not done:
    #     time.sleep(10)
    #     if epics.caget("11bmb:slew.SMSG")=="SCAN Complete":
    #         done=True
