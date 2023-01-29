from flask import Flask,render_template,redirect

app=Flask(__name__)

app.config['SECRET_KEY']="vksnvjvjkfjvn27846t292v247f"

@app.route("/",methods=['get','post'])
def predict():
    return render_template("home.html")


if __name__=='__main__':
    app.run(debug=True)