import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require a GUI
import matplotlib.pyplot as plt

from flask import Flask,request,render_template
app=Flask(__name__)
@app.route("/",methods=["GET","POST"])

def index():
    data=pd.read_csv("data.csv")
    data.columns = data.columns.str.strip()
    if request.method=="POST":
        try:
            result=request.form
            if(result['ID']=="" or result['id_value']==""):
                return render_template('wrong_input.html')
            elif result["ID"]=="student_id":
                student_id=data[data['Student id']==int(result['id_value'])]
                if student_id.empty:
                    return render_template('wrong_input.html')
                total_marks=student_id['Marks'].sum()
                return render_template('student_details.html',list=student_id.values.tolist(),total=total_marks)
            else:
                course_id=data[data['Course id']==int(result['id_value'])]
                print(course_id)
                if course_id.empty:
                    return render_template('wrong_input.html')
                avg_marks=course_id['Marks'].mean()
                max_marks=course_id['Marks'].max()
                plt.hist(course_id['Marks'], bins=10, edgecolor='black')
                plt.xlabel('Marks')
                plt.ylabel('Frequency')
                plt.title(f'Histogram of Marks for Course ID {result["id_value"]}')
                plt.savefig("static/histogram.png")
                plt.close()
                return render_template("course_details.html",average_marks=avg_marks,max_marks=max_marks)
        except:
            return render_template('wrong_input.html')
    else:
       return  render_template("index.html")
        
if __name__=='__main__':
    app.debug=True
    app.run()
    