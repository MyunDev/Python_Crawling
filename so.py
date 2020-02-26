import requests #라이브러리 설치해서 쉽게 url 내용 불러올 수 있게 만듬
from bs4 import BeautifulSoup #Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping. 

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"


def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div",{"class" : "s-pagination"}).find_all("a")
  #pages = pages[0:-1] : 가져온 페이지에서 마지막 NEXT 절삭
  #print(pages[-1]) :절삭한 후 마지막 숫자 불러옴

  last_page = pages[-2].get_text(strip=True) 
  #스트립을 작성하면 추출해서 가져올때 whitespace 공간이 생기는 것을 방지함 
  return int(last_page) #range 함수를 쓰려면 string을 int형으로 바꿔줘야함

def extract_job(html):
    title = html.find("h2",{"class" : "mb4"}).find("a")["title"]
  
    

  
    company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span", recursive = False)
    company = company.get_text(strip = True)
    location = location.get_text(strip = True).strip("•")
    #company = company.get_text(strip = True).strip("\n")
    #location = location.get_text(strip = True ).strip("-").strip(" \r").stirp("\n")
    job_id = html['data-jobid']
    return {"title" : title, "company": company, "location": location, "apply_link" : f"https://stackoverflow.com/jobs/{job_id}"}
   
   
  
  
  
  
  #title = html.find("h2",{"class" : "mb4"}).find("a")["title"]
  #return {"title" : title}
  
  
  #company, location= html.find("h3",{"class":"mb4"}).find_all("span",recursive=False)
  #company = company.get_text(strip=True).strip("-")
  #location = location.get_text(strip=True)
  #job_id = html["data-jobid"]


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):

    #print(page + 1) 0~175말고 0~176(마지막페이지) 가 나오게 하기 위해서
    print(f"Scrapping SO : page : {page}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class" : "-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job) #append 함수 리스트에 요소 추가 
  return jobs





def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs