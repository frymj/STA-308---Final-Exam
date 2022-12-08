#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:58:03 2022

@author: matthewfry
"""
"""
Data Task:
The file gasoline_prices.csv Download gasoline_prices.csvcontains the state 
average gasoline prices for each state (and Washington, DC) in the United 
States on November 29, 2022 according to AAA. The file state_abb_codes.csv 
state_abb_codes.csvprovides a mapping of states & districts in the United 
States with their abbreviations, and the file censusRegions.csv 
censusRegions.csvprovides a mapping of states and districts based on 
census regions. 

For each of the census regions, compute the mean state (that is, remove 
Washington, D.C.) percentage increase (difference) in the price of Diesel 
vs Regular gasoline ( (Diesel - Regular)/Regular*100), along with the 
corresponding standard deviation and coefficient of variation . The result 
of your program should be a table of numbers with 4 rows (corresponding 
to the four census regions) and 3 columns of calculated values (the mean, 
standard deviation and coefficient of variation) [note: your output may 
be 4 columns if you include/consider census regions).

Takeaways from instructions:
    Compute the mean percentage increase in the price of Regular vs Diesel by 
    state
    Remove Washington DC
    Group states by census region
    Also compute standard deviation and coefficient of variation

Website for fuel prices by state: "https://tjfisher19.github.io/data/gasoline_prices.csv"
Website for state abbreviations: "https://tjfisher19.github.io/data/state_abb_codes.csv"
Website for census regions: "https://tjfisher19.github.io/data/censusRegions.csv"

"""
#%%
import numpy as np
import pandas as pd

# Reading all three data sets

FuelPriceStateDF = pd.read_csv("https://tjfisher19.github.io/data/gasoline_prices.csv")
StateAbbrevsDF = pd.read_csv("https://tjfisher19.github.io/data/state_abb_codes.csv")
CensusRegionsDF = pd.read_csv("https://tjfisher19.github.io/data/censusRegions.csv")

#%%
## Now that the data is read in, I am going to select the data I need from
##  the first data set in order to reduce the amount of unnecessary 
##  information in my final data frame and find the percent difference in 
##  price from Diesel to Regular

FuelPriceStateDF = FuelPriceStateDF.loc[:, ['State', 'Regular', 'Diesel']]
## The above line selects the columns State, Regular, and Diesel

FuelPriceStateDF = FuelPriceStateDF.assign(
    Pct_PriceDiff = (FuelPriceStateDF.Diesel - FuelPriceStateDF.Regular)/FuelPriceStateDF.Regular *100)
## The above line(s) creates a new column, Pct_PriceDiff, which represents
##  the price increase from regular to diesel

FuelPriceStateDF = FuelPriceStateDF[FuelPriceStateDF.State != "District of Columbia"]
## The above line removes Washington DC since it is not a state and does not
##  have a region associated with it

StateAbbrevsDF = StateAbbrevsDF.loc[:, ['State', 'Code']]
## The above line selects the columns State and Code

StatesWithCodes = FuelPriceStateDF.merge(StateAbbrevsDF, left_on = 'State',
                                         right_on = 'State')
## The above line(s) merges the data set containing the percent price 
##  difference and the state codes which will correspond to the states'
##  region in the final data set

StatesWithCodes = StatesWithCodes.loc[:, ['Code', 'Pct_PriceDiff']]
## The above line of code selects the Code and Pct_PriceDiff columns,
##  once again, to reduce unnecessary data in the data frame

PriceDiffWithRegion = StatesWithCodes.merge(CensusRegionsDF, 
                                            left_on = 'Code', 
                                            right_on = 'State')
## The above line(s) of code merges the census regions data frame with
##  the data frame containing states' codes that will correspond to a region
##  allowing me to group by region, thereby allowing me to acquire statistics
##  based on region

StatsByRegion = PriceDiffWithRegion.groupby("Region").agg({"Pct_PriceDiff": ["mean", "std"]})

cv = PriceDiffWithRegion.groupby("Region").agg({"Pct_PriceDiff": "std"})/PriceDiffWithRegion.groupby("Region").agg({"Pct_PriceDiff": "mean"})*100
cv = cv.assign(CoeffOfVar = PriceDiffWithRegion.groupby("Region").agg({"Pct_PriceDiff": "std"})/PriceDiffWithRegion.groupby("Region").agg({"Pct_PriceDiff": "mean"})*100)
cv = cv.loc[:, 'CoeffOfVar']
## I'm sure there was a better way of finding and aggregating the Coefficient
##  of Variation but after hours of trying I resorted to this and it finally
##  worked. So, I merged the database "cv" with my StatsByRegion database for
##  the desired final output (below).

StatsByRegion = StatsByRegion.merge(cv, left_on = "Region", right_on = "Region")
print(StatsByRegion)

"""
See you next semester Dr. Fisher. Don't do anything I wouldn't
"""