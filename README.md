Baku Hotel Analysis Project


This project is a comprehensive analysis of hotels in Baku, Azerbaijan, based on real hotel data and synthetic guest and review data. The analysis helps uncover guest preferences, satisfaction scores, and key insights to improve hotel offerings and enhance guest experiences. The data has been collected, cleaned, analyzed, and visualized using a combination of Python, SQL, and Qlik Sense.


Hotels Data: Contains detailed information about 140 hotels in Baku, including their names, star ratings, amenities, room counts, and distance from major landmarks such as the airport and city center.

Hotel Guests: Contains synthetic guest data for 3,705 guests, including demographics, booking information, and guest types (e.g., repeat guests, first-time guests).

Hotel Reviews: Contains synthetic review data for over 3,500 reviews across the hotels, with ratings for different categories such as room comfort, service quality, cleanliness, and an overall review score.

Analysis Goals of this project are:

To understand the preferences of hotel guests in Baku.
To provide actionable insights for hotels on how to improve their services and attract more guests.
To visualize trends in guest reviews, satisfaction levels, and hotel amenities.
To determine how factors like distance to the city center or airport impact guest ratings.
Tech Stack
This project utilizes the following tools and technologies:

Python (for data scraping, cleaning, and processing)

SQL (for storing and querying the data in Oracle SQL)

Qlik Sense (for data visualization and dashboard creation)

Pandas (for data manipulation)

BeautifulSoup & Selenium (for web scraping)



Installation
To run the project locally:

Clone the repository:

bash
Copy code

git clone https://github.com/yourusername/baku-hotel-analysis.git
cd baku-hotel-analysis



Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Set up the SQL database: Load the dataset into your Oracle SQL or any preferred database management system.

Run the analysis scripts: Use the Python scripts in the scripts/ folder to process data, clean, and prepare it for visualization.

Qlik Sense: Open the provided Qlik Sense files to explore the interactive dashboards created as part of this analysis.

Usage
After setting up the project, you can:

Scrape hotel and review data using the provided scraping scripts.
Analyze guest data using SQL queries and Python scripts.
Visualize key insights through the Qlik Sense dashboard.
Example:
Hotel Performance: See how guest satisfaction varies across hotels based on location, amenities, and room rates.
Guest Demographics: Analyze trends in guest nationality, booking lead time, and preferences for repeat guests.
Visualizations
Key visualizations in the project include:

Pie charts showing guest nationality distribution and hotel renovation age.
Bar charts showing hotel review scores and guest satisfaction levels.
Scatter plots correlating guest count with hotel distance from the city center and airport.
Treemaps displaying hotel amenities and how they affect overall ratings.
License
This project is licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:

arduino
Copy code
http://www.apache.org/licenses/LICENSE-2.0
Feel free to replace yourusername in the git clone section with your actual GitHub username once you create the repository. Let me know if you need help with anything else!
