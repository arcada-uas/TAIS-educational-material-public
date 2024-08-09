from data_service import clean_data


def test_service():
    csv_file = 'MSFT.US.csv'
    returned_data = clean_data(csv_file)
    print(returned_data)
    return

test_service()
