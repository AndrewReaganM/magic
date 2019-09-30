# Timing Documentation

This is an experiment for testing the timing of pseudo-random number generators. The script for testing the timing will test a series of specified sites and output the timing results.

## Input file

The input file for the testing script timingexperiment.py is a YAML file that inclues each site in the specified form shown below:

[Region]_[zone]_[VM|app]_[Java|Python]@1.2.3.4
  
 An example of an input file can be found at <magic/timing_experiment/external_sites.yaml>.
 
 ## Output file
 
The script, timingexperiment.py will produce an output file which includes the timing results for each of the sites included in the input YAML file. 
If an error occurs when testing a site, an error message of the form "ERROR on [Region]_[zone]_[VM|app]_[Java|Python]@1.2.3.4" will be logged. 

The output for each site is in the form specified below:
 
[Region]_[zone]_[VM|app]_[Java|Python]@1.2.3.4 time_in_milliseconds random_number_generated
  
The resulting output file produced from the input file mentioned in the "Input file" section of this document can be found at <magic/timing_experiment/outputfile.txt>.
  
## Instructions and Dependencies

Python 3 is required. Be sure that the input file sites.yaml is updated with the target sites to be tested.

Run the following command.
 ```Python
python3 timingexperiment.py
```

After, outputfile.txt should be produced. 

## Example step by step

### Change to the timing_experiment directory.

```bash
Melissas-MacBook-Pro-2:~ melissawilson$ cd Documents/GitHub/magic/timing_experiment/
```
### Run the script.

```bash
Melissas-MacBook-Pro-2:timing_experiment melissawilson$ python3 timingexperiment.py
```
