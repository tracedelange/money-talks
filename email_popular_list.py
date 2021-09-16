import email_report
import requests
import datetime

def fetch_top_20():
    
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    week_ago_string = week_ago.strftime("%m-%d-%Y")
    fetch = requests.get("https://money-talks-sinatra-api.herokuapp.com/mentions/by-date/" + week_ago_string)
    resp = fetch.json()
    
    return resp

def email_top_20(popular_list, address='tracedelange@me.com'):

    date_string = datetime.date.today().strftime("%m-%d-%Y")
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    week_ago_string = week_ago.strftime("%m-%d-%Y")

    message_list = []

    for i in range(len(popular_list)):
        message_list.append(str(i+1) + '. ' + popular_list[i]['ticker']['ticker_name'] + ' -> ' + str(popular_list[i]['estimated_outreach']))

    message_data = ('\n').join(message_list)

    email_body = """

    Top Mentioned Tickers From %s To %s

    ------------------------------------------
    %s
    __________________________________________


    """ % (date_string, week_ago_string, message_data)

    email_report.email_report(email_body, address, 'Top Tickers - ' + date_string)

    return

def main(address='tracedelange@me.com'):
    print("sending out email for most popular tickers")

    data = fetch_top_20()

    if len(data) > 0:
        email_top_20(data, address)
    else:
        print('Something went wrong while fetching...')
    return


if __name__ == ("__main__"):
    main()