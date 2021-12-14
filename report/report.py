import boto3
from html2image import Html2Image
from bs4 import BeautifulSoup as bs
import re

def SendReport(fullname,Oxy,Pulse,Temp,result):
    # Send message to SQS queue
    s3_client = boto3.client('s3')
    html = open("invoice.html")

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
        'Pass')).replace_with(result)
        



    fullname = fullname.replace(" ","_")	
    new_file_name=str(fullname)+".html"
    # Alter HTML file to see the changes done
    with open(new_file_name, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


    hti = Html2Image()
    new_png=fullname+".png"
    hti.screenshot(
        html_file=new_file_name,
        save_as=new_png,
        size=(750, 563)
    )            
    #response = s3_client.upload_file(new_png, "s3-prac5-bucket", new_png)
    print("\n\nfile uploaded")

SendReport("kevin",12,90,21,"Nagative")