gdp-lat
===================

This project is an analysis of the relationship between the
GDP and latitude of countries around the world.
 It contains 1) a Python script which scrapes data from Wikipedia
 using LXML, creates and merges data frames using Pandas,
 runs linear regression using statsmodels, and plots the data using
 Matplotlib, and 2) a paper describing the process and results.
 This was done for a class on Computational Economics.

Install
==========

First, install Python (I used 2.7.6), pip, and
 Latex (if you want to make the paper).

To install dependencies invoke
```
pip install lxml numpy pandas statsmodels matplotlib patsy
```

Run
====

To run the script, invoke
```
python gdp-lat.py
```
which will print the output of the regression, and generate
 figure/scatter.pdf.

To make the paper, go to paper/ and invoke
```
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

Warning
=========
This script works as of 12/24/2014, but is likely to break in the future
due to changes in the web pages being used as a data source.
