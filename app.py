from flask import Flask,render_template,request,flash,redirect,url_for
import joblib
import numpy as np
from datetime import datetime

app=Flask(__name__)

app.config['SECRET_KEY']="669c717bc7904470b2f188baf8b464a5"

# Load the  regression model in the app
regression_model=joblib.load('regression_model.gz')

# Load the standardisation model in the app
std_model=joblib.load('standerd_model.gz')

@app.route("/",methods=['get','post'])
def home():
    if request.method=='POST':

        # formate of date
        date_format='%Y-%m-%dT%H:%M'

        # getting the information from the form
        airline=request.form['Airline']
        source=request.form['Source']
        destination=request.form['Destination']
        departure_time=request.form['Departure_time']
        arrival_time=request.form['Arrival_time']
        stops=request.form['Stops']

        # checking if arrival_time filed is filled or not
        if not arrival_time:
            flash("Please Enter Arrival Time.")
            return redirect(url_for('home'))

        # checking if departure_time field is filled or not
        if not departure_time:
            flash("Please Enter Departure Time.")
            return redirect(url_for('home'))

        # checking souce and destination
        if source==destination:
            flash("Source and destination can not be same.")
            return redirect(url_for('home'))

        #converting string object to datetime object
        departure_time=datetime.strptime(departure_time,date_format)
        arrival_time=datetime.strptime(arrival_time,date_format)
        
        # arrival_time can not be less than departure time 
        if arrival_time<departure_time:
            flash("You can not Arrive before Departing.Please check arrival and departure time.")
            return redirect(url_for('home'))
        
        # Airline
        Air_India=0
        GoAir=0
        IndiGo=0
        Jet_Airways=0
        Jet_Airways_Business=0
        Multiple_carriers=0
        Multiple_carriers_Premium_economy=0
        SpiceJet=0
        Vistara=0
        Vistara_Premium_economy=0
        # Source
        s_Chennai=0
        s_Delhi=0
        s_Kolkata=0
        s_Mumbai=0
        # Destination
        d_Cochin=0
        d_Delhi=0
        d_Hyderabad=0
        d_Kolkata=0
        d_New_Delhi=0
        # Departure
        journey_day=departure_time.day
        journey_mon=departure_time.month
        dep_hour=departure_time.hour
        dep_minu=departure_time.minute
        # Arrival
        ari_hour=arrival_time.hour
        ari_minu=arrival_time.minute
        # Duration
        date=arrival_time-departure_time
        duration_hour=(date.days*24)+int(date.seconds/60)/60
        duration_minu=int(date.seconds/60)%60

        # airline check
        if airline=="Air India":
            Air_India=1
        elif airline=="GoAir":
            GoAir=1
        elif airline=="IndiGo":
            IndiGo=1
        elif airline=="Jet Airways":
            Jet_Airways=1
        elif airline=="Jet Airways Business":
            Jet_Airways_Business=1
        elif airline=="Multiple carriers":
            Multiple_carriers=1
        elif airline=="Multiple carriers Premium economy":
            Multiple_carriers_Premium_economy=1
        elif airline=="SpiceJet":
            SpiceJet=1
        elif airline=="Vistara":
            Vistara=1
        elif airline=="Vistara Premium economy":
            Vistara_Premium_economy=1

        # Source check
        if source=="Delhi":
            s_Delhi=1
        elif source=="Kolkata":
            s_Kolkata=1
        elif source=="Mumbai":
            s_Mumbai=1
        elif source=="Chennai":
            s_Chennai=1
        
        # destination check
        if destination=="Cochin":
            d_Cochin=1
        elif destination=="Delhi":
            d_Delhi=1
        elif destination=="New Delhi":
            d_New_Delhi=1
        elif destination=="Hyderabad":
            d_Hyderabad=1
        elif destination=="Kolkata":
            d_Kolkata=1

        arr=np.array([stops,journey_day,journey_mon,dep_hour,dep_minu,ari_hour,ari_minu,duration_hour,duration_minu,
                        Air_India,GoAir,IndiGo,Jet_Airways,Jet_Airways_Business,Multiple_carriers,
                        Multiple_carriers_Premium_economy,SpiceJet,Vistara,Vistara_Premium_economy,d_Cochin,
                        d_Delhi,d_Hyderabad,d_Kolkata,d_New_Delhi,s_Chennai,s_Delhi,s_Kolkata,s_Mumbai])

        arr=np.reshape(arr,(1,arr.size))

        arr=std_model.transform(arr)

        prediction=int(regression_model.predict(arr)[0])

        return redirect(url_for('prediction',value=prediction))

    return render_template("home.html")

@app.route("/prediction/<value>",methods=['get'])
def prediction(value):
    return render_template("prediction.html",value=value)

if __name__=='__main__':
    app.run(debug=True)