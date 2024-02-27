import pandas 

def main():
	source_df = source_ingestion()
	

	#replace source data frame with normalized data

	normalized_df = normalize_all_data(source_df)
	print(normalized_df)
	




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

main()



