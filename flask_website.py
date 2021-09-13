#from create_plot_file import create_plot
#from create_name_file import create_name
from flask import Flask
from flask import render_template, url_for, request, redirect
import requests
import json
import plotly.express as px
import plotly
import pandas as pd

#-------------------------------------------------------------------------------
#Initialize app

app=Flask(__name__,template_folder='https://goals.github.io')

#-------------------------------------------------------------------------------
#Home page

#global compname
#compname='tesla'

@app.route('/')
def search():
    return render_template("index.html")

#-------------------------------------------------------------------------------
#Graph page

@app.route('/goals', methods =["GET", "POST"])
def goals_page():

    if request.method == "POST":
        cname = request.form.get('cname')

        try:
            cname=cname.lower()
            json_obj=requests.get(f'https://tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization/goals?q=nasdaq:{cname}&token=63e8a1a2f70c2b11fedb599ffce8831b')
            json_data=json_obj.json()
            company_name=json_data[0]['company_name']
            cname=cname.upper()

            sdg=[]
            score=[]
            goal_len=len(json_data[0]['goals'])

            for i in range(goal_len):
                sdg=sdg +[json_data[0]['goals'][i]['sdg']]
                score=score + [json_data[0]['goals'][i]['score']]

            df=pd.DataFrame({"sdg":sdg,"score":score})

            fig = px.bar(df, x="sdg", y="score", barmode="group",
            labels={
                     "sdg": "Sustainable Development Goals",
                     "score": "Goal Scores"
                 })

            graphJSON= json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        except KeyError:
            cname=cname
            company_name='Could not find company'
            graphJSON=''
        #name=create_name()
        #graph=create_plot()
        return render_template('goals.html', name=company_name, plot=graphJSON, cname=cname)

#-------------------------------------------------------------------------------
#Run app

app.run(port=8000)
