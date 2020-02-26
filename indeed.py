import requests #라이브러리 설치해서 쉽게 url 내용 불러올 수 있게 만듬
from bs4 import BeautifulSoup #Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping. 

LIMIT = 50 
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page() : 
  result = requests.get(URL) #해당 Url의 내용을 긁어옴
  soup = BeautifulSoup(result.text,"html.parser") #beautifulsoup 라이브러리를 이용해서 screen scraping함  soup.땡땡땡을 쓰기 위한 준비 html에서 데이터를 추출한다.
  pagination = soup.find("div", {"class":"pagination"}) #indeed홈페이지에서 해당 페이지가 몇 페이지까지 있는지 불러온다.
  links = pagination.find_all('a') #pagination 에서 anchor a태그를 찾아온다.
  #여기서 links는 리스트이다. indeed_soup.find해서 찾아온 결과를 pagination변수에 넣어줬는데 거기서 리스트를 만들어서 links에 넣어준 것이다
  pages = [] #빈 리스트 만들기
  for link in links[:-1]:    #links의 마지막 요소 next는 읽지 않는다.
    pages.append(int(link.string))
    
    #만든 pages 리스트에 links에서 찾은 link 마다의 span을 넣어주기
    #append는 리스트에 구성물을 넣어주는 함수이다.
    #.string을 이용해서 가져올때 string만 가져옴.
    #link.string만 해도 된다. 왜냐하면 anchor 태그 밑에 string이 2,3, 이런식으로 숫자 하나밖에 없음.
    #pages.append(link.find("span").string)
    #pages = pages[0:-1] #pages리스트의 처음부터 마지막까지의 리스트 

  max_page = pages[-1] #pages숫자 중에서 가장 마지막 숫자 불러온다. 20을 가져와야 하기 때문에
  #print(range(max_page)) #range: 괄호안에 넣은 수만큼의 배열을 만들어줌.
  return max_page

#range()함수 연속된 숫자 정수를 만들어준다.
#range(0,10)


def extract_job(html):
  title = html.find("div",{"class":"title"}).find("a")["title"]
  company = html.find("span",{"class":"company"}) #span 태그 중 class 이름이 company인 것을 찾아낸다. 

  if company is None:
    company = "Unknow"
  else:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = str(company_anchor.string) #링크 있
    else:
      company = str(company.string) #링크 없
    company = company.strip() ##stirp()빈칸없애주기
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return{"title": title, "company": company, "location" : location,"link": f"https://www.indeed.com/viewjob?jk={job_id}"}




def extract_jobs(last_page):
  
  jobs = []
  for page in range(last_page):
    print(f"Scrapping indeed Page : {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)

      #title = result.find("div",{"class":"title"})
      #anchor = title.find("a")["title"]
  return jobs


def get_jobs():
  last_page = get_last_page() 
  #마지막 페이지를 extract_indeed_pages(get_last_page) 함수를 이용해서 last_page변수에 저장 
  jobs = extract_jobs(last_page)
  return jobs

