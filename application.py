from flask import Flask,jsonify,render_template,request
import pickle
import numpy as np
import pandas as pd

## Import ridge regressor and standard scaler pickle
xgb_model=pickle.load(open('models/xgb.pkl','rb'))
standard_scaler=pickle.load(open('models/scaler.pkl','rb'))



application = Flask(__name__)
app=application

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():

    if request.method == 'POST':

        try:

            # Get values from form
            temperature = float(request.form['Temperature'])
            rh = float(request.form['RH'])
            ws = float(request.form['Ws'])
            rain = float(request.form['Rain'])
            ffmc = float(request.form['FFMC'])
            dmc = float(request.form['DMC'])
            isi = float(request.form['ISI'])
            region = int(request.form['Region'])



            if temperature < -50 or temperature > 60:
                return render_template(
                    'predict.html',
                    error='Temperature must be between -50°C and 60°C.'
                )

            if rh < 0 or rh > 100:
                return render_template(
                    'predict.html',
                    error='Relative Humidity must be between 0% and 100%.'
                )

            if ws < 0:
                return render_template(
                    'predict.html',
                    error='Wind Speed cannot be negative.'
                )

            if rain < 0:
                return render_template(
                    'predict.html',
                    error='Rainfall cannot be negative.'
                )

            if ffmc < 0:
                return render_template(
                    'predict.html',
                    error='FFMC cannot be negative.'
                )

            if dmc < 0:
                return render_template(
                    'predict.html',
                    error='DMC cannot be negative.'
                )

            if isi < 0:
                return render_template(
                    'predict.html',
                    error='ISI cannot be negative.'
                )

            if region not in [0, 1]:
                return render_template(
                    'predict.html',
                    error='Please select a valid region.'
                )


            # Create DataFrame
            new_data = pd.DataFrame([[
                temperature,
                rh,
                ws,
                rain,
                ffmc,
                dmc,
                isi,
                region
            ]], columns=[
                'Temperature',
                'RH',
                'Ws',
                'Rain',
                'FFMC',
                'DMC',
                'ISI',
                'Region'
            ])


            # Prediction
            prediction = xgb_model.predict(new_data)

            result = round(float(prediction[0]), 2)


            # FWI danger category
            if result < 5.2:
                danger = 'Very Low'

            elif result < 11.2:
                danger = 'Low'

            elif result < 21.3:
                danger = 'Moderate'

            elif result < 38:
                danger = 'High'

            elif result < 50:
                danger = 'Very High'

            else:
                danger = 'Extreme'


            # Return result to HTML
            return render_template(
                'predict.html',
                results=result,
                danger=danger
            )


        except Exception as e:

            print("ERROR:", e)

            return render_template(
                'predict.html',
                error='Please check your inputs and try again.'
            )


    return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug=True)