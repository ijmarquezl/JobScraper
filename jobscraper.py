#!/usr/bin/python3
"""Script for Webscraping Job Boards."""

import json
from mongo_dbhelper import DBHelper as dbh
from webobject import WebObject as WO

# First we initialize the Object
wo = WO()

# Next we define some labels for the different boards
# INDEED
row_div = "row"
jtattrs = {'data-tn-element': 'jobTitle'}  # Attribute of <a>
jt = 'title'  # Index of jobTitle array
compattrs = {'class': 'company'}  # First possible classname
rlsattrs = {'class': 'result-link-source'}  # Second possible classname
salparam = 'nobr'  # Salary param for find
sjclparam = {'class': 'sjcl'}  # Div class attribute for second try Salary
sumspan = {'class': 'summary'}  # Span attribute summary
locspan = {'class': 'location'}  # Span attribute location

# We now get the data from the job board
query = 'q=Software+Development+manager'
loc = 'l=Dallas%2C+TX'
url = 'https://www.indeed.com/jobs?'
url = url + query + '&' + loc
page = wo.getURLContents(url)
soup = wo.soup

# Results containers
jobs = []
salaries = []
companies = []
locations = []
summaries = []
hrefs = []

for div in wo.getByDiv(row_div, soup):
    for a in wo.getByA(jtattrs, div):
        jobs.append(a[jt])
    try:
        salaries.append(wo.find(salparam, div).text)
    except Exception:
        try:
            div_two = wo.find(sjclparam, div, "div")
            div_three = div_two.find("div")
            salaries.append(div_three.text.strip())
        except Exception:
            salaries.append("Nothing_found")
    company = wo.getBySpan(compattrs, div)
    if len(company) > 0:
        for b in company:
            companies.append(b.text.strip())
    else:
        sec_try = wo.getBySpan(rlsattrs, div)
        for span in sec_try:
            companies.append(span.text.strip())
spans = wo.getBySpan(locspan, soup)
for span in spans:
        locations.append(span.text)
spans = wo.getBySpan(sumspan, soup)
for span in spans:
    summaries.append(span.text.strip())

db = dbh('JobsBase')

for i in range(len(jobs)):
    resultsdict = {"jobboard": 'Indeed.com', "searchterm": query, "jobtitle": jobs[i], "company": companies[i], "salary": salaries[i], "localtion": locations[i], "summary": summaries[i]}
    jsonRes = json.dumps(resultsdict)
    res = db.dbInsert('jobBoards', resultsdict)
    type(res)
    print(jsonRes)
