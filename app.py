from flask import Flask , render_template , request , jsonify
import prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# api listening to POST requests and predicting sentiments
@app.route('/predict' , methods = ['POST'])
def predict():

    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status' : 'error',
                    'message' : 'Empty Review'}
    
    else:

        # calling the predict method from prediction.py module
        sentiment , path = prediction.predict(review)
        response = {'status' : 'success',
                    'message' : 'Got it',
                    'sentiment' : sentiment,
                    'path' : path}

    return jsonify(response)


# Creating an API to save the review, user clicks on the Save button
@app.route('/save' , methods = ['POST'])
def save():
    # Extracting data, product name, review, and sentiment from the JSON data
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # Creating a final variable separated by commas
    data_entry = f"{date},{product},{review},{sentiment}"

    # Open the file in 'append' mode and log the data
    with open('static/assets/datafiles/updated_product_dataset.csv', 'a') as file:
        file.write(data_entry)

    # Return a success message
    return jsonify({'status': 'success', 'message': 'Data Logged'})


if __name__  ==  "__main__":
    app.run(debug = True)