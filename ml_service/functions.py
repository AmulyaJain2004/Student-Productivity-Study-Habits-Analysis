# response = requests.get(API_URL) # Fetch data from Django API
# if response.status_code == 200:
#     data = response.json()
#     df = pd.DataFrame(data)
#     print("Data Loaded Successfully!")
# else:
#     print("Error fetching data:", response.status_code)

def get_data(API_URL):
    try:
        response = requests.get(API_URL) # Fetch data from Django API
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
    else:
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            print("Data Loaded Successfully!")
            return df
        else:
            print("Error fetching data:", response.status_code)
            return None


def dataframeInfo(df):
    print("\nDataframe Head:")
    print(df.head()) # Display the first 5 rows
    
    print("\nDataframe Random data:")
    print(df.sample(5)) # Display 5 random rows
    
    print("\nDataframe Tail:")
    print(df.tail()) # Display the last 5 rows
    
    print("\nDataframe Columns:")
    print(df.columns) # Display the column names
    
    print("\nDataframe Shape:")
    print(df.shape) # Display the number of rows and columns
    
    print("Dataframe Info:")
    print(df.info()) # Display the data types and missing values
    
    print("\nDataframe Description:")
    print(df.describe()) # Display the summary statistics
    return

