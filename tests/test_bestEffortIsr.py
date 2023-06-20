# This file is part of ci_summit.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import unittest

import lsst.afw.image as afwImage
from lsst.daf.butler.tests import addDatasetType
import lsst.utils.tests
from lsst.utils import getPackageDir

from lsst.summit.utils.bestEffort import BestEffortIsr
import lsst.summit.utils.butlerUtils as butlerUtils


class BestEffortIsrTestCase(lsst.utils.tests.TestCase):
    @classmethod
    def setUp(cls):
        butlerPath = os.path.join(getPackageDir("ci_summit"), "DATA")
        cls.bestEffortIsr = BestEffortIsr(repoString=butlerPath)

        for col in cls.bestEffortIsr.collections:
            cls.bestEffortIsr.butler.registry.registerCollection(col)

        addDatasetType(
            cls.bestEffortIsr.butler,
            "quickLookExp",
            ["instrument", "exposure", "detector"],
            "ExposureF",
        )

        cls.dataId = {"day_obs": 20210121, "seq_num": 743, "detector": 0}

    def test_getExposure(self):
        # in most locations this will load a pre-made image
        exp = self.bestEffortIsr.getExposure(self.dataId)
        self.assertIsInstance(exp, afwImage.Exposure)

        # this will always actually run isr with whatever calibs are available
        exp = self.bestEffortIsr.getExposure(self.dataId, forceRemake=True)
        self.assertIsInstance(exp, afwImage.Exposure)

    def test_getExposureFromExpRecord(self):
        """Test getting with an expRecord. This requires also passing in
        the detector number as a kwarg.
        """
        expRecord = butlerUtils.getExpRecordFromDataId(
            self.bestEffortIsr.butler, self.dataId
        )

        exp = self.bestEffortIsr.getExposure(expRecord, detector=0)
        self.assertIsInstance(exp, afwImage.Exposure)

        # and then again with just the dataCoordinate
        exp = self.bestEffortIsr.getExposure(expRecord.dataId, detector=0)
        self.assertIsInstance(exp, afwImage.Exposure)

        # Try forceRemake with an expRecord and a detector as a kwarg
        # as forceRemake has a different code path, as it has to get a raw
        exp = self.bestEffortIsr.getExposure(
            expRecord.dataId, detector=0, forceRemake=True
        )
        self.assertIsInstance(exp, afwImage.Exposure)

    def test_raises(self):
        """Ensure function cannot be called without specifying a detector."""
        dataId = self.dataId
        dataId.pop("detector")
        with self.assertRaises(ValueError):
            self.bestEffortIsr.getExposure(dataId, forceRemake=True)


class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
