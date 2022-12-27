import sys as system
import datetime as dt
import heapq as hq
import csv
from typing import List


class LogProcessor:
    def __init__(self):
        # all_date_logDict save all date and logs as a dictionary
        # For each item, key is the date, value is a list that contain all cookies for that specific date
        self.all_date_logDict = {}

    def read_file(self, fileName) -> None:
        try:
            with open(fileName) as logFile:
                logs = csv.reader(logFile)  # save entire csv file as an object called logs
                for log in logs:
                    self.save_log_in_dict(log)

        except IOError:
            raise ValueError("File not Found")
        finally:
            logFile.close()  # close the file in finally block to avoid leaving file in an opened status

    def save_log_in_dict(self, original_log) -> None:
        real_log, date_time = original_log[0], original_log[1]
        date = date_time.split("T")[0]  # remove the part after T so that only date part get stored as key
        if date not in self.all_date_logDict:
            self.all_date_logDict[date] = [real_log]  # save the date and cookie into the dictionary for first time
        else:
            self.all_date_logDict[date].append(real_log)  # add the cookie in the corresponding list for the date

    def top_k_frequent_logs(self, date: str) -> List[str]:
        logs = []
        if date not in self.all_date_logDict:
            return logs  # if the date that searched by user does not exist in dictionary, return a null list
        else:
            logs = self.all_date_logDict[date]
        counters = {}  # counter is a local hashmap used to count the frequency of a cookie in a day
        for cookie in logs:
            if cookie in counters:
                counters[cookie] -= 1  # use negative value as counter since we want to construct a Max-heap later
            else:
                counters[cookie] = -1

        heap = []  # use heap structure to find most active cookies
        for count in counters:
            hq.heappush(heap, (counters[count], count))


        result = set()  # a list to show top frequent cookies, saveing as list make it easy for further extension
        highestFrequency, mostActiveCookie = hq.heappop(heap)  #heappop the most active cookie
        for (cookie, frequency) in counters.items():
            if frequency == highestFrequency:
                result.add(cookie)
        return result


if __name__ == '__main__':
    if len(system.argv) != 4:
        raise Exception("Your input command does not match requirement, \
        expected format: 'most_active_cookie.py filename.csv -d YYYY-MM-DD'.")
    fileName = system.argv[1]  # take the filename from the command
    _d = system.argv[2]  # take the "-d" from command
    searchDate = system.argv[3]  # take the searching date from command

    if not fileName:
        raise ValueError("Unable to find the file")
    if not dt.datetime.strptime(searchDate, '%Y-%m-%d'):
        raise ValueError("Invalid date format, please enter your date format as YYYY-MM-DD")

    log_processor = LogProcessor()  # create a log_processor object to start everything
    log_processor.read_file(fileName)  # call read_file function to write cookies into the date-cookie dictonary

    topKFrequentlyLogs = log_processor.top_k_frequent_logs(searchDate)
    if topKFrequentlyLogs is None:
        print("We do not have any cookies for ", searchDate, " , try a different date")  # No result from this date
    else:
        print("Most active cookie(s):")
        for item in topKFrequentlyLogs:
            print(item)
