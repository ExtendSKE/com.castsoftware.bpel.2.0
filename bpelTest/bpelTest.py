import unittest
import cast.analysers.test


class BpelTest(unittest.TestCase):
    def testRegisterPlugin(self):
        analysis = cast.analysers.test.UATestAnalysis('BPEL')
        analysis.add_selection("TSTAPP")
        analysis.set_verbose()
        analysis.run()
if __name__ == "__main__":
    unittest.main()
