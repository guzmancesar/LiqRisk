import pandas 
from sklearn.model_selection import train_test_split
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report

def main():
	source_df = source_ingestion()
	

	#replace source data frame with normalized data

	normalized_df = normalize_all_data(source_df)
	
	normalized_df['liq_risk_identified'] = normalized_df.apply(assign_target_label, axis=1)
	
	tt_df = training_and_testing(normalized_df)



def assign_target_label(row):
    #all thresholds below are spitballs as I have no industry knowledge
    spread_threshold = 2  # Example threshold for bid-ask spread
    volume_threshold = -2  # Example threshold for trading volume
    volatility_threshold = 2  # Example threshold for volatility

    # Check if the observation meets the criteria for high liquidity risk
    if (row['spread_avg'] > spread_threshold) or (row['volume_total'] < volume_threshold) or (row['volatility_average'] > volatility_threshold):
        return 1  # High liquidity risk
    else:
        return 0  # Low liquidity risk




def source_ingestion():


	source_volatility = pandas.read_csv('btc_volatility.csv')
	source_volume = pandas.read_csv('btc_trading_vol.csv')
	source_spread = pandas.read_csv('btc_spread.csv')

	data_to_normalize = source_volatility[["Time","avg"]]
	data_to_normalize = data_to_normalize.rename(columns = {"avg":"volatility_average"})

	#print(list(source_volume.columns))

	#https://developers.google.com/machine-learning/data-prep/transform/normalization
	data_to_normalize = pandas.merge(data_to_normalize, source_volume[["Time", "total"]], on='Time')
	data_to_normalize = pandas.merge(data_to_normalize, source_spread[["Time", "avg"]], on='Time')

	data_to_normalize = data_to_normalize.rename(columns = {"total":"volume_total"})
	data_to_normalize = data_to_normalize.rename(columns = {"avg":"spread_avg"})



	data_to_normalize.to_csv('output.csv')
	return data_to_normalize
	

#normalization function for the raw data
def normalize_column(column):
    
    mean = column.mean()
    std_dev = column.std()
    normalized_column = (column - mean) / std_dev
    return normalized_column


def normalize_all_data(raw_dataframe):
	raw_dataframe["spread_avg"] = normalize_column(raw_dataframe['spread_avg'])
	raw_dataframe["volume_total"] = normalize_column(raw_dataframe['volume_total'])
	raw_dataframe["volatility_average"] = normalize_column(raw_dataframe['volatility_average'])


	return raw_dataframe

#def normalize_source_data(source_dataframe):


def training_and_testing(whole_data):
    feat = whole_data[['spread_avg', 'volume_total', 'volatility_average']]
    target = whole_data['liq_risk_identified']

    #no random state to allow use o f algo and take multiple outputs into consideration
    feat_train, feat_test, target_train, target_test = train_test_split(feat, target, test_size=0.3)

    model = svm.SVC(kernel ='linear')
    model.fit(feat_train, target_train)

    test_result = model.predict(feat_test)
    accuracy_res = accuracy_score(target_test, test_result)
    result = classification_report(target_test, test_result)

    print("SVM Accuracy:", accuracy_res)
    print("SVM Classification Report:\n", result)


main()



