import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/<username>')
def get_attendance_meet_url(username):

    if '-' in username:
        user,passwd=username.split('-')
    else:
        user=username
        passwd=username
    url = 'https://tkmce.etlab.in/user/login'
    payload = {'LoginForm[username]': user, 'LoginForm[password]': passwd}

    sess = requests.session()
    post = sess.post(url=url, data=payload)
    attendance_url = 'https://tkmce.etlab.in/ktuacademics/student/viewattendancesubject/22'
    grid_url='https://tkmce.etlab.in/ktuacademics/student/attendance'
    data = BeautifulSoup(sess.get(attendance_url).content, 'html.parser')
    grid_data=BeautifulSoup(sess.get(grid_url).content, 'html.parser')
    user_name = (data.find('span',{'class':'text'}).getText().strip())
        
    atten_table = data.find_all('table', {'class': 'items table table-striped table-bordered'})
    attendance={}

    for tag in atten_table:
        num=tag.find_all('th',{'class':'span2'})
        for i in range(len(num)-2):
            sub_code = tag.find_all('th', {'style': 'text-align:center'})[i].getText().strip()
            sub_name = grid_data.find(text=re.compile(sub_code+'\s\-\s.+'))
            if sub_name != None:
                sub_name=sub_name.replace('									','')
            else:
                sub_name=sub_code
            perc = tag.find_all('td', {'class': 'span2'})[i].getText().strip()
            attendance[sub_name]=perc



    link_dict={}
    subjects=[]
    url='https://tkmce.etlab.in/ktuacademics/student/onlinevideolink'
    data = BeautifulSoup(sess.get(url).content, 'html.parser')
    link_table = data.find_all('table', {'class': 'section table table-bordered table-striped'})
    for tag in link_table:
        link_name=tag.find_all('td',{'class':'span5'})
        links=tag.find_all('a')
        for name in link_name:
            sub_name=name.getText().replace('						','')
            sub_name=sub_name.replace('\n\t','')
            if sub_name!='\nVideo Link\n':
                subjects.append(sub_name)
        for link in links:
            gmeet=link['href']
            link_dict[subjects[0]]=gmeet  
            subjects.remove(subjects[0])

    print(link_dict)
    return(jsonify({'status':'OK','Name':user_name,'attendance':attendance,'meet_urls':link_dict}))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status': 'Not found', 'error': 'Cannot find requested endpoint'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
