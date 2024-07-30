import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io

def test_model(model, x_test, y_test, dates_test):
    x_test = np.array(x_test).reshape(-1, 1)
    y_pred = model.predict(x_test)
    print(f"x_test in testing service: {x_test}")
    print(f"y_pred in testing service: {y_pred}")
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse}")

    # Create a BytesIO object to save the plot in-memory
    plot_stream = io.BytesIO()

    # Plot the results
    plt.figure(figsize=(14, 7))
    plt.plot(dates_test, y_test, label='Actual')
    plt.plot(dates_test, y_pred, label='Predicted')

    # Format the date on the x-axis
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=120))  # Set major ticks every 120 days
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.gcf().autofmt_xdate()  # Rotate date labels vertically

    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('MSFT Stock Price Prediction')
    plt.legend()
    plt.grid(True)

    # Save the plot to the BytesIO object
    plt.savefig(plot_stream, format='png')
    plt.close()

    # Get the binary data from the BytesIO object
    plot_stream.seek(0)
    plot_binary = plot_stream.read()

    return rmse, plot_binary
