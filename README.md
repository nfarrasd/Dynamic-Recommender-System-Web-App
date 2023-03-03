# Dynamic Recommender System Web-App

Link: [Website](https://recommendation-system-fe.vercel.app/)

This is a side-project created in order to build a recommendation system pipeline for users as well as segmenting the users based on an e-commerce transactional data by the following steps:

1.   Extract the data from Kaggle website
2.   Transform the data (making sure it is usable and consistent)
3.   Make a Recommendation System model using Turicreate
4.   Segmenting the products and customers using WordCloud and Clustering based on the transaction histories
5.   Deploy the Recommender Pipeline with Flask so that users can freely enter new transactions and get recommendations

**Note**: 
1. Steps 1-4 are not shown in this repo, only the analysis and model summary will be presented below. (Since this repo focuses more on the RecSys model deployment and back-end).
2. This can only be run through Ubuntu since Turicreate module does not suppoert Windows OS (except by using WSL).
3. Please put the 'index.html' file in a folder called 'template'.

## Summary
1. Recommendation System Pipeline was built under 2 scenarios:
    - **Purchase Counts with Pearson Similarity** method for old users
    - **Popularity Model with Binary Input** method for new users
2. Followings are the **top 5 most popular products**:

    - White Hanging Heart T-Light Holder	(2028 sold)
    - Regency Cakestand 3 Tier (1724 sold)
    - Jumbo Bag Red Retrospot	(1618 sold)
    - Assorted Colour Bird Ornament	(1408 sold)
    - Party Bunting (1397 sold)
3. Products of the following categories are **more likely** to **attract** customers:
    - Heart
    - Vintage
    - Bag
    - Retrospot
    - Cake
  
    with **Red**, **Pink**, and **Blue** colours.
4. The weekly # of transactions and Gross Revenue Value (GPV) have an **increment trend**, with an increment of **+45.07%** and **+17.89%** overall, respectively.
5. Followings are the **top 3 countries** with the **most # of transactions**:
    - United Kingdom (475309 transactions)
    - Germany	(8635 transactions)
    - France	(8065 transactions)
6. Followings are the **top 3 countries** with the **highest GPV**:
    - United Kingdom (\$ 8747561.66)
    - Netherlands	(\$ 283889.34)
    - Ireland	(\$ 271164.30)

## Credit
[Felix Fernando](felixFern (Felix Fernando)) as the one who designed the webpage' UI to be more interactive.
