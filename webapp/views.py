from django.shortcuts import render
import requests
import bs4
import time
# Create your views here


def index(request):
	value = []
	if request.method == 'POST':
		form = request.POST['your_url']
		resp = requests.get(form)
		scrapval = bs4.BeautifulSoup(resp.text,"html.parser")
		for data in scrapval.find_all('img'):
			srcval = data.get('src')
			print(srcval)
			value.append(srcval)
   
	return render(request,'index.html',{'value':value})

def news(request):
    links = []
    context = {}
    toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
    toi_soup = bs4.BeautifulSoup(toi_r.content, 'lxml')

    toi_headings = toi_soup.find_all('h2')
    news = toi_soup.find_all('div', class_ = 'brief_box')
    # removing footer links
    toi_news = []

    for th in toi_headings:
        toi_news.append(th.text)
    
    for more in news:
        link = more.find('a')
        links.append(link)
    data = zip(links, toi_news)
    #Getting news from Hindustan times
    context = {
        'data':data
    }

    
    return render(request, 'news.html', context)


def jobs(request):
    companies = []
    dates = []
    skills = []
    links = []
    context = {}
    
    if request.method  == 'POST':
        title = request.POST['title']
        location = request.POST['location']
        html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords='+title+'&txtLocation='+location+'&sort=date').text
        soup = bs4.BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
        for job in jobs:
            published_date = job.find('span', class_ = 'sim-posted').span.text 
            if 'few' in published_date:
               company_name = job.find('h3', class_ = 'joblist-comp-name').text.strip()
               skill = job.find('span', class_ = 'srp-skills').text.strip()
               more_info = job.header.h2.a['href']
               companies.append(company_name)
               dates.append(published_date)
               skills.append(skill)
               links.append(more_info)  
               data = zip(companies,dates,skills,links)
    
        if len(title)>0:
            context = {'data':data, 'title':title}
            
        else:
            context = {
                'message':'Oops!!! Sorry we could not find any job for your match..., pls try again, thank you'
                }
            
    return render(request, 'jobs.html', context)

