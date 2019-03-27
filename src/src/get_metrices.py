import os
import re
import shlex
import sys
import pandas as pd
import numpy as np
from glob2 import glob, iglob
import subprocess as sp
from pathlib import Path
from pdb import set_trace
from collections import defaultdict
import os
import platform
from os.path import dirname as up
import json

class MetricsGetter(object):

    def __init__(self,path):
        self.path = path #get the repo path
        # Reference current directory, so we can go back after we are done.
        self.cwd = Path(os.getcwd())
        self.json_file_path = self.cwd.joinpath(".temp", "json")
        # Create a folder to hold the json files
        try:
            if not self.json_file_path.is_dir():
                os.makedirs(self.json_file_path)
        except:
            sys.stderr.write(str("There is an error creating dir"))

    @staticmethod
    def _os_cmd(cmd, verbose=True):
        """
        Run a command on the shell

        Parameters
        ----------
        cmd: str
            A command to run.
        """
        cmd = shlex.split(cmd)
        with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE) as p:
            out, err = p.communicate()
        if verbose: #print to std error which goes to log when running in cloud
            sys.stderr.write(str("\n"))
            sys.stderr.write(str(out))
            sys.stderr.write(str("\n"))
            sys.stderr.write(str(err))
        return out, err

    def get_metrics(self):
        # Create the path for the json file
        json_file = self.json_file_path.joinpath("out.json")
        # Create the complexity report command the data is in json format and stored in to out.json file
        cmd = "cr --format json --output {} {}".format(
                str(json_file), str(self.path))
        self._os_cmd(cmd)

        # Read into a pandas df
        df = pd.read_json(json_file)
        file_complexity = []
        for i in range(df.shape[0]):
            #Aggregate
            aggregate_sloc_logical = df.iloc[i,0]['aggregate']['sloc']['logical']
            aggregate_sloc_physical = df.iloc[i,0]['aggregate']['sloc']['physical']
            aggregate_cyclomatic = df.iloc[i,0]['aggregate']['cyclomatic']
            aggregate_halstead_operators_distinct = df.iloc[i,0]['aggregate']['halstead']['operators']['distinct']
            aggregate_halstead_operators_total = df.iloc[i,0]['aggregate']['halstead']['operators']['total']
            aggregate_halstead_operands_distinct = df.iloc[i,0]['aggregate']['halstead']['operands']['distinct']
            aggregate_halstead_operands_total = df.iloc[i,0]['aggregate']['halstead']['operands']['total']
            aggregate_halstead_length = df.iloc[i,0]['aggregate']['halstead']['length']
            aggregate_halstead_vocabulary = df.iloc[i,0]['aggregate']['halstead']['vocabulary']
            aggregate_halstead_difficulty = df.iloc[i,0]['aggregate']['halstead']['difficulty']
            aggregate_halstead_volume = df.iloc[i,0]['aggregate']['halstead']['volume']
            aggregate_halstead_effort = df.iloc[i,0]['aggregate']['halstead']['effort']
            aggregate_halstead_bugs = df.iloc[i,0]['aggregate']['halstead']['bugs']
            aggregate_halstead_time = df.iloc[i,0]['aggregate']['halstead']['time']
            aggregate_params = df.iloc[i,0]['aggregate']['params']
            aggregate_line = df.iloc[i,0]['aggregate']['line']
            aggregate_cyclomaticDensity = df.iloc[i,0]['aggregate']['cyclomaticDensity']
            #Dependency
            file_count_dependencies = len(df.iloc[i,0]['dependencies'])
            #maintainability
            file_maintainability = df.iloc[i,0]['maintainability']
            #loc
            file_loc = df.iloc[i,0]['loc']
            #cyclomatic
            file_cyclomatic = df.iloc[i,0]['cyclomatic']
            #effort
            file_effort = df.iloc[i,0]['effort']
            #params
            file_params = df.iloc[i,0]['params']
            #path
            file_path = df.iloc[i,0]['path'].split(self.path,1)[1]
            #function
            total_function_sloc_logical = 0
            total_function_sloc_physical = 0
            total_function_cyclomatic = 0
            total_function_halstead_operators_distinct = 0
            total_function_halstead_operators_total = 0
            total_function_halstead_operands_distinct = 0
            total_function_halstead_operands_total = 0
            total_function_halstead_length = 0
            total_function_halstead_vocabulary = 0
            total_function_halstead_difficulty = 0
            total_function_halstead_volume = 0
            total_function_halstead_effort = 0
            total_function_halstead_bugs = 0
            total_function_halstead_time = 0
            total_function_params = 0
            total_function_line = 0
            total_function_cyclomaticDensity = 0
            # Numer of function
            if len(df.iloc[i,0]['functions']) == 0:
                num_function = 1
            else:
                num_function = len(df.iloc[i,0]['functions'])
                for j in range(num_function):
                    total_function_sloc_logical += df.iloc[i,0]['functions'][j]['sloc']['logical']
                    total_function_sloc_physical += df.iloc[i,0]['functions'][j]['sloc']['physical']
                    total_function_cyclomatic += df.iloc[i,0]['functions'][j]['cyclomatic']
                    total_function_halstead_operators_distinct += df.iloc[i,0]['functions'][j]['halstead']['operators']['distinct']
                    total_function_halstead_operators_total += df.iloc[i,0]['functions'][j]['halstead']['operators']['total']
                    total_function_halstead_operands_distinct += df.iloc[i,0]['functions'][j]['halstead']['operands']['distinct']
                    total_function_halstead_operands_total += df.iloc[i,0]['functions'][j]['halstead']['operands']['total']
                    total_function_halstead_length += df.iloc[i,0]['functions'][j]['halstead']['length']
                    total_function_halstead_vocabulary += df.iloc[i,0]['functions'][j]['halstead']['vocabulary']
                    total_function_halstead_difficulty += df.iloc[i,0]['functions'][j]['halstead']['difficulty']
                    total_function_halstead_volume += df.iloc[i,0]['functions'][j]['halstead']['volume']
                    total_function_halstead_effort += df.iloc[i,0]['functions'][j]['halstead']['effort']
                    total_function_halstead_bugs += df.iloc[i,0]['functions'][j]['halstead']['bugs']
                    total_function_halstead_time += df.iloc[i,0]['functions'][j]['halstead']['time']
                    total_function_params += df.iloc[i,0]['functions'][j]['params']
                    total_function_line += df.iloc[i,0]['functions'][j]['line']
                    if df.iloc[i,0]['functions'][j]['cyclomaticDensity'] is None:
                        total_function_cyclomaticDensity += 0
                    else:
                        total_function_cyclomaticDensity += df.iloc[i,0]['functions'][j]['cyclomaticDensity']
            #Avg metric
            avg_function_sloc_logical = total_function_sloc_logical/num_function
            avg_function_sloc_physical = total_function_sloc_physical/num_function
            avg_function_cyclomatic = total_function_cyclomatic/num_function
            avg_function_halstead_operators_distinct = total_function_halstead_operators_distinct/num_function
            avg_function_halstead_operators_total = total_function_halstead_operators_total/num_function
            avg_function_halstead_operands_distinct = total_function_halstead_operands_distinct/num_function
            avg_function_halstead_operands_total = total_function_halstead_operands_total/num_function
            avg_function_halstead_length = total_function_halstead_length/num_function
            avg_function_halstead_vocabulary = total_function_halstead_vocabulary/num_function
            avg_function_halstead_difficulty = total_function_halstead_difficulty/num_function
            avg_function_halstead_volume = total_function_halstead_volume/num_function
            avg_function_halstead_effort = total_function_halstead_effort/num_function
            avg_function_halstead_bugs = total_function_halstead_bugs/num_function
            avg_function_halstead_time = total_function_halstead_time/num_function
            avg_function_params = total_function_params/num_function
            avg_function_line = total_function_line/num_function
            avg_function_cyclomaticDensity = total_function_cyclomaticDensity/num_function
            #Create Dataframe
            file_complexity.append([file_path,aggregate_sloc_logical,aggregate_sloc_physical,aggregate_cyclomatic,
                                aggregate_halstead_operators_distinct,aggregate_halstead_operators_total,
                                aggregate_halstead_operands_distinct,aggregate_halstead_operands_total,
                                aggregate_halstead_length,aggregate_halstead_vocabulary,aggregate_halstead_difficulty,
                                aggregate_halstead_volume,aggregate_halstead_effort,aggregate_halstead_bugs,
                                aggregate_halstead_time,aggregate_params,aggregate_line,aggregate_cyclomaticDensity,
                                file_count_dependencies,file_maintainability,file_loc,file_cyclomatic,
                                file_effort,file_params,avg_function_sloc_logical,avg_function_sloc_physical,
                                avg_function_cyclomatic,avg_function_halstead_operators_distinct,
                                avg_function_halstead_operators_total,avg_function_halstead_operands_distinct,
                                avg_function_halstead_operands_total,avg_function_halstead_length,
                                avg_function_halstead_vocabulary,avg_function_halstead_difficulty,
                                avg_function_halstead_volume,avg_function_halstead_effort,avg_function_halstead_bugs,
                                avg_function_halstead_time,avg_function_params,avg_function_line,avg_function_cyclomaticDensity,
                                total_function_sloc_logical,total_function_sloc_physical,total_function_cyclomatic,
                                total_function_halstead_operators_distinct,total_function_halstead_operators_total,
                                total_function_halstead_operands_distinct,total_function_halstead_operands_total,
                                total_function_halstead_length,total_function_halstead_vocabulary,
                                total_function_halstead_difficulty,total_function_halstead_volume,total_function_halstead_effort,
                                total_function_halstead_bugs,total_function_halstead_time,total_function_params,
                                total_function_line,total_function_cyclomaticDensity])

        cleared_df = pd.DataFrame(file_complexity, columns = ['file_path','aggregate_sloc_logical','aggregate_sloc_physical','aggregate_cyclomatic',
                          'aggregate_halstead_operators_distinct','aggregate_halstead_operators_total',
                         'aggregate_halstead_operands_distinct','aggregate_halstead_operands_total',
                         'aggregate_halstead_length','aggregate_halstead_vocabulary','aggregate_halstead_difficulty',
                         'aggregate_halstead_volume','aggregate_halstead_effort','aggregate_halstead_bugs',
                         'aggregate_halstead_time','aggregate_params','aggregate_line','aggregate_cyclomaticDensity',
                         'file_count_dependencies','file_maintainability','file_loc','file_cyclomatic',
                         'file_effort','file_params','avg_function_sloc_logical','avg_function_sloc_physical',
                          'avg_function_cyclomatic','avg_function_halstead_operators_distinct',
                         'avg_function_halstead_operators_total','avg_function_halstead_operands_distinct',
                         'avg_function_halstead_operands_total','avg_function_halstead_length',
                         'avg_function_halstead_vocabulary','avg_function_halstead_difficulty',
                         'avg_function_halstead_volume','avg_function_halstead_effort','avg_function_halstead_bugs',
                         'avg_function_halstead_time','avg_function_params','avg_function_line','avg_function_cyclomaticDensity',
                         'total_function_sloc_logical','total_function_sloc_physical','total_function_cyclomatic',
                         'total_function_halstead_operators_distinct','total_function_halstead_operators_total',
                         'total_function_halstead_operands_distinct','total_function_halstead_operands_total',
                         'total_function_halstead_length','total_function_halstead_vocabulary',
                         'total_function_halstead_difficulty','total_function_halstead_volume','total_function_halstead_effort',
                         'total_function_halstead_bugs','total_function_halstead_time','total_function_params',
                         'total_function_line','total_function_cyclomaticDensity'])
        cleared_df.set_index(keys = 'file_path', inplace = True)
        cleared_df.dropna(axis = 0,how='any',inplace = True) 
        
        # Creating result in r2c format
        result = {}
        result["check_id"] = 'complexity'
        result["path"] = 'javaScript'
        result["extra"] = cleared_df.to_dict(orient='index')
        final_result = {"results": [result]}
        result_json = json.dumps(final_result) 
        #printing to get the data into the shell script
        print(result_json)             

        return result_json


if __name__ == "__main__":
    metrics = MetricsGetter(sys.argv[1])
    metrics.get_metrics()






