
from os import name
from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from .models import CovidDb, alco
from .models import diabDb
import boto3
from html2image import Html2Image
from bs4 import BeautifulSoup as bs
import re
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def diabetesdb(request):
    tasks_obj2 = diabDb.objects.all()
    return render(request, 'diabetesdb.html',{"alltasks": tasks_obj2,"alltasks2":tasks_obj2} )

def coviddb(request):
    
    tasks_obj = CovidDb.objects.all()
    
    return render(request, 'coviddb.html',{"alltasks": tasks_obj,"alltasks2":tasks_obj} )

def alcoholdb(request):
    
    tasks_obj = alco.objects.all()
    
    return render(request, 'alcoholdb.html',{"alltasks": tasks_obj,"alltasks2":tasks_obj} )

    
def diabetes(request):
    """ 
    Reading the training data set. 
    """
    new_png1=""
    dfx = pd.read_csv('data/Diabetes_XTrain.csv')
    dfy = pd.read_csv('data/Diabetes_YTrain.csv')
    X = dfx.values
    Y = dfy.values
    Y = Y.reshape((-1,))

    """ 
    Reading data from user. 
    """
    value = ''

    if request.method == 'POST':

        name = request.POST['name']
        glucose = float(request.POST['glucose'])
        bloodpressure = float(request.POST['bloodpressure'])
        skinthickness = float(request.POST['skinthickness'])
        bmi = float(request.POST['bmi'])
        insulin = float(request.POST['insulin'])
        pedigree = float(request.POST['pedigree'])
        age = float(request.POST['age'])

        user_data = np.array(
            (
             glucose,
             bloodpressure,
             skinthickness,
             bmi,
             insulin,
             pedigree,
             age)
        ).reshape(1, 7)

        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X, Y)

        predictions = knn.predict(user_data)
        new_png1=""
        if int(predictions[0]) == 1:
           # value = 'Your Diabeties Data Checked and it is Positive.'
            value = 'Data is been Checked it is Positive Must take care and must consorn a doctor immediatly'
            c_obj1= diabDb(name=name,glucose=glucose,bloodpressure=bloodpressure,skinthickness=skinthickness,bmi=bmi,insulin=insulin,pedigree=pedigree,age=age,result1=value)
            c_obj1.save()
            new_png1=SendReport1(name, glucose, bloodpressure, bmi, value)
            new_png1 = "https://cadproject.s3.amazonaws.com/"+new_png1
        elif int(predictions[0]) == 0:
            #value = "Your Diabeties Data Checked and it is Negative"
            value = "Data is been Checked it is Negative.Your health Is monitered to be good"
            c_obj1= diabDb(name=name,glucose=glucose,bloodpressure=bloodpressure,skinthickness=skinthickness,bmi=bmi,insulin=insulin,pedigree=pedigree,age=age,result1=value)
            c_obj1.save() 
            new_png1=SendReport1(name, glucose, bloodpressure, bmi, value)
            new_png1= "https://cadproject.s3.amazonaws.com/"+new_png1

    return render(request,
                  'diabetes.html', context ={'value':value,"new_png1":new_png1}                   
                  )

#COVID MODULE
def covid(request):
    new_png=""
    df = pd.read_csv('data/qt_dataset.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1:]

    value = ''

    if request.method == 'POST':
        Name = request.POST['fullname']
        Oxy = float(request.POST['Oxy'])
        Pulse = float(request.POST['Pulse'])
        Temp = float(request.POST['Temp'])
        
        

        user_data = np.array(
            (Oxy,
             Pulse,
             Temp,
            )
        ).reshape(1, 3)

        rf = RandomForestClassifier(
            n_estimators=16,
            criterion='entropy',
            max_depth=9
        )

        rf.fit(np.nan_to_num(X), Y)
        rf.score(np.nan_to_num(X), Y)
        predictions = rf.predict(user_data)
        new_png=""
        if int(predictions[0]) == 1:
            
            value = 'Data is been Checked it is Positive. Must take care and must concern a doctor immediatly.'
            c_obj= CovidDb(Name=Name,Oxy=Oxy,Pulse=Pulse,Temp=Temp,result=value)
            c_obj.save()
            new_png=SendReport(Name, Oxy, Pulse, Temp, value)
            new_png = "https://cadproject.s3.amazonaws.com/"+new_png
        elif int(predictions[0]) == 0:
            
            value = "Data is been Checked it is Negative.Your health Is monitered to be good."
            c_obj= CovidDb(Name=Name,Oxy=Oxy,Pulse=Pulse,Temp=Temp,result=value)
            c_obj.save() 
            new_png=SendReport(Name, Oxy, Pulse, Temp, value)
            new_png = "https://cadproject.s3.amazonaws.com/"+new_png
    return render(request,
                  'covid.html', context ={'value':value,"new_png":new_png}                   
                  )


def SendReport(fullname,Oxy,Pulse,Temp,result1):
    # Send message to SQS queue
    s3_client = boto3.client('s3')
    html = open("report/invoice.html")

    # Parse HTML file in Beautiful Soup
    soup = bs(html, 'html.parser')

    # Give location where text is
    # stored which you wish to alter
    old_text0 = soup.find("h2", {"id": "fullname"})
    old_text1 = soup.find("td", {"id": "Oxy"})
    old_text2 = soup.find("td", {"id": "Pulse"})
    old_text3 = soup.find("td", {"id": "Temp"})
    old_text4 = soup.find("h1", {"id": "result"})
    # Replace the already stored text with
    # the new text which you wish to assign
    new_text0 = old_text0.find(text=re.compile(
        'Kevin')).replace_with(fullname)
    new_text1 = old_text1.find(text=re.compile(
        'Oxy')).replace_with(str(Oxy))
    new_text2 = old_text2.find(text=re.compile(
        'Pulse')).replace_with(str(Pulse))
    new_text3 = old_text3.find(text=re.compile(
        'Temp')).replace_with(str(Temp))
    new_text4 = old_text4.find(text=re.compile(
        'Pass')).replace_with(result1)


    fullname = fullname.replace(" ","_")	
    new_file_name="report/"+str(fullname)+".html"
    # Alter HTML file to see the changes done
    with open(new_file_name, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


    response = s3_client.upload_file(new_file_name, "cadproject", new_file_name)
    return new_file_name
    print("\n\nfile uploaded")
    


def SendReport1(name, glucose, bloodpressure, bmi,result1):
    # Send message to SQS queue
    s3_client = boto3.client('s3')
    html = open("report/diabetes/invoiced.html")

    # Parse HTML file in Beautiful Soup
    soup = bs(html, 'html.parser')

    # Give location where text is
    # stored which you wish to alter
    old_text0 = soup.find("h2", {"id": "name"})
    old_text1 = soup.find("td", {"id": "glucose"})
    old_text2 = soup.find("td", {"id": "bloodpressure"})
    old_text3 = soup.find("td", {"id": "bmi"})
    old_text4 = soup.find("h1", {"id": "result1"})
    # Replace the already stored text with
    # the new text which you wish to assign
    new_text0 = old_text0.find(text=re.compile(
        'Kevin')).replace_with(name)
    new_text1 = old_text1.find(text=re.compile(
        'glucose')).replace_with(str(glucose))
    new_text2 = old_text2.find(text=re.compile(
        'bloodpressure')).replace_with(str(bloodpressure))
    new_text2 = old_text3.find(text=re.compile(
        'bmi')).replace_with(str(bmi))
    new_text3 = old_text4.find(text=re.compile(
        'Pass')).replace_with(result1)
  

    name = name.replace(" ","_")	
    new_file_name1="report/diabetes/"+str(name)+".html"
    # Alter HTML file to see the changes done
    with open(new_file_name1, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


    response = s3_client.upload_file(new_file_name1, "cadproject", new_file_name1)
    return new_file_name1
    print("\n\nfile uploaded") 
    #https://ccep4destination.s3.ap-south-1.amazonaws.com/drag.html

def alcohol(request):
    value=""
    new_png2=""
    if request.method == 'POST':
        Name1 = request.POST['Name1']
        print(Name1)
        Age = request.POST['Age']
        bac_val = float(request.POST['bac_val'])
        
        new_png2=""
        if(bac_val>=0.08):
            value = "Sorry!! You are too drunk to work or drive!"
            c_obj2= alco(Name1=Name1,Age=Age,bac_val=bac_val,result2=value)
            c_obj2.save()
            new_png2 = SendReport2(Name1, Age, bac_val, value)
            new_png2 = "https://cadproject.s3.amazonaws.com/"+new_png2
            
        else:
            value ="Congrats!! You're perfectly fine to work ro drive"
            c_obj2= alco(Name1=Name1,Age=Age,bac_val=bac_val,result2=value)
            c_obj2.save() 
            new_png2 = SendReport2(Name1, Age, bac_val, value)
            new_png2 = "https://cadproject.s3.amazonaws.com/"+new_png2
           
            
    return render(request,
                      'alcohol.html', context ={'value':value,"new_png2":new_png2}                   
                  )

def SendReport2(Name1, Age, bac_val,result2):
    # Send message to SQS queue
    s3_client = boto3.client('s3')
    html = open("report/diabetes/invoiced2.html")

    # Parse HTML file in Beautiful Soup
    soup = bs(html, 'html.parser')

    # Give location where text is
    # stored which you wish to alter
    old_text0 = soup.find("h2", {"id": "Name1"})
    old_text1 = soup.find("td", {"id": "Age"})
    old_text2 = soup.find("td", {"id": "bac_val"})
    old_text3 = soup.find("h1", {"id": "result2"})
    
    # Replace the already stored text with
    # the new text which you wish to assign
    new_text0 = old_text0.find(text=re.compile(
        'Kevin')).replace_with(Name1)
    new_text1 = old_text1.find(text=re.compile(
        'Age')).replace_with(str(Age))
    new_text2 = old_text2.find(text=re.compile(
        'bac_val')).replace_with(str(bac_val))
    new_text3 = old_text3.find(text=re.compile(
        'Pass')).replace_with(result2)
  

    name = Name1.replace(" ","_")	
    new_file_name2="report/diabetes/"+str(Name1)+".html"
    # Alter HTML file to see the changes done
    with open(new_file_name2, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


    response = s3_client.upload_file(new_file_name2, "cadproject", new_file_name2)
    return new_file_name2
    print("\n\nfile uploaded")
    #https://ccep4destination.s3.ap-south-1.amazonaws.com/drag.html