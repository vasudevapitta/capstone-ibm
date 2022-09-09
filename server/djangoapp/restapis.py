import requests
import json
# import related models here
from .models import CarMake, CarModel, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    # print('json_result from line 31', json_result)    

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                
                                   short_name=dealer_doc["short_name"],st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result[0]

        # print("line 70 restapis",json_result)
        dealer_doc = dealers
        print("0th address element line 73",dealers["address"])
        dealer_obj = CarDealer(address=dealers["address"], city=dealers["city"],
                                id=dealers["id"], lat=dealers["lat"], long=dealers["long"], full_name=dealers["full_name"],
                                
                                short_name=dealers["short_name"],st=dealers["st"], zip=dealers["zip"])
    return dealer_obj

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealership=dealer_id)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        print(reviews)
        for review_doc in reviews:
            if(review_doc["purchase"]):
                review_obj = DealerReview(
                    name=review_doc["name"],
                    dealership=review_doc["dealership"],
                    review=review_doc["review"],
                    # sentiment=analyze_review_sentiments(review_doc["review"]),
                    sentiment="neutral",
                    purchase=review_doc["purchase"],
                    purchase_date=review_doc["purchase_date"],
                    car_make=review_doc["car_make"],
                    car_model=review_doc["car_model"],
                    car_year=review_doc["car_year"]
                )
                # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            else:
                review_obj = DealerReview(
                    name=review_doc["name"],
                    dealership=review_doc["dealership"],
                    review=review_doc["review"],
                    # sentiment=analyze_review_sentiments(review_doc["review"]),
                    sentiment="neutral",
                    purchase=review_doc["purchase"]
                )
                # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results
    
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



