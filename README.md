## Chronological-ASX-News-Aggregator_MarketPulse

#Overview:

Market Pulse is a Python-powered financial news aggregator that collects market-related articles from multiple Australian financial news providers and presents them in a single, easy-to-read timeline.
Rather than visiting several websites individually, users can view the latest headlines, article summaries, and publication times in one place. Market Pulse standardizes news data from different sources, sorts articles chronologically, and provides direct links back to the original publishers for full article reading and source attribution.
The project is designed to provide a faster and more efficient way to monitor market-moving news while respecting publishers by directing users to the original content.

#Features:

Aggregates news from multiple Australian financial news sources.
Collects article titles, summaries, publication dates, and source links.
Standardizes article information into a consistent format regardless of source.
Converts publication times into sortable datetime values for accurate chronological ordering.
Handles both absolute dates and relative timestamps.
Removes duplicate articles where appropriate.
Displays all results through a clean and lightweight NiceGUI interface.
Provides direct links to original articles for further reading.
Creates a single timeline of market news from multiple publishers.

#Supported Sources:


-AFR Markets

-Livewire Markets

-Market Index


Additional sources can be added by creating new scraper modules that conform to the existing article structure.


#How It Works:

Market Pulse retrieves the latest articles from supported news providers and extracts key article information, including:

-Headline

-Publication date and time

-Article summary

-Source URL

Each article is then standardized into a common structure, allowing information from different websites to be combined seamlessly.
Dates are normalized into a consistent format so articles can be accurately ordered from newest to oldest regardless of their original source.
The finalized article collection is then displayed through the NiceGUI interface, allowing users to browse the latest market news and open original articles directly from their source.

#Libraries Used:

-curl_cffi

-Beautiful Soup (beautifulsoup4)

-NiceGUI

-datetime

#Installation:

Install the required Python dependencies and run the application.

#Project Goals:

The primary goal of Market Pulse is to provide a centralized view of Australian financial news without requiring users to monitor multiple websites independently.




#Disclaimer:

Market Pulse is a news aggregation tool and does not republish full articles. All article content remains the property of its respective publisher.
Users are provided with article metadata and links to the original sources, where full content can be accessed according to each publisher's terms and conditions.
