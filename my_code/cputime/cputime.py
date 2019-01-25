
import sys
import argparse
from sample_proc import  Sample
from command import Command
def parse(param_list):
	parser = argparse.ArgumentParser()
	parser.add_argument("pname")
	parser.add_argument("interval")
	parser.add_argument("totaltime")
	argv = parser.parse_args()
	s = Sample(argv.pname,int(argv.interval),int(argv.totaltime))
	return s.run()
if __name__ == '__main__':
	if len(sys.argv) > 1:
		print (parse(sys.argv[1:]))
