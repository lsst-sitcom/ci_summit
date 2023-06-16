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

import matplotlib
import os
import tempfile
import unittest

from lsst.daf.butler import Butler
from lsst.daf.butler.tests import addDatasetType
import lsst.utils.tests
from lsst.utils import getPackageDir

from lsst.summit.utils import ImageExaminer
from lsst.summit.utils.bestEffort import BestEffortIsr
from lsst.summit.utils.butlerUtils import getLatissDefaultCollections


matplotlib.use("Agg")


class ImageExaminerTestCase(lsst.utils.tests.TestCase):
    @classmethod
    def setUpClass(cls):
        butlerPath = os.path.join(getPackageDir("ci_summit"), "DATA")
        cls.butler = Butler(
            butlerPath,
            collections=getLatissDefaultCollections(),
            writeable=False,
            instrument="LATISS",
        )
        cls.dataId = {"day_obs": 20200315, "seq_num": 120, "detector": 0}
        cls.bestEffort = BestEffortIsr(repoString=butlerPath)
        for col in cls.bestEffort.collections:
            cls.bestEffort.butler.registry.registerCollection(col)

        addDatasetType(
            cls.bestEffort.butler,
            "quickLookExp",
            ["instrument", "exposure", "detector"],
            "ExposureF",
        )

        cls.outputDir = tempfile.mkdtemp()
        cls.outputFilename = os.path.join(cls.outputDir, "testImageExaminer.jpg")

    def test_imageExaminer(self):
        """Test that the animator produces a large file without worrying about
        the contents?
        """
        exp = self.bestEffort.getExposure(self.dataId)
        imExam = ImageExaminer(
            exp,
            doTweakCentroid=True,
            boxHalfSize=105,
            doForceCoM=False,
            savePlots=self.outputFilename,
        )
        imExam.plot()

        self.assertTrue(os.path.isfile(self.outputFilename))
        self.assertTrue(os.path.getsize(self.outputFilename) > 100000)


class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
