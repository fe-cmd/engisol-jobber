import requests
from bs4 import BeautifulSoup

#url = 'https://ng.indeed.com/jobs?q='+job+'&l='+location+'&sort=date'

titles = []
companies = []
summaries = []
links = []
dates = []

def job_data(url,items):
    res = requests.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    data = soup.find_all('div',class_='jobsearch-SerpJobCard')
    
    for i in data:
        
        title = i.find('h2',class_='title')
        
        if items[0] in title.text:
            company = i.find('span',class_='company')
            link = title.find('a')
            summary = i.find('div',class_='summary')
        
            date = i.find('span',class_='date')
            
            titles.append(title.text.strip())
            links.append('https://ng.indeed.com'+link['href'])
            companies.append(company.text.strip())
            dates.append(date.text.strip())
            summaries.append(summary.text.strip())
    
    return titles,companies,summaries,dates,links

#job_data(url)
                         