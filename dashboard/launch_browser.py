#!/usr/bin/env python3

import os
import datetime
import time
import psutil


FILENAME_LOG = "log.txt"
FILEPATH_LOG = "./" + FILENAME_LOG
MAXFILESIZE_LOG = 100*1024*1024 #=256MB
BROWSER_PROCESS_NAME = "chromium"
SCHEDULE_DOW = (1, 2, 3, 4, 5) # 1 = Monday
SCHEDULE_HOURS = (7, 8) # 1-24

def writelog(text, write_to_file=True):
	logline = "[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S%Z") + "]: " + text
	print(logline)
	if write_to_file:

		# Check logfile existance and filesize
		try:
			filesize = os.path.getsize(FILEPATH_LOG)
		except Exception:
			filesize = 0
		
		# Delete logfile if too large
		if filesize > MAXFILESIZE_LOG:
			os.delete(FILEPATH_LOG)
		
		# Write to file
		with open(FILEPATH_LOG, "a+") as logfile:
			logfile.write("\n" + logline)


def main():
	def is_dashboard_open():
		for proc in psutil.process_iter():
			if "chromium" in proc.name():
				return True
		return False


	def launch_dashboard():
		cmd = '/usr/bin/chromium-browser --start-fullscreen --kiosk "./index.html"'
		os.system(cmd)


	def kill_dashboard():
		for proc in psutil.process_iter():
			if BROWSER_PROCESS_NAME in proc.name():
				proc.kill()
				return True
		return False
			


	while True:
		now = datetime.datetime.now()
		dow = now.isoweekday()
		keep_open = False

		if dow in SCHEDULE_DOW:
			if now.hour in SCHEDULE_HOURS:
				if not is_dashboard_open():
					writelog("Launching dashboard")
					launch_dashboard()
					keep_open = True
					writelog("Launched dashboard")
		
		if not keep_open:
			kill_dashboard()				

		time.sleep(2)



if __name__ == "__main__":
	writelog("program start")
	main()
	writelog("program end")
