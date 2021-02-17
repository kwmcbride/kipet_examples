# Standard library imports
from pathlib import Path
import subprocess
import sys
import time
import unittest


class TestExamples(unittest.TestCase):
    """Test to check if all of the example problems are working properly"""
    
    def setUp(self):
        self.dir_examples = Path.cwd().joinpath('examples')
        self.files = list(self.dir_examples.rglob("*.py"))
        self.std_out = open("test_examples.log", "w")

    def tearDown(self):
        self.std_out.close()

    def test_examples(self):
        
        grades = {}
        flagpy = 0
        countpy = 0
        flagps = 0
        
        print('Testing the example problems in folder: examples')
        number_of_examples = len(self.files)
        print(f'There are {number_of_examples} example problems to be evaluated')
        
        for n, file in enumerate(self.files):
            
            file = Path(file)
            margin = 10
            print(f'Running example ({n + 1}/{number_of_examples}):\n')
            print('File'.rjust(margin) + f' : {file.stem}')
                  
            start = time.time()
            flagpy = subprocess.call([sys.executable, file,'1'],
                                stdout=self.std_out,
                                stderr=subprocess.STDOUT)
            end = time.time()
            
            if flagpy!=0: 
                print('Status'.rjust(margin) + f' : Fail\n')
                countpy = countpy + 1
                flagpy=1
                flagps=1
                grades[file.stem] = False 
                
            else:
                print('Status'.rjust(margin) + f' : Pass')
                print('Time'.rjust(margin) + f' : {end-start:0.4f}\n')
                grades[file.stem] = True
                
            print('Results'.rjust(margin) + f' : P: {n + 1 -countpy} | F: {countpy} | T: {n + 1} | R: {(n + 1 -countpy)/(n + 1):0.2f}%\n')
            continue
        
        print(f'{countpy} files in {self.dir_examples} failed:')
        for file, grade in grades.items():
            if not grade:
                print(f'\t{file}')
            
        self.assertEqual(int(flagpy), 0) 
        self.assertEqual(int(flagps), 0)

        return grades

if __name__ == '__main__':
    
    unittest.main()