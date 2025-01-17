import os
import subprocess
import unittest
from baseclasses import BaseRegTest
from cgnsutilities.cgnsutilities import readGrid, BC

baseDir = os.path.dirname(os.path.abspath(__file__))


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = readGrid(os.path.abspath(os.path.join(baseDir, "../examples/717_wl_L2.cgns")))

    def test_getTotalCellsNodes(self, train=False):
        totalCells, totalNodes = self.grid.getTotalCellsNodes()
        refFile = os.path.join(baseDir, "ref", "totalCellsNodes.ref")
        with BaseRegTest(refFile, train=train) as handler:
            handler.root_add_val("Total cells", totalCells, tol=0)
            handler.root_add_val("Total nodes", totalNodes, tol=0)

    def train_getTotalCellsNodes(self):
        self.test_getTotalCellsNodes(train=True)

    def test_getWallCellsNodes(self, train=False):
        nWallCells, nWallNodes = self.grid.getWallCellsNodes()
        refFile = os.path.join(baseDir, "ref", "wallCellsNodes.ref")
        with BaseRegTest(refFile, train=train) as handler:
            handler.root_add_val("Wall cells", nWallCells, tol=0)
            handler.root_add_val("Wall nodes", nWallNodes, tol=0)

    def train_getWallCellsNodes(self):
        self.test_getWallCellsNodes(train=True)

    def test_getBlockInfo(self, train=False):
        blockInfo = self.grid.getBlockInfo()
        refFile = os.path.join(baseDir, "ref", "blockInfo.ref")
        with BaseRegTest(refFile, train=train) as handler:
            handler.root_add_dict("Block info", blockInfo, tol=0)

    def train_getBlockInfo(self):
        self.test_getBlockInfo(train=True)

    def test_overwriteFamilies(self):
        # Find a specific BC and overwrite the family
        famFile = os.path.abspath(os.path.join(baseDir, "../examples/family_famFile"))
        # Check the family before overwriting.
        self.assertEqual(self.grid.blocks[0].bocos[0].family.strip().decode("utf-8"), "wall")
        self.grid.overwriteFamilies(famFile)
        self.assertEqual(self.grid.blocks[0].bocos[0].family, "wing1")

    def test_overwriteBCs(self):
        # Find a specific BC and overwrite the type and family
        bcFile = os.path.abspath(os.path.join(baseDir, "../examples/overwriteBCs_bcFile"))
        # Check the BC before overwriting. Note that the "updated" BC is first deleted and new appended
        self.assertEqual(self.grid.blocks[0].bocos[0].family.strip().decode("utf-8"), "wall")
        self.assertEqual(self.grid.blocks[0].bocos[0].type, BC["bcwallviscous"])
        self.grid.overwriteBCs(bcFile)
        self.assertEqual(self.grid.blocks[0].bocos[-1].family, "wall_inviscid")
        self.assertEqual(self.grid.blocks[0].bocos[-1].type, BC["bcwallinviscid"])


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.grid = os.path.abspath(os.path.join(baseDir, "../examples/717_wl_L2.cgns"))

    def test_overwriteBCs_CLI(self):
        if os.path.isfile("717_wl_L2_overwriteBCs.cgns"):
            os.remove("717_wl_L2_overwriteBCs.cgns")

        cmd = "cgns_utils overwriteBC "
        cmd += self.grid + " "
        cmd += os.path.abspath(os.path.join(baseDir, "../examples/overwriteBCs_bcFile")) + " "
        cmd += "717_wl_L2_overwriteBCs.cgns"

        out = subprocess.run(cmd, shell=True)
        self.assertFalse(out.returncode)
        self.assertTrue(os.path.isfile("717_wl_L2_overwriteBCs.cgns"))
        os.remove("717_wl_L2_overwriteBCs.cgns")

    def test_overwriteFamilies(self):
        if os.path.isfile("717_wl_L2_overwriteFamilies.cgns"):
            os.remove("717_wl_L2_overwriteFamilies.cgns")

        cmd = "cgns_utils overwriteFamilies "
        cmd += self.grid + " "
        cmd += os.path.abspath(os.path.join(baseDir, "../examples/family_famFile")) + " "
        cmd += "717_wl_L2_overwriteFamilies.cgns"

        out = subprocess.run(cmd, shell=True)
        self.assertFalse(out.returncode)
        self.assertTrue(os.path.isfile("717_wl_L2_overwriteFamilies.cgns"))
        os.remove("717_wl_L2_overwriteFamilies.cgns")


class TestBlock(unittest.TestCase):
    def setUp(self):
        self.grid = readGrid(os.path.abspath(os.path.join(baseDir, "../examples/717_wl_L2.cgns")))

    def test_getNumCells(self, train=False):
        refFile = os.path.join(baseDir, "ref", "block_getNumCells.ref")
        with BaseRegTest(refFile, train=train) as handler:
            # Just pick the first block from the grid to test
            numCells = self.grid.blocks[0].getNumCells()
            handler.root_add_val("Number of cells", numCells, tol=0)

    def train_getNumCells(self):
        self.test_getNumCells(train=True)

    def test_getNumNodes(self, train=False):
        refFile = os.path.join(baseDir, "ref", "block_getNumNodes.ref")
        with BaseRegTest(refFile, train=train) as handler:
            # Just pick the first block from the grid to test
            numCells = self.grid.blocks[0].getNumNodes()
            handler.root_add_val("Number of nodes in the first block", numCells, tol=0)

    def train_getNumNodes(self):
        self.test_getNumNodes(train=True)
