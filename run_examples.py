# Standard library imports
from pathlib import Path
import subprocess
import sys
import time
import unittest


class TestExamples(unittest.TestCase):
    """Test to check if all of the example problems are working properly"""
    
    def setUpClass(self):
        self.dir_examples = Path.cwd().joinpath('examples')
        self.files = list(self.dir_examples.rglob("*.py"))
        self.std_out = open("test_examples.log", "w")

    def tearDownClass(self):
        self.std_out.close()

    def test_examples(self):
        
        grades = {}
        flagpy = 0
        countpy = 0
        flagps = 0
        
        print('Testing the example problems in kipet_examples repository')
        number_of_examples = len(self.files)
        print(f'There are {number_of_examples} example problems to be evaluated')
        
        for n, file in enumerate(self.files):
            
            file = Path(file)
            print(f'Running tutorial example ({n + 1}/{number_of_examples}): {file.stem}')
            
            start = time.time()
            flagpy = subprocess.call([sys.executable, file,'1'],
                                stdout=self.std_out,
                                stderr=subprocess.STDOUT)
            end = time.time()
            
            if flagpy!=0: 
                print(f"\n\t #### {file.stem} FAILED ####\n")
                countpy = countpy + 1
                flagpy=1
                flagps=1
                grades[file.stem] = False 
                
            else:
                print(f"\n\t #### {file.stem} PASSED {end-start:0.4f} seconds ####\n")
                grades[file.stem] = True
                
            continue
        
        print(f'{countpy} files in {self.dir_examples} failed')
        print(grades)
        
        self.assertEqual(int(flagpy), 0) 
        self.assertEqual(int(flagps), 0)

        

        return grades

if __name__ == '__main__':
    
    unittest.main()
