import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

def processcsv(csvfile='NVL.csv'):
	data = pd.read_csv(csvfile)
	dt = pd.to_datetime({'year': data.years,
		                 'month': data.months,
		                 'day': data.days})
	data['date'] = dt

	# reorder data by datetime
	data.sort_values(by=['date'], inplace=True, ascending=True)

	return data

def plotsfcrunoff(csvfile1='NVL_new.csv', csvfile2='MDV_new.csv', varname='sfcrunoffs', ylabel='Daily sum of degree day pixels (K)', titl='Timeseries of cumulative surface runoff in '):

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

		axes[i].plot(summer1.date, summer1.sfcrunoffs, color='red', label='NVL')
		axes[i].plot(summer1.date, summer2.sfcrunoffs, color='blue', label='MDV')
		axes[i].plot(summer1.date, (summer1.sfcrunoffs * (1088/2641)), color='green', label='NVL scaled') #scaling factor calculated from pixel area

		axes[i].set_ylabel("Daily total surface runoff (mm)", color='black', fontsize=14)
		axes[i].set_ylim(bottom=data1[varname].min(), top=data1[varname].max())
		#axes[i].legend(loc=0)

	lines_1, labels_1 = axes[i].get_legend_handles_labels()

	lines = lines_1
	labels = labels_1

	axes[0].legend(lines, labels, loc=0)

	fig.supxlabel("Date")
	#fig.supylabel("Daily total surface runoff (mm)")
	fig.suptitle(titl + csvfile1.split(".")[0].split("_")[0] + ' and ' + csvfile2.split(".")[0].split("_")[0], fontsize=25)
	#plt.subplots_adjust(hspace=0.1)
	#plt.tight_layout()

	#plt.savefig(varname + csvfile1.split(".")[0] + '.png')
	plt.savefig(varname + csvfile1.split(".")[0].split("_")[0] + csvfile2.split(".")[0].split("_")[0] + '.png')
	plt.close('all')



def plotdegreeday(csvfile1='MDV_new.csv', csvfile2='MDV_newdegday.csv', varname='degreedays_sum', ylabel='Daily sum of degree day pixels (K)', titl='Timeseries of cumulative degree days in '):

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
		ax2.plot(summer2.date, summer2[varname], label=varname, color='orange')
		#ax2.plot(summer2.date, summer2['v_avg'], label='v10_avg', color='red')
		#ax2.plot(summer2.date, np.zeros(len(summer2.date), dtype=np.int32), color='grey')
		ax2.set_ylabel(ylabel,color="orange",fontsize=14)
		ax2.set_ylim(bottom=data2[varname].min(), top=data2[varname].max())

	lines_1, labels_1 = axes[i].get_legend_handles_labels()
	lines_2, labels_2 = ax2.get_legend_handles_labels()

	lines = lines_1 + lines_2
	labels = labels_1 + labels_2

	axes[0].legend(lines, labels, loc=0)

	fig.supxlabel("Date")
	#fig.supylabel("Daily total surface runoff (mm)")
	fig.suptitle(titl + csvfile1.split(".")[0].split("_")[0], fontsize=25)
	#plt.subplots_adjust(hspace=0.1)
	#plt.tight_layout()

	#plt.savefig(varname + csvfile1.split(".")[0] + '.png')
	plt.savefig(varname + csvfile1.split(".")[0].split("_")[0] + '.png')
	plt.close('all')


def plotwindvector(csvfile1='MDV_new.csv', csvfile2='MDV_newwind.csv', 
					ylabel='Windspeed (m/s)', 
					titl='Timeseries of daily average wind in '):

	"""
	Plots timeseries subplot for summers of the spatial sum of sfc runoff

	@param csvfile directory of csv file 

	"""

	data1 = processcsv(csvfile1)
	data2 = processcsv(csvfile2)

	#plot each summer timeseries on a seperate subplot
	ncol=1
	nrow = 7

	fig, axes = plt.subplots(nrow, ncol, figsize=(50,40), sharex=False, sharey=True, constrained_layout=True)
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
		uv = np.sqrt((summer2['u_avg']**2) + (summer2['v_avg']**2))
		ax2.plot(summer2.date, uv, label='ws', color='black')
		q = ax2.quiver(summer2.date, uv, summer2['u_avg'], summer2['v_avg'], color='black', units='x', width=0.1, scale=4)
		ax2.set_ylabel(ylabel,color="black",fontsize=14)
		ax2.set_ylim(bottom=uv.min()-3, top=uv.max()+4)
		# if i==0:
		# 	plt.colorbar(q, orientation="vertical")
		# else:
		# 	continue

	lines_1, labels_1 = axes[i].get_legend_handles_labels()
	lines_2, labels_2 = ax2.get_legend_handles_labels()

	lines = lines_1 + lines_2
	labels = labels_1 + labels_2

	axes[0].legend(lines, labels, loc=0)

	fig.supxlabel("Date")
	#fig.supylabel("Daily total surface runoff (mm)")
	fig.suptitle(titl + csvfile1.split(".")[0].split("_")[0], fontsize=25)
	#plt.subplots_adjust(hspace=0.1)


	plt.savefig('uv' + 'quiver' + csvfile1.split(".")[0].split("_")[0] + '.png')
	plt.close('all')

