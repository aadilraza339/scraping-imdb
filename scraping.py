import requests,json
from pprint import pprint
import os.path
from bs4 import BeautifulSoup
import random,time
def scrape_top_list():
	if os.path.isfile("scraping.text"):
		with open("scraping.text","r") as count:
			main_data=json.load(count)
		return(main_data)
	master_list = []
	url = "https://www.imdb.com/india/top-rated-indian-movies/"
	sample = requests.get(url)
	soup = BeautifulSoup(sample.text,'html.parser')
	need = soup.find("div",class_="lister")
	tbody = need.find("tbody",class_="lister-list")
	trs = tbody.findAll("tr")
	rang = 0
	mainList = []
	for tr in trs:
		master_list = {}
		rang = rang+1
		name = tr.find("td",class_="titleColumn").a
		master_list["name"] = name.get_text()
		master_list["postiton"] =rang
		year = tr.find("span",class_="secondaryInfo")
		new_year=year["year"]=year.get_text()
		cut = int(new_year[1:5]) 
		master_list["year"] = cut
		rating = tr.find("td",class_="ratingColumn imdbRating")
		movie_rating =rating.get_text()
		rating_cut=float(movie_rating[3:5])
		master_list["rating"]=rating_cut
		master_list["url"]="https://www.imdb.com"+name["href"][:17]
		mainList.append(master_list)
		with open("scraping.text","w") as copy:
			data=json.dump(mainList,copy,indent=4)
	# pprint.pprint(mainList)
top_movies_list=(scrape_top_list())

# print(scrape_top_list())
# ..........2
def group_by_year(movies):
	years={}
	for i in movies:
		year=i["year"]
		years[year]=[]	
	for j in years:
		for key in movies:
			movies_year=key["year"]
			if j==movies_year:
				years[j].append(key)

	return(years)
# dec_arg=group_by_year(top_movies_list)
pprint(group_by_year(top_movies_list))

# ................3
def group_by_decade(movies):
	movies_by_decade1={}
	list2=[]
	for index in movies:
		mod=index%10
		decade=index-mod
		if decade not in list2:
			list2.append(decade)
	list2.sort()
	for i in list2:
		movies_by_decade1[i]=[]
	for i in movies_by_decade1:
		dec10=i+9
		for x in movies:
			if x<=dec10 and x>=i:
				for v in movies[x]:
					movies_by_decade1[i].append(v)
	return(movies_by_decade1)

group_by_decade(dec_arg) 

# ...................12
def scrape_movie_cast(movies_cast_url):
	movies_=requests.get(movies_cast_url)
	cast_soup=BeautifulSoup(movies_.text,'html.parser')
	cast_list=cast_soup.find_all("div",class_="see-more")
	for i in cast_list:
		if "See full cast »"==(i.text.strip()):
			cast=(i.find("a").get("href"))
	cast_requests=movies_cast_url+cast
	page=requests.get(cast_requests)
	soup_page=BeautifulSoup(page.text,"html.parser")
	cast_table=soup_page.find("table",class_="cast_list")
	cast_tr=cast_table.find_all("tr")
	cast_id=[]
	for td in cast_tr:
		# print(td.text.strip())
		all_td=td.find_all("td",class_="")
		for j in all_td:
			href=(j.find("a").get("href")[6:15])
			name_=(j.text.strip())
			cast_name={'id':href,
						'name':name_}
			cast_id.append(cast_name)
	return(cast_id)

# (scrape_movie_cast(top_movies_list[0]["url"]))

# ............4
def scrape_movie_details(movie_url):
	movie_url_ids=(movie_url[27:36])
	randint=random.randint(1,3)
	if os.path.isfile('scrapingdata/'+movie_url_ids+".json"):
		with open('scrapingdata/'+movie_url_ids+".json","r") as copy1:
			tom=json.load(copy1)
			return(tom)
	else:
		movies_details={}
		language=[]
		Director=[]
		qaq=[]
		ham=[]
		time1=time.sleep(randint)
		data=requests.get(movie_url)
		soup=BeautifulSoup(data.text,"html.parser")
		div=soup.find('div',class_="title_wrapper")
		name=div.find("h1").get_text()
		to=name.split()
		to.pop()
		name=(" ".join(to))
		movies_details["name"]=name
		d=soup.find("div",class_="credit_summary_item")
		Dir=d.find_all("a")
		for i in Dir:
			Director.append(i.text)
		# print(Director)
		movies_details["Director"]=Director
		div_hindi=soup.find('div',attrs={'class':'article','id':'titleDetails'})
		sushant=div_hindi.find_all("div",class_="txt-block")
		bio=[]
		for i in sushant:
			h4=i.find('h4')
			if h4:
				if h4.text=="Language:":
					lan=(i.find_all('a'))
					for j in lan:
						language.append(j.text)
					movies_details["language"]=language
				if h4.text=="Country:":
					coun=(i.find("a"))
					pop4=(coun.text)
					movies_details["Country"]=pop4
		pos=soup.find("div",class_="poster").img["src"]
		movies_details["poster_image_url"]=[pos]
		dada=soup.find("div",class_="summary_text").get_text()
		bio=dada.strip()
		movies_details["bio"]=bio
		go=soup.find("div",class_="subtext")
		waw=go.find("time").get_text()
		ti=waw.strip().split()
		mint=0
		for i in ti:
			if 'h' in i:
				time_=int(i.strip("h"))*60
			
			elif "min" in i:
				mint+=int(i.strip("min"))
			runing=(time_+mint)
			movies_details["runing_time"]=runing
		gam=go.find_all("a")
		for i in gam:
			ham.append(i.text)
		ham.pop()
		movies_details["genre"]=ham
		movies_details['cast']=scrape_movie_cast(movie_url)
		with open('scrapingdata/'+movie_url_ids+".json","w") as copy:
			json.dump(movies_details,copy)
	
		return(movies_details)	
# scrape_movie_details(url_10_all)
# ..........5

def get_movie_list_details(movies_list):
	a=0
	movies_url_list=[]
	while a<250:
		ope=scrape_movie_details(movies_list[a]["url"])
		a=a+1
		movies_url_list.append(ope)
	# pprint(movies_url_list)
	return(movies_url_list)
you=get_movie_list_details(top_movies_list)
# pprint(movies_detail_list)
# ...........6
# def analyse_movies_language(movies_list):
# 	check_list1={}
# 	count=[]
# 	for i in movies_list:
# 		for j in i["language"]:
# 			count.append(j)
# 	for x in count:
# 		if x not in check_list1:
# 			check_list1[x]=1
# 		else:
# 			check_list1[x]+=1
# 	return(check_list1)


# analyse_movies_language(movies_detail_list)

# ..........7
# def analyse_movies_directors(movies_directors):
# 	Director_list=[]
# 	movies_directors_list={}
# 	for i in movies_directors:
# 		for j in i["Director"]:
# 			# print(j)
# 			Director_list.append(j)
# 	for c in Director_list:
# 		if c not in movies_directors_list:
# 			movies_directors_list[c]=1
# 		else:
# 			movies_directors_list[c]+=1
# 	return(movies_directors_list)
# analyse_movies_directors(movies_detail_list)


# ..........................10
# def analyse_language_and_directors(coun):
# 	Director_list={}
# 	for d in coun:
# 		for Dir in d["Director"]:
# 			Director_list[Dir]={}
# 	# print(Director_list)
# 	for i in range(len(coun)):
# 		for j in Director_list:
# 			if j in coun[i]["Director"]:
# 				for Language in coun[i]["language"]:
# 					Director_list[j][Language]=0

# 	for i in range(len(coun)):
# 		for j in Director_list:
# 			if j in coun[i]["Director"]:
# 				for Language in coun[i]["language"]:
# 					Director_list[j][Language]+=1
	# pprint(Director_list)

	

# analyse_language_and_directors(movies_detail_list)

# ............................11
# def analyse_movies_genre(movies_list):
# 	genre_list=[]
# 	genre_dic={}
# 	for i in movies_list:
# 		for genre  in i["genre"]:
# 			genre_list.append(genre)
# 	for k in genre_list:
# 		if k not in genre_dic:
# 			genre_dic[k]=1
# 		else:
# 			genre_dic[k]+=1
# 	return(genre_dic) 
			
# analyse_movies_genre(movies_detail_list)

# .......................14


def co_actors(co_casts):
	pprint(co_casts)
	empty={}
	for i in co_casts:
		c=i["cast"]
		for j in c:
			ct=(j["id"])
			empty[ct]={}
			empty[ct]["name"]=j["name"]
			empty[ct]["frequent_co_actors"]=[]
			break
		empty1=empty[ct]["frequent_co_actors"]
		count=-1
		for j in c:
			empty2={}
			count+=1
			empty_list=[]
			empty_list.append(ct)
			num=0
			if count>0:
				empty_list.append(j["id"])
				for k in co_casts:
					p=k["cast"]
					for g in p:
						if g["id"]==empty_list[0]:
							for h in p:
								if h["id"]==empty_list[1]:
									num+=1
									empty2["num_movies"]=num
				empty2["name"]=j["name"]
				empty2["id"]=j["id"]
				empty1.append(empty2)
				if count==5:
					break
	return (empty)
# pprint(co_actors(you))