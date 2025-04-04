import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io
import time
from flask import Flask, jsonify, render_template, request, logging, render_template_string
import schedule
import threading
import matplotlib
matplotlib.use('Agg')
import requests
from bs4 import BeautifulSoup



top_100_nyse_tickers = {
    'Apple Inc.': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'NVIDIA': 'NVDA',
    'Alphabet Inc.': 'GOOGL',
    'Meta Platforms': 'META',
    'Tesla Inc.': 'TSLA',
    'Berkshire Hathaway': 'BRK-B',
    'Johnson & Johnson': 'JNJ',
    'UnitedHealth Group': 'UNH',            
    'Exxon Mobil': 'XOM',
    'Walmart': 'WMT',
    'Procter & Gamble': 'PG',
    'Visa Inc.': 'V',
    'JPMorgan Chase': 'JPM',
    'Home Depot': 'HD',
    'Pfizer': 'PFE',
    'Chevron': 'CVX',
    'Mastercard': 'MA',
    'AbbVie': 'ABBV',
    'Coca-Cola': 'KO',
    'PepsiCo': 'PEP',
    'Eli Lilly': 'LLY',
    'Intel': 'INTC',

}

# Function to get current stock price
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')
    if not data.empty:
        return data['Close'].iloc[-1]
    else:
        return None

# Function to get stock info
def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        'debtToEquity': info.get('debtToEquity', 'N/A'),
        'roe': info.get('returnOnEquity', 'N/A'),
        'pegRatio': info.get('pegRatio', 'N/A')
    }

# Function to send email alert with attachment
def email_alert(subject, body, to, images):
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['to'] = to
    user = "joepip699@gmail.com"
    msg['from'] = user
    password = "" #password 

    msg.attach(MIMEText(body, 'html'))

    for img_data, img_id in images:
        img_cid = img_id[1:-1]
        image_part = MIMEImage(img_data, 'png')
        image_part.add_header('Content-ID', f'<{img_cid}>')
        msg.attach(image_part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Job function to check stock price movement and send email
def job():
    print("Running job...")
  #  email_body = ""
  #  images = []
   # for company, ticker in top_100_nyse_tickers.items():
    #    current_price = get_stock_price(ticker)
     #   if current_price is not None:
      #      print(f"{company} ({ticker}) current price: {current_price}")
       #     if f'previous_price_{ticker}' not in job.__dict__:
        #        setattr(job, f'previous_price_{ticker}', current_price)

         #   previous_price = getattr(job, f'previous_price_{ticker}')
          #  change_percentage = ((current_price - previous_price) / previous_price) * 100
           # print(f"{company} ({ticker}) change percentage: {change_percentage:.2f}%")

            #stock_info = get_stock_info(ticker)
            #debt_to_equity = stock_info['debtToEquity']
            #roe = stock_info['roe']
            #peg = stock_info['pegRatio']

            #relevant_info = debt_to_equity if debt_to_equity != 'N/A' else 26
            #roe_info = roe if roe != 'N/A' else 1
            #peg_info = peg if peg != 'N/A' else 2

            #if change_percentage >= 1 and relevant_info <= 25 and roe_info <= 0.15 and peg_info <= 1:
               # email_body += f"{company} ({ticker}) has increased by {change_percentage:.2f}% in the last 30 minutes. It has a commendable debt to equity ratio of {debt_to_equity}. Its ROE is promising at {roe}. Its PEG ratio is also impressive at {peg}. Buying is highly recommended.<br>"
                # Generate plot for the stock price change
                #data = pd.DataFrame({'Price': [previous_price, current_price], 'Time': ['Previous', 'Current']})
                #plt.figure()
                #sns.lineplot(x='Time', y='Price', data=data)
                #plt.title(f'{company} ({ticker}) Price Change')
                #plt.xlabel('Time')
                #plt.ylabel('Price')
                #buf = io.BytesIO()
                #plt.savefig(buf, format='png')
                #buf.seek(0)
                #images.append((buf.read(), f"<{ticker}_img>"))
            #elif change_percentage > 0 and change_percentage <= 1 and relevant_info <= 25 and roe_info <= 0.15:
              #  email_body += f"{company} ({ticker}) has increased by {change_percentage:.2f}% in the last 30 minutes. It has a commendable debt to equity ratio of {debt_to_equity}. Its ROE is promising at {roe}. Its PEG ratio is also impressive at {peg}. Buying is recommended.<br>"
                # Generate plot for the stock price change
                #data = pd.DataFrame({'Price': [previous_price, current_price], 'Time': ['Previous', 'Current']})
                #plt.figure()
                #sns.lineplot(x='Time', y='Price', data=data)
                #plt.title(f'{company} ({ticker}) Price Change')
                #plt.xlabel('Time')
                #plt.ylabel('Price')
                #buf = io.BytesIO()
                #plt.savefig(buf, format='png')
                #buf.seek(0)
                #images.append((buf.read(), f"<{ticker}_img>"))
            #elif change_percentage == 0 and relevant_info <= 25 and roe_info <= 0.15:
              #  email_body += f"{company} ({ticker}) has not changed {change_percentage:.2f}% in the last 30 minutes. It has a commendable debt to equity ratio of {debt_to_equity}. Its ROE is promising at {roe}. Its PEG ratio is also impressive at {peg}. Consider holding or buying a small amount.<br>"
                # Generate plot for the stock price change
               #data = pd.DataFrame({'Price': [previous_price, current_price], 'Time': ['Previous', 'Current']})
               # plt.figure()
               # sns.lineplot(x='Time', y='Price', data=data)
               # plt.title(f'{company} ({ticker}) Price Change')
               # plt.xlabel('Time')
               # plt.ylabel('Price')
               # buf = io.BytesIO()
               # plt.savefig(buf, format='png')
               # buf.seek(0)
               # images.append((buf.read(), f"<{ticker}_img>"))

            #setattr(job, f'previous_price_{ticker}', current_price)
        #else:
      #      print(f"Failed to retrieve stock price for {company} ({ticker})")

    #if email_body:
     #   email_alert("Stock Alert", email_body, "sandeagle1@yahoo.com", images)





app = Flask(__name__)

email_term = ""
# You need to define this dictionary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock-data')
def get_stock_data():
    data_list = []
    for company, ticker in top_100_nyse_tickers.items():
        data = process_stock(ticker, company)
        if data:
            data_list.append(data)
    print("API returning data:", data_list)
    return jsonify(data_list)
@app.route('/email-registration')
def email_registration():
    return render_template('3 page of website.html')
@app.route('/another-page', methods=['GET', 'POST'])

def another_page():
    global email_term
    if request.method == 'POST':
        if 'email' in request.form:
            email_term = request.form.get('email', '').strip()
            return jsonify({"message": "Email registered successfully!"})
        elif 'search' in request.form:
            search_term = request.form.get('search', '')
            data_list = []
            for ticker in search_term.split(','):
                ticker = ticker.strip()
                data = process_stock(ticker, ticker)
                if data:
                    data_list.append(data)
            return jsonify(data_list)
    elif request.method == 'GET':
        return render_template('2 page of website.html')

def process_stock(ticker, company):
    current_price = get_stock_price(ticker)
    if current_price is not None:
        print(f"{company} ({ticker}) current price: {current_price}")
        if f'previous_price_{ticker}' not in process_stock.__dict__:
            setattr(process_stock, f'previous_price_{ticker}', current_price)
        
        previous_price = getattr(process_stock, f'previous_price_{ticker}')
        change_percentage = ((current_price - previous_price) / previous_price) * 100
        print(f"{company} ({ticker}) change percentage: {change_percentage:.2f}%")

        stock_info = get_stock_info(ticker)
        debt_to_equity = stock_info['debtToEquity']
        roe = stock_info['roe']
        peg = stock_info['pegRatio']

        buy_recommendation = get_buy_recommendation(change_percentage, debt_to_equity, roe, peg)

        setattr(process_stock, f'previous_price_{ticker}', current_price)

        return {
            'company': company,
            'ticker': ticker,
            'price': current_price,
            'debtToEquity': debt_to_equity,
            'roe': roe,
            'pegRatio': peg,
            'change_percentage': f"{change_percentage:.2f}%",
            'buy_recommendation': buy_recommendation
        }
    return None

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')
    return data['Close'].iloc[-1] if not data.empty else None

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        'debtToEquity': info.get('debtToEquity', 'N/A'),
        'roe': info.get('returnOnEquity', 'N/A'),
        'pegRatio': info.get('pegRatio', 'N/A')
    }

def get_buy_recommendation(change_percentage, debt_to_equity, roe, peg):
    relevant_info = debt_to_equity if debt_to_equity != 'N/A' else 26
    roe_info = roe if roe != 'N/A' else 1
    peg_info = peg if peg != 'N/A' else 2

    if change_percentage >= 1 and relevant_info <= 25 and roe_info <= 0.15 and peg_info <= 1:
        return "Buying is highly recommended."
    elif change_percentage > 0 and change_percentage <= 1 and relevant_info <= 25 and roe_info <= 0.15:
        return "Buying is recommended."
    elif change_percentage == 0:
        return "Hold"
    return ""

def email_alert(subject, body, to, images):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = to
    user = "joepip699@gmail.com"
    msg['From'] = user
    password = ""

    msg.attach(MIMEText(body, 'html'))

    for img_data, img_id in images:
        img_cid = img_id[1:-1]
        image_part = MIMEImage(img_data, 'png')
        image_part.add_header('Content-ID', f'<{img_cid}>')
        msg.attach(image_part)
      
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def job():
    print("Running job...")
    email_body = ""
    images = []
    for company, ticker in top_100_nyse_tickers.items():
        current_price = get_stock_price(ticker)
        if current_price is not None:
            print(f"{company} ({ticker}) current price: {current_price}")
            if f'previous_price_{ticker}' not in job.__dict__:
                setattr(job, f'previous_price_{ticker}', current_price)

            previous_price = getattr(job, f'previous_price_{ticker}')
            change_percentage = ((current_price - previous_price) / previous_price) * 100
            print(f"{company} ({ticker}) change percentage: {change_percentage:.2f}%")

            stock_info = get_stock_info(ticker)
            debt_to_equity = stock_info['debtToEquity']
            roe = stock_info['roe']
            peg = stock_info['pegRatio']

            relevant_info = debt_to_equity if debt_to_equity != 'N/A' else 26
            roe_info = roe if roe != 'N/A' else 1
            peg_info = peg if peg != 'N/A' else 2

            if change_percentage >= 1 and relevant_info <= 25 and roe_info <= 0.15 and peg_info <= 1:
                email_body += f"{company} ({ticker}) has increased by {change_percentage:.2f}% in the last 30 minutes. It has a commendable debt to equity ratio of {debt_to_equity}. Its ROE is promising at {roe}. Its PEG ratio is also impressive at {peg}. Buying is highly recommended.<br>"
                # Generate plot for the stock price change
                data = pd.DataFrame({'Price': [previous_price, current_price], 'Time': ['Previous', 'Current']})
                plt.figure()
                sns.lineplot(x='Time', y='Price', data=data)
                plt.title(f'{company} ({ticker}) Price Change')
                plt.xlabel('Time')
                plt.ylabel('Price')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                images.append((buf.read(), f"<{ticker}_img>"))
            elif change_percentage > 0 and change_percentage <= 1 and relevant_info <= 25 and roe_info <= 0.15:
                email_body += f"{company} ({ticker}) has increased by {change_percentage:.2f}% in the last 30 minutes. It has a commendable debt to equity ratio of {debt_to_equity}. Its ROE is promising at {roe}. Its PEG ratio is also impressive at {peg}. Buying is recommended.<br>"
                # Generate plot for the stock price change
                data = pd.DataFrame({'Price': [previous_price, current_price], 'Time': ['Previous', 'Current']})
                plt.figure()
                sns.lineplot(x='Time', y='Price', data=data)
                plt.title(f'{company} ({ticker}) Price Change')
                plt.xlabel('Time')
                plt.ylabel('Price')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                images.append((buf.read(), f"<{ticker}_img>"))
            elif change_percentage == 0 and relevant_info <= 25 and roe_info <= 0.15:
                email_body += f"{company} ({ticker}) has not changed {change_percentage:.2f}% in the last 30 minutes. It has a commendable debt to equity ratio of {debt_to_equity}. Its ROE is promising at {roe}. Its PEG ratio is also impressive at {peg}. Consider holding or buying a small amount.<br>"
             # Generate plot for the stock price change
                data = pd.DataFrame({'Price': [previous_price, current_price], 'Time': ['Previous', 'Current']})
                plt.figure()
                sns.lineplot(x='Time', y='Price', data=data)
                plt.title(f'{company} ({ticker}) Price Change')
                plt.xlabel('Time')
                plt.ylabel('Price')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                images.append((buf.read(), f"<{ticker}_img>"))

            setattr(job, f'previous_price_{ticker}', current_price)
        else:
            print(f"Failed to retrieve stock price for {company} ({ticker})")

    if email_body and email_term:
        email_alert("Stock Alert", email_body, email_term, images)





def get_historical_free_cash_flow(ticker):
    """
    Retrieve historical free cash flow data using yfinance.

    Parameters:
    ticker (str): The ticker symbol of the company (e.g., 'LNTH').

    Returns:
    pd.Series: Historical free cash flow data.
    """
    stock = yf.Ticker(ticker)
    cash_flow = stock.cashflow
    fcf = cash_flow.loc['Free Cash Flow']
    fcf = fcf.dropna()  # Remove any NaN values
    return fcf

def project_free_cash_flows(historical_fcf, growth_rate, years):
    """
    Project future free cash flows based on historical data and a growth rate.

    Parameters:
    historical_fcf (pd.Series): Historical free cash flow data.
    growth_rate (float): Annual growth rate (e.g., 0.05 for 5%).
    years (int): Number of years to project.

    Returns:
    list: Projected free cash flows for the specified number of years.
    """
    last_fcf = historical_fcf.iloc[-1]
    projected_fcfs = [last_fcf * (1 + growth_rate) ** i for i in range(1, years + 1)]
    return projected_fcfs

def calculate_intrinsic_value(projected_fcfs, discount_rate, terminal_growth_rate):
    """
    Calculate the intrinsic value of a company using DCF analysis.
    
    Parameters:
    projected_fcfs (list): List of projected free cash flows for each year.
    discount_rate (float): Discount rate (as a decimal, e.g., 0.09 for 9%).
    terminal_growth_rate (float): Perpetual growth rate (as a decimal, e.g., 0.03 for 3%).
    
    Returns:
    float: Intrinsic value of the company in billions.
    """
    # Calculate the terminal value
    terminal_value = projected_fcfs[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    
    # Discount the projected free cash flows
    present_values = [
        fcf / (1 + discount_rate) ** (i + 1) 
        for i, fcf in enumerate(projected_fcfs)
    ]
    
    # Discount the terminal value
    terminal_value_pv = terminal_value / (1 + discount_rate) ** len(projected_fcfs)
    
    # Sum the present values of the projected free cash flows and the terminal value
    intrinsic_value = sum(present_values) + terminal_value_pv
    
    return intrinsic_value / 1000  # Convert to billions


  
def analyze_stock(ticker):
    fcf_data = get_historical_free_cash_flow(ticker)
    
    print("Historical Free Cash Flow Data (in millions):")
    print(fcf_data)

    growth_rate = 0.05  # 5% annual growth rate
    years = 5  # Project 5 years into the future

    projected_fcfs = project_free_cash_flows(fcf_data, growth_rate, years)
    print("Projected Free Cash Flows (in millions):")
    print(projected_fcfs)

    discount_rate = 0.1  # 10%
    terminal_growth_rate = 0.03  # 3%

    intrinsic_value = calculate_intrinsic_value(projected_fcfs, discount_rate, terminal_growth_rate)
    print(f"The intrinsic value is: ${intrinsic_value:.2f} billion USD")

    suggested_value = intrinsic_value * 0.7
    print(f"A good Market Cap is: ${suggested_value:.2f} billion USD")

    historical_fcf_dict = {date.strftime('%Y-%m-%d'): value for date, value in fcf_data.items()}
    
    
    return {
        'historical_fcf': historical_fcf_dict,  # Convert Series to dict for JSON serialization
        'projected_fcfs': projected_fcfs,
        'intrinsic_value': intrinsic_value,
        'suggested_value': suggested_value,
    }

@app.route("/buffet-stock", methods=['GET', 'POST'])
def buffet_stock():
    if request.method == 'POST':
        ticker = request.form["ticker"].strip()
        analysis_result = analyze_stock(ticker)
        return jsonify(analysis_result)
    
    return render_template('4 page of website.html')    



@app.route("/quizparatu", methods=['GET', 'POST'])
def quiz_template():
    return render_template('quizz.html')


@app.route("/congress-per")
def congress_per():
    return render_template('5 page of website.html')

@app.route("/fetch-trades")
def fetch_trades():
    trades = []
    url = 'https://www.capitoltrades.com/trades'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        trade_table = soup.find('table')
        
        if trade_table:
            trade_body = trade_table.find('tbody')
            
            if trade_body:
                for row in trade_body.find_all('tr'):
                    columns = row.find_all('td')
                    if columns:
                        trade = {
                            'date': columns[0].text.strip(),
                            'representative': columns[1].text.strip(),
                            'ticker': columns[2].text.strip(),
                            'transaction': columns[3].text.strip(),
                            'amount': columns[4].text.strip(),
                        }
                        trades.append(trade)
            else:
                print('Tbody not found within the table. Please check the HTML structure and adjust the selector.')
        else:
            print('Trade table not found. Please check the HTML structure and adjust the selector.')
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')
    
    return jsonify(trades)
    
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


        

if __name__ == '__main__':
    print("Starting scheduler...")
    schedule.every(1).minutes.do(job)
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    app.run(debug=True)
