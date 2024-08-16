from data_service import clean_data
import json


def test_data_service():
    csv_file = 'MSFT.US.test.csv'
    returned_data = clean_data(csv_file)
    print(returned_data)

    #save the data to a json file
    with open('cleaned_data.json', 'w') as f:
        #add data with variable names to json file:
        json.dump({
            'x_train': list(returned_data[0]),
            'x_test': list(returned_data[1]),
            'y_train': list(returned_data[2]),
            'y_test': list(returned_data[3]),
            'dates_train': list(returned_data[4]),
            'dates_test': list(returned_data[5])
        }, f)
    return


if __name__ == "__main__":
    test_data_service()
