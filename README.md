# Dynamic Recommender System Web-App

Link: [Website](https://recommendation-system-fe.vercel.app/)

This is a side-project made by Moch Nabil Farras Dhiya (me) in order to implement my knowledge on recommendation system algorithm and also model deployment using Flask.

## Guide
Please always refer to this database below when using all the features in the web-app.
**Databases**
1. [User Database](https://docs.google.com/spreadsheets/d/1sssW6fHPxilpS4gafUbfdR5s3zzlYI2Wah8Oc1QZIB4/edit?usp=sharing)
2. [Stock Database](https://docs.google.com/spreadsheets/d/1JIwFwvc1HKbZCXHEOTi3FSdWnNdXN62yCqYCkoYHCnY/edit?usp=sharing)
3. [Transaction Database](https://docs.google.com/spreadsheets/d/1xluzFXJoYJ5s3KoEITQp38L098NbBShCiok-71toF4E/edit?usp=sharing)

**Optional Steps**
1. Enter a new user ID at the "Add Customer Data" section
2. Enter a new stock data which consists of Stock Code and Item Description at the "Add Stock Data" section.
3. Enter a new transaction history

**Main Feature**
Enter an existing user ID, then wait several seconds for the backend to process. In a short while, 10 recommended items (Stock Code) will pop up.

## Business Understanding
Due to the high-level of competitiveness in today's industry, it is a given for company to have a better understanding on their customer' nature and deliver the best service. In order to do so, recommendation system algorithm is one of the algorithms which are of the main concern among the company. Many company developed a complex algorithm using many method, such as multi-stage neural network, association rules, etc. 

### Problem
Build a recommendation system algorithm which can recommend items to new users and old users (which already made a purchase) differently.

### Analytical Approach
1. Distinguish old users and new users, then experimenting with different models for both cases, which includes the usage of pearson and cosine similarity approaches.
2. Evaluate the models performance, then pick the model which has the lowest RMSE for both cases.
3. Do additional analysis on the dataset to gain a better understanding of the customer base location, and also the most popular product names and categories.

## Steps
1.   Extract the data from Kaggle website
2.   Transform the data (making sure it is usable and consistent)
3.   Make a Recommendation System model using existing package for simplicity
4.   Deploy the Recommender Pipeline with Flask with add-in features (can enter new users, products, transactions)

## Summary
Recommendation System Pipeline was built under 2 scenarios:
    1. **Purchase Counts with Pearson Similarity** method for old users
    2. **Popularity Model with Binary Input** method for new users

## Credit
[Felix Fernando](https://github.com/FelixFern) as the one who designed the webpage' UI to be more interactive.
