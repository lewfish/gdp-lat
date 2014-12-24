gdp-lat
===================

A Python script to examine the relationship between the GDP and latitude of countries around the world. It scrapes data from Wikipedia using LXML, creates and merges data tables using Pandas, runs linear regression using statsmodels, and plots the data using Matplotlib. This was done for a class in Computational Economics.

To install dependencies invoke
```pip install lxml numpy pandas statsmodels matplotlib patsy```

This script works as of 12/24/2014, but is likely to break in the future
due to changes in the web pages being used as a data source.
