import urllib2
import re

import lxml.html as html
import lxml.etree as etree
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def lat_gdp_exp():
    """Scrapes latitude and gdp data, runs linear regression and plots the data"""

    lat_gdp = make_gdp_lat_frame()
    #lat_gdp.to_csv("data/lat_gdp.csv")

    #if make_gdp_lat_frame() doesn't work, then you can read
    #from a cached csv file
    #lat_gdp = pd.read_csv("data/lat_gdp.csv")

    #do linear regression, using latitude to predict gdp
    X = lat_gdp[["latitude"]]
    y = lat_gdp["gdp"]
    
    #add constant column for bias term
    X = sm.add_constant(X, prepend=False)
    model = sm.OLS(y, X)
    results = model.fit()
    print results.summary()

    #plot gdp vs. latitude
    plt.plot(lat_gdp["latitude"], lat_gdp["gdp"], 'ro')
    plt.plot(lat_gdp["latitude"], results.fittedvalues, 'b')
    plt.xlabel("| latitude |")
    plt.ylabel("gdp")
    plt.savefig("paper/scatter.pdf")

def make_gdp_lat_frame():
    """Makes a DataFrame where the rows are countries, lats, and gdps"""

    #get data
    gdp = make_gdp_frame()
    n_lat = make_lat_frame(is_north=True)
    s_lat = make_lat_frame(is_north=False)

    #create a single DataFrame with north and south lats
    lat = pd.merge(n_lat, s_lat, on="country")

    #get the abs val of the mean of the lats and put it in a new DataFrame
    mean_lat = lat[["n_lat","s_lat"]].mean(1).abs()
    mean_lat = pd.DataFrame({"country":lat["country"],
                             "latitude":mean_lat})
    lat_gdp = pd.merge(mean_lat, gdp, on="country")
    return lat_gdp
    
def make_gdp_frame():
    """Make a DataFrame with country and gdp columns using data from Wikipedia"""
    
    url = "http://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita"
    root = html.parse(url)

    country_gdp_list = []

    rows = root.xpath("//table[1]//table[1]//tr")
    for r in rows:
        country = r.xpath("./td[2]//text()")
        gdp = r.xpath("./td[3]//text()")
        if len(country) > 1 and len(gdp) > 0:
            country = country[1]
            gdp = int(gdp[0].replace(",", ""))
            country_gdp_list.append((country, gdp))

    gdp_frame = pd.DataFrame(country_gdp_list, columns=["country", "gdp"])
    return gdp_frame

def pp(x):
    print etree.tostring(x, pretty_print=True)

def make_lat_frame(is_north):
    """Makes a DataFrame with a country and a n_lat (northernmost latitude) or s_lat column depending on the value of is_north"""

    if is_north:
        col_name = "n_lat"
        url = "http://en.wikipedia.org/wiki/List_of_countries_by_northernmost_point"
        table_xpath = "//div[@id=\'mw-content-text\']/table[1]/tr"
    else:
        col_name = "s_lat"
        url = "http://en.wikipedia.org/wiki/List_of_countries_by_southernmost_point"
        table_xpath = "//div[@id=\'mw-content-text\']/table[2]/tr"

    root = html.parse(url)
    country_lat_list = []
    rows = root.xpath(table_xpath)[1:]

    for r in rows:
        cols = r.xpath("./td")
        if len(cols) == 4:
            country = r.xpath("./td[2]//text()")[1]
            lat = r.xpath("./td[4]//text()")[0]
            
            #get the degree and if it's south, negate it
            split_lat = re.findall("[0-9NS]+", lat)
            lat = int(split_lat[0])
            ns = split_lat[-1]
            if ns == "S":
                lat = -lat
            country_lat_list.append((country, lat))

    lat_frame = pd.DataFrame(country_lat_list, columns=["country", col_name])
    return lat_frame

def test():
    print make_gdp_frame()
    print make_lat_frame(is_north=True)
    print make_lat_frame(is_north=False)

if __name__ == "__main__":
    #test()
    lat_gdp_exp()
