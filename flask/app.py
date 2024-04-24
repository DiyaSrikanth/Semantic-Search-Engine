from flask import Flask, request, render_template
from embed import embed
import pandas as pd
from flask.helpers import url_for

app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'hello world'

@app.route('/', methods=['GET', 'POST'])
def home():
    input_text = request.form.get('input_sentence')
    if (input_text!= None) and (input_text!=''):
        subtitle_files=[]
        your_sub = embed(input_text)
        subtitle = your_sub['content_name'].values
        for x in subtitle:
            #x=x.replace('.srt', '')
            download_url = url_for('static', filename=x)
                # Create download link with correct URL
            srt = f'<a href="{download_url}" download>{x}</a>'
            subtitle_files.append(srt)
        your_sub['Download links']= subtitle_files
        your_sub = your_sub.drop(columns= ['ids', 'content_name'])
        your_sub.rename(columns={'name':'Subtitle name'}, inplace=True)
        your_sub.index+=1
        return render_template('home.html', tables =[your_sub.to_html(index=True, classes='data', escape=False)], titles = your_sub.columns.values)
    else:
        return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)