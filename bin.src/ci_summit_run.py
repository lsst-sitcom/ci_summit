import os

from lsst.ci.builder import CommandRunner
from lsst.ci.builder.commands import (
    CreateButler,
    RegisterInstrument,
    WriteCuratedCalibrations,
    IngestRaws,
    DefineVisits,
    TestRunner,
)

TESTDATA_DIR = os.environ["TESTDATA_CI_SUMMIT_DIR"]
INSTRUMENT_NAME = "LATISS"

index_command = 0

ciRunner = CommandRunner(os.environ["CI_SUMMIT_DIR"])
ciRunner.register("butler", 0)(CreateButler)


@ciRunner.register("instrument", index_command := index_command + 1)
class SummitRegisterInstrument(RegisterInstrument):
    instrumentName = "lsst.obs.lsst.Latiss"


@ciRunner.register("write_calibrations", index_command := index_command + 1)
class SummitWriteCuratedCalibrations(WriteCuratedCalibrations):
    instrumentName = INSTRUMENT_NAME


@ciRunner.register("ingest", index_command := index_command + 1)
class SummitIngestRaws(IngestRaws):
    rawLocation = os.path.join(TESTDATA_DIR, "raw")


@ciRunner.register("define_visits", index_command := index_command + 1)
class SummitDefineVisits(DefineVisits):
    instrumentName = INSTRUMENT_NAME
    collectionsName = f"{INSTRUMENT_NAME}/raw/all"


ciRunner.run()
