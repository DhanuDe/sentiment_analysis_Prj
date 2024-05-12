from flask import Flask,render_template,request,redirect

from helper import preprocessing,vectorizer,get_pred

app = Flask(__name__)

data  =dict()


reviews = ['good Product','bad product', 'I like it']

positive =2
negative =2

@app.route("/")
def index():
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative

    return render_template('index.html',data =data)


@app.route("/",methods =['post'])
def my_post():
    text = request.form['text']
    processed_text = preprocessing(text)
    vec_text = vectorizer(processed_text)
    prediction = get_pred(vec_text)

    if prediction == 'negative':
        global negative
        negative +=1

    else:
        global positive
        positive +=1

    reviews.insert(0,text)
    return redirect(request.url)




if __name__ == '__main__':
    app.run()
    