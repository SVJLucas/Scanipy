from pyarxiv import query, download_entries
from pyarxiv.arxiv_categories import ArxivCategory, arxiv_category_map
import requests
import os
import pandas as pd

def choose_topic(topic, max_results):
    # Perform the arXiv API query with the 'max_results' parameter
    entries = query(title=topic, max_results=max_results)
    
    # Pull title, author, date, and link to PDF of paper from "entries"
    # and put each in its own list

    titles = map(lambda x: x['title'], entries)
    authors = map(lambda x: x['author'], entries)
    updated = map(lambda x: x['updated'], entries)
    links = map(lambda x: x['link'], entries)

    # Create an empty dataframe called "papers"
    papers = pd.DataFrame()

    # Insert columns into "papers" from the previously created lists

    papers['Title'] = pd.Series(titles)
    papers['Author'] = pd.Series(authors)
    papers['Updated'] = pd.Series(updated)
    papers['Link'] = pd.Series(links)

    # Slice HH:MM:SS off of each row in the date column

    papers['Updated'] = papers['Updated'].str.slice(stop = 10)

    # Reformat URL string to take the user to the PDF of the paper

    papers['Link'] = papers['Link'].str.replace("abs", "pdf", case = True)

    # Sort the dataframe in descending order by date

    papers = papers.sort_values(by = 'Updated', ascending = False).reset_index(drop = True).head(max_results)
    
    # Calculate the number of rows in the "papers" DataFrame
    num_rows = len(papers)
    print("Number of papers:", num_rows)
    
    return papers
