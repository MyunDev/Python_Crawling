import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode = "w") #파일을 열어서 file 변수에 저장 
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return
  