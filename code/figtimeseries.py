import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def processcsv(csvfile='NVL.csv'):
	data = pd.read_csv(csvfile)
	dt = pd.to_datetime({'year': data.years,
		                 'month': data.months,
		                 'day': data.days})
	data['date'] = dt

	# reorder data by datetime
	data.sort_values(by=['date'], inplace=True, ascending=True)

	return data




def plotsumrunoff(csvfile1='MDV.csv', csvfile2='MDVdegday.csv', varname='degreedays_sum', ylabel='Daily sum of degree day pixels (K)', titl='Timeseries of cumulative degree days in '):

	"""
	Plots timeseries subplot for summers of the spatial sum of sfc runoff

	@param csvfile directory of csv file 

	"""

	data1 = processcsv(csvfile1)
	data2 = processcsv(csvfile2)

	#plot each summer timeseries on a seperate subplot
	ncol=1
	nrow = 7

	fig, axes = plt.subplots(nrow, ncol, figsize=(20,40), sharex=False, sharey=True, constrained_layout=True)
	for iplot in range(nrow):
		i = iplot // ncol
		dtmin = datetime(year=(i+2013), month=11, day=1)
		dtmax = dtmin + timedelta(days=150)
		summer1 = data1[(data1['date'] >= dtmin) & (data1['date'] < dtmax)]
		summer2 = data2[(data2['date'] >= dtmin) & (data2['date'] < dtmax)]
		axes[i].plot(summer1.date, summer1.sfcrunoffs, color='blue', label='surface runoff')
		axes[i].set_ylabel("Daily total surface runoff (mm)", color='blue', fontsize=14)
		#axes[i].legend(loc=0)

		ax2=axes[i].twinx()
		ax2.plot(summer2.date, summer2[varname], label='u10_avg', color='orange')
		ax2.plot(summer2.date, summer2['v_avg'], label='v10_avg', color='red')
		ax2.plot(summer2.date, np.zeros(len(summer2.date), dtype=np.int32), color='grey')
		ax2.set_ylabel(ylabel,color="orange",fontsize=14)
		ax2.set_ylim(bottom=data2[varname].min(), top=data2['v_avg'].max())

	lines_1, labels_1 = axes[i].get_legend_handles_labels()
	lines_2, labels_2 = ax2.get_legend_handles_labels()

	lines = lines_1 + lines_2
	labels = labels_1 + labels_2

	axes[0].legend(lines, labels, loc=0)

	fig.supxlabel("Date")
	#fig.supylabel("Daily total surface runoff (mm)")
	fig.suptitle(titl + csvfile1.split(".")[0], fontsize=25)
	#plt.subplots_adjust(hspace=0.1)
	#plt.tight_layout()

	plt.savefig(varname + csvfile1.split(".")[0] + '.png')
	plt.close('all')

