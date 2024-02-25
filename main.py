import pandas 

def main():
	print("test")





def normalize_source():


	source_volatility = pandas.read_csv('btc_volatility.csv')
	source_volume = pandas.read_csv('btc_trading_vol.csv')
	source_spread = pandas.read_csv('btc_spread.csv')

	data_to_normalize = source_volatility[["Time","avg"]]
	data_to_normalize = data_to_normalize.rename(columns = {"avg":"volatility_average"})

	#print(list(source_volume.columns))


	data_to_normalize = pandas.merge(data_to_normalize, source_volume[["Time", "total"]], on='Time')
	data_to_normalize = pandas.merge(data_to_normalize, source_spread[["Time", "avg"]], on='Time')

	data_to_normalize = data_to_normalize.rename(columns = {"total":"volume_total"})
	data_to_normalize = data_to_normalize.rename(columns = {"avg":"spread_avg"})



	data_to_normalize.to_csv('output.csv')

	

normalize_source()