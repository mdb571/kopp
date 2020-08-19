import requests
from bs4 import BeautifulSoup


url = 'https://tkmce.etlab.in/user/login'
payload = {'LoginForm[username]': '180051', 'LoginForm[password]': '180051'}

sess = requests.session()
post = sess.post(url=url, data=payload)


def get_attendance():
    attendance_url = 'https://tkmce.etlab.in/ktuacademics/student/viewattendancesubject/22'

    _data = BeautifulSoup(sess.get(attendance_url).content, 'html.parser')
    _user_name = (_data.find('span',{'class':'text'}).getText().strip())
        
    atten_table = _data.find_all('table', {'class': 'items table table-striped table-bordered'})

    message = []

    for tag in atten_table:
        num=tag.find_all('th',{'class':'span2'})
        for i in range(len(num)-2):
            _sub = tag.find_all('th', {'style': 'text-align:center'})[i].getText().strip()
            _perc = tag.find_all('td', {'class': 'span2'})[i].getText().strip()
            _message = '{}, your attedance for {} is {}'.format(_user_name,_sub, _perc)
            message.append("\n"+_message)
            print(_message)     


get_attendance()