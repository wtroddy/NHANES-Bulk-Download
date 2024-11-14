# NHANES Bulk Download

This is a quick implementation to download NHANES data in bulk. 

## About

As far as I can tell, there is no way to do a bulk download of all NHANES datasets for a given cycle. I also cannot find a comprehensive list of all datasets in a release cycle from a single machine readable source. This utility helps with those problems.

I started developing this as a tool to download all of the data for another project, so it's not very feature rich but may add more capabilities and handling over time. Feel free to open an issue if something doesn't work. 

## Data File List

I couldn't find a machine readable list of all files, but it can be hacked. If you go to https://wwwn.cdc.gov/nchs/nhanes/search/default.aspx and search for:
- Search Term: SEQN
- Fields to Search: Variable Name
- Limited Access: Exclude
- Release Cycle: (Cycle you want to download)
- Result Page Size: MAX

This seems to give a result list that appears to be complete. These programs will accept this input table and use it to identify and download the files of interest.

See `data_file_lists/cycle_2017-2018.csv` as an example.

## Technical Setup  

This project was built with python 3.11.10. 

Example use:

```
conda create --name nhanes-download python=3.11
conda activate nhanes-download 
pip install -r requirements.txt
python ./src/nhanes_download.py
```