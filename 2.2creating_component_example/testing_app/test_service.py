import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def test_model(model, x_test, y_test, dates_test):
    x_test = np.array(x_test).reshape(-1, 1)
    print("x_test in test service: " + str(x_test))
    y_pred = model.predict(x_test)
    print("y_pred in test service: " + str(y_pred))
    print("y_test in test service: " + str(y_test))
    print("dates_test in test service: " + str(dates_test))
    print("x_test in test service: " + str(x_test))
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse}")

    #plot the results:
    
    plt.figure(figsize=(14, 7))
    plt.plot(dates_test, y_test, label='Actual')
    plt.plot(dates_test, y_pred, label='Predicted')

    # Format the date on the x-axis
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=120))  # Set major ticks every 10 days
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))


    plt.gcf().autofmt_xdate() 


    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('MSFT Stock Price Prediction')
    plt.legend()
    plt.grid(True)
    current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plot_filename = f'test_plot_{current_time_str}.png'
    plt.savefig(plot_filename)

    return rmse, plot_filename