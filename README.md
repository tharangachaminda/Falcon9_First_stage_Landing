![Logo](https://github.com/tharangachaminda/Falcon9_First_stage_Landing/blob/main/Dash.png)

# SpaceX Falcon9 First Stage Landing Prediction - Analysis
![Logo](https://github.com/tharangachaminda/Falcon9_First_stage_Landing/blob/main/Dash.png)

SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch. In this lab, you will collect and make sure the data is in the correct format from an API. The following is an example of a successful and launch.

### Business Impact
Aerospace manufacturing is a very expensive process. According to SpaceX website, because of their approach of reusing stage 1 reduces the total cost from a significant amount. Therefore, these analysis and predictions will very useful for future projects of aerospace industry.

### Stackholders
For this project stackholders possibly be
- SpaceX
- NASA
- Aerospace manufacturers around the world

### Data Sources
SpaceX API: https://api.spacexdata.com/v4/

From this API, I fetch following data.
- Booster Versions
- Launch Site
- Payload Data
- Booster Versions
- Core Data
- Launch Data

Falcon 9 Wikipedia Page: 
- Old launches from 2010 - 2019 - https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2010%E2%80%932019)
- Latest launches 2020 to present date - https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches

### Technologies and Tools
I have used following tools and technologies for this project.
- **Python statistical libraries and Mathematical libraries** for data analysis
- SQL language
- SQlite
- [Folium](https://python-visualization.github.io/folium/) for interative Maps
- Various **Python libraries** to visualize different insights along the way
- [Plotly Dash](https://dash.plotly.com/) for interactive dashboard

### Analytic Techniques
1. **Descriptive Statistics** wil be used to derive valueable insights from the data.
2. Graphs ans Charts
3. Interactive Maps
4. Interactive Dashboard


## Installation

I have used [*sqlalchemy*](https://www.sqlalchemy.org/) as the database toolkit and [*geopy*](https://geopy.readthedocs.io/)  for measure distance between points on Folium maps. 

```bash
pip install sqlalchemy --user
pip install geopy --user
```
    
## 🏆 Lessons Learned

1. Plotly and Plotly Express
2. Plotly Dash conponents
3. Folium library for interactive geographical maps

## Demo
[Try it on my profile](http://ec2-34-215-236-233.us-west-2.compute.amazonaws.com/falcon9_dashboard)
