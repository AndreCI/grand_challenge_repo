#import pylab
import numpy as np
import sys
import matplotlib.pyplot as plt
import os

def plot_results(results, path, name):
	sno=results[:,0]
	best=results[:,1]
	avg=results[:,2]
	std=results[:,3]
	plt.plot(sno,best, color='magenta', label='best', lw=3)
	plt.plot(sno,avg, color='blue' ,  label='average' , lw=2 )
	plt.fill_between(sno,avg-std,avg+std, color='blue',alpha=0.3 , label='standard deviation')
	ax=plt.subplot(111)
	ax.set_xlim(1, len(sno))
	plt.xlabel('Generation',fontsize=20)
	plt.ylabel('Fitness', fontsize=20)
	plt.legend(loc='lower right', fontsize=15, fancybox=1)
	plt.title(name)	
	plt.grid()
	plt.show()
	plt.savefig(os.path.join(path,'%s_fitness_evol.png' %name))
	
if __name__ == "__main__":
    #if len(sys.argv) < 2 :
    #    print ("Usage: python plot_results.py BestAvgStd.txt")
    #    exit()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dlist = os.listdir(dir_path)
	for dir in dlist:
		if os.path.isdir(dir):
			current_dir_path = os.path.join(dir_path, dir)
			print(current_dir_path)
			results_file = os.path.join(current_dir_path,'BestAvgStd.txt')
			if os.path.exists(results_file):
				results = np.loadtxt(results_file)
				plot_results(results, current_dir_path, str(dir))
    


    # best_plot, = pylab.plot(results[:,1], '-', color='red')
    # pylab.hold(True)
    # mean_plot, = pylab.plot(results[:,2], '-', color='black')
    # pylab.legend([best_plot, mean_plot],['Best', 'Avg'], loc='best')
    # ax = pylab.gca()
    # ax.set_ylabel('Fitness',size=20)
    # ax.set_xlabel('Generation',size=20)
    #pylab.show()