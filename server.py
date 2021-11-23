from datetime import datetime, timedelta
from flask import Flask, render_template
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
from database import News, db,app
from selenium import webdriver
from bs4 import BeautifulSoup
from transformers import pipeline
import jwt


db.engine.execute('drop table IF EXISTS news')

db.engine.execute('CREATE TABLE news (ID int, name_of_coin VARCHAR (255), news VARCHAR)')

db.session.commit()

app.config['SECRET_KEY'] = 'thisismyflasksecretkey'

@app.route('/webpage')
def webpage():

    auth = request.authorization

    if auth and auth.password == 'Farabi2003':
        return render_template('form.html')

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})


@app.route('/coin',  methods = ['POST', 'GET'])
def coin():
    if request.method == 'GET':
        return "GETTING DATA"

    if request.method == 'POST':
        
        summarizer = pipeline("summarization")
        

        names = request.form['name']
        url = 'https://coinmarketcap.com/currencies/'+ str(names) + "/news/"

        driver = webdriver.Chrome(executable_path=r'C:\Users\admin\Downloads\chromedriver_win32 (1)\chromedriver.exe')
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')

        filteredNews = []
        allNews = []
        allNews = soup.findAll('div', class_='sc-16r8icm-0 jKrmxw container')
        print("+++++++++++++++++++++++++++++")
        print(allNews)
        print("+++++++++++++++++++++++++++++")
        for i in range(len(allNews)):
            if allNews[i].find('p', class_='sc-1eb5slv-0 svowul-3 ddtKCV') is not None:
                print("----------------------------")
                print("filtredNews1 : ",filteredNews)
                print("----------------------------")
                filteredNews.append(allNews[i].text)
                print("----------------------------")
                print("filtredNews2 : ",filteredNews)
                print("----------------------------")
                ARTICLE = filteredNews
                filteredNews = summarizer(ARTICLE, max_length=80, min_length=50, do_sample=False)
                print("----------------------------")
                print("filtredNews3 : ",filteredNews)
                print("----------------------------")
                

        for i, news_item in enumerate(filteredNews):
            print(i, f"{news_item}\n")


        for filteredParagraphs in filteredNews:
            new_ex = News(1, names, str(filteredParagraphs['summary_text']))
            db.session.add(new_ex)
            db.session.commit()
           
            coins = db.engine.execute("select * from news where name_of_coin = '"+names+"'")
            return render_template("news.html", coins=coins)


if __name__ == '__main__':
    app.run(debug=True)
