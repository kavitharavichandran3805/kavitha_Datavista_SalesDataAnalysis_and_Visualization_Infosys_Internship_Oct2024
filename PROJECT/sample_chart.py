import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta
from textblob import TextBlob

def graph(average_sentiment_score,start_date,today):
    months = []
    current_date = start_date
    while current_date < today - relativedelta(days=31):  
        months.append(current_date.strftime('%b %Y'))
        current_date += timedelta(days=30) 

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')


    xpos = range(len(months))
    ypos = [1] * len(months)
    zpos = [0] * len(months)
    dx = [0.5] * len(months)
    dy = [0.5] * len(months)
    dz = average_sentiment_score

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='skyblue')
    ax.set_xlabel('Months', fontsize=12, fontweight='bold',labelpad=30)
    ax.set_ylabel('Sentiment Score', fontsize=12, fontweight='bold')
    ax.set_zlabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('COMMENTS ANALYSIS', fontsize=14, fontweight='bold')

    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=10)

    ax.set_yticks([])
    ax.set_zticks([])

    plt.tight_layout()
    plt.show()


def analyze_sentiment(comment_dict):
    combined_text = f"{comment_dict['Reviews']} {comment_dict['Comments']}"
    blob = TextBlob(combined_text)
    sentiment_polarity = blob.sentiment.polarity
    return sentiment_polarity

def calculate_score(comment_dict):
    ratings = int(comment_dict['Ratings'])
    ratings_score = ratings * 20
    sentiment_polarity = analyze_sentiment(comment_dict)
    reviews_comments_score = (sentiment_polarity + 1) * 50
    final_score = (ratings_score + reviews_comments_score) / 2
    return final_score

def sentimental_score(dict1):
    if dict1:
        length=len(dict1)
        today = dt.today()
        one_year_ago = today - relativedelta(months=12)
        start_date =one_year_ago
        sentiment_score=[0]*12
        no_of_comments=[0]*12

        for item in dict1:
            if isinstance(item['Date'], str):
                item['Date'] = dt.strptime(item['Date'], '%d/%m/%Y')
            if start_date <= item['Date']<= today:
                month_number = (item['Date'].year-start_date.year)*12+item['Date'].month-start_date.month
                new_dict = {'Ratings': item['Ratings'], 'Reviews': item['Reviews'], 'Comments': item['Comments']}
                score=calculate_score(new_dict)
                sentiment_score[month_number-1]+=score
                no_of_comments[month_number-1]+=1
        average_sentiment_score=[]
        for score, months in zip(sentiment_score, no_of_comments):
            if months != 0:
                average_sentiment_score.append(score / months)
            else:
                average_sentiment_score.append(0)
        print(average_sentiment_score)
        graph(average_sentiment_score,start_date,today)
    else:
        print('NO REVIEWS')
       