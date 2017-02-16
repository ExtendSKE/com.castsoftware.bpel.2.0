import unittest
import cast.analysers.test


class Test(unittest.TestCase):
    def testRegisterPlugin(self):
        # create a DotNet analysis
        analysis = cast.analysers.test.UATestAnalysis('BPEL')
        # DotNet need a selection of a csproj or sln
        analysis.add_selection('BPEL_Sample\Oracle_Samples')
        #analysis.result_file_path = 'C:\\Users\\ako\\Documents\\My Received Files\\com.castsoftware.bpel.1.0\\' + '_temp.uax'
        # analysis.add_database_table()
        analysis.set_verbose()
        analysis.run()
        
if __name__ == "__main__":
    unittest.main()
