import sys
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template

if len(sys.argv) != 3:
    sys.exit(1)

def html_file(content):
    html_file = open('output.html',"w")
    html_file.write(content)
    html_file.close()

data=pd.read_csv('data.csv')
data.columns = data.columns.str.strip()

template1=Template("""
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
      </head>
      <body>
        <h1>{{ title }}</h1>
        <table border="1" style="border-collapse: collapse;">
          <tr>
            {% for x in column_headers %}      
            <th>{{ x }}</th>
            {% endfor %}
          </tr>
          
          {% for row in list %}
          <tr>
            {% for cell in row %}
            <td>{{ cell }}</td>
            {% endfor %}
          </tr>
          {% endfor %}             
          <tr>
            <td colspan="2">Total</td>
            <td>{{ total }}</td>
          </tr>
        </table>
      </body>
    </html>
    """)


template2=Template("""
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>{{title}}</title>
  </head>
  <body>
    <h1>{{title}}</h1>
    <table border="1" style="border-collapse: collapse;">
      <tr>
        {% for x in column_headers %}      
        <th>{{ x }}</th>
        {% endfor %}
      </tr>
      <tr>
        <td>{{average_marks}}</td>
        <td>{{max_marks}}</td>
      </tr>
    </table>
    <img src="{{histogram}}" alt="histogram">
  </body>
</html>""")

template3=Template("""
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>ERROR</title>
  </head>
  <body>
    <h1>Wrong Inputs</h1>
    Something went wrong
  </body>
</html>
""")
flag=sys.argv[1]
s_c_id=sys.argv[2]

if flag=="-s":
    student_data=data[data['Student id']==int(s_c_id)]

    if student_data.empty:
        content=template3.render()
        html_file(content)

    else:
        student_total_marks = student_data['Marks'].sum()
        content=template1.render(title="Student Details",column_headers=["Student id","Course id","Marks"],list=student_data.values.tolist(),total=student_total_marks)
        html_file(content)

elif flag=="-c":
    course_data=data[data['Course id']==int(s_c_id)]
    if course_data.empty:
        content=template3.render()
        html_file(content)
    else:
        average_marks = course_data['Marks'].mean()
        max_marks = course_data['Marks'].max()
        plt.hist(course_data['Marks'], bins=10, edgecolor='black')
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.title(f'Histogram of Marks for Course ID {s_c_id}')
        plt.savefig('histogram.png')
        content=template2.render(title="Course Details",column_headers=["Average Marks","Maximum Marks"],average_marks=average_marks,max_marks=max_marks,histogram='histogram.png')
        html_file(content)

else:
    content=template3.render()
    html_file(content)