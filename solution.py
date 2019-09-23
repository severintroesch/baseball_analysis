# -*- coding: utf-8 -*-
"""
CAS Inf Eng - Module Scripting

SOLUTION TO ASSIGNMENT 4.4: *Grammer of Graphics for Baseball Data*

@author: severin troesch

GOAL OF ANALYSIS:
    To get data from the major league baseball (MLB) from the internet and to 
    visualize certain features of interest using the "grammar of graphics".

PACKAGES USED:
    - pybaseball    (for scraping of baseball-data)
    - plotnine      (for grammar of graphics)

"""

#%% importing packages

## baseball-module
from pybaseball import pitching_stats
from pybaseball import statcast

## grammar of graphics module
from plotnine import *

## further modules
from datetime import date


#%% get data 

today = date.today() #today as reference


## first, standard pitching stats for last 5 years
end_1 = today.year
start_1 = today.year - 5 #year as integer

pitching = pitching_stats(start_1, end_1) #takes a while

# give sucess-message and summary stats of data set
print()
print("Sucessfully sampled pitching stats of the last 5 years:")
print()
#list(pitching.columns) #list variable names
pitching.describe() #summary stats of pitching data frame


## then, more detailed pitching stats for last month

# date of one month ago - be careful current day is 31st
if today.month - 1 == 0: #check if its january
    one_month_ago = today.replace(month = 12) #if january
else:
    one_month_ago = today.replace(month = today.month -1)
     
     
pitching_last_month =  statcast(start_dt=str(one_month_ago), end_dt=str(today)) 

# give sucess-message and summary stats of data set
print()
print("Sucessfully sampled statcast-stats of the last month:")
print()
list(pitching_last_month.columns) #list variable names
pitching_last_month.describe() #summary stats of pitching data frame

# explanation of statcast variables: http://m.mlb.com/glossary/statcast


#%% plotting:

## now build a cool plot using the data (with grammer of graphics)

# build a homerun-variable:
pitching_last_month['hr'] = pitching_last_month.events=='home_run'

# then, get rid of NAs in relevant variables 
pitching_last_month_2 = pitching_last_month.dropna(subset=['launch_angle', 'launch_speed', 'estimated_ba_using_speedangle', 'hr'])


# and finally, the plot: at which pitch speeds and angles are home runs hit?
(ggplot(pitching_last_month_2, aes(x="launch_speed", 
                                   y="launch_angle", 
                                   color = "hr"))
 + geom_point())
    

# additionally, the analysis cad be done and plotted individually by the type of pitch:
(ggplot(pitching_last_month_2, aes(x="launch_speed", 
                                   y="launch_angle", 
                                   color = "hr"))
 + geom_point()
 + facet_wrap('~pitch_type'))    #important "wrap" feature of the package

    
    
print("LOOKS COOL ;-)")


    