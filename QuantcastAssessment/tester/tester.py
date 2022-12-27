import math
import string
import csv
from most_active_cookie import LogProcessor
import random
import datetime as dt
import unittest


class CSV_FileCreator:
    def cookie_generator(self, lengthOfList):
        # generate a list of random cookies
        cookies = []
        random_cookie_range = list(string.ascii_letters) + [0, 1, 2, 3, 5, 6, 7, 8, 9]
        for i in range(lengthOfList):
            cookie = "".join([str(random.choice(random_cookie_range)) for _ in range(16)])
            cookies.append(cookie)
        return cookies

    def date_generator(self):
        # generate a random date and time for mock info
        random_year = random.randint(1970, 2022)
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)  # As this is a mock test, we only consider 28 days in a month
        random_hour = random.randint(1, 23)
        random_minute = random.randint(1, 59)
        random_second = random.randint(1, 59)
        random_date_time = dt.datetime(random_year, random_month, random_day, random_hour, \
                                       random_minute, random_second, tzinfo=dt.timezone.utc)
        formatted_random_date_time = dt.datetime.strptime(random_date_time, "%Y-%m-%dT%H:%M:%S%z")
        return formatted_random_date_time

    def generate_count_each_unique_cookies(self, num_unique_cookies, num_cookies, multiple_max_cookies_enable):
        count = {}
        unassigned_cookie = num_cookies
        additional_add = 0
        for i in range(num_unique_cookies):
            if i + 1 < num_unique_cookies:
                additional_add = random.randint(1, math.ceil(num_cookies // num_unique_cookies))
            else:
                if multiple_max_cookies_enable:
                    additional_add = random.randint(1, math.ceil(num_cookies // num_unique_cookies))
                else:
                    additional_add = unassigned_cookie
            count.append(additional_add)
            unassigned_cookie -= additional_add
        return count

    def generate_list_of_indices_each_unique_cookies(self, cookie_frequency, num_dates, multiple_max_cookies_enable):
        list_index_of_date = []
        most_frequency = max(cookie_frequency)
        num_of_most_frequency = cookie_frequency.count(most_frequency)
        if not multiple_max_cookies_enable:
            max_query_day_count = random.randint(1, num_of_most_frequency)
        else:
            max_query_day_count = num_of_most_frequency
        if num_dates - num_of_most_frequency > 0:
            other_query_day_count = random.randint(1, num_dates - num_of_most_frequency)
        else:
            other_query_day_count = 0
        assigning_date_index = random.randint(0, num_dates - 1)
        excluded_list = list(range(num_dates))
        excluded_list.pop(assigning_date_index)
        for count in cookie_frequency:
            if count == most_frequency:
                if max_query_day_count > 0:
                    list_index_of_date.append(assigning_date_index)
                    max_query_day_count -= 1
                else:
                    date_index = random.choice(excluded_list)
                    list_index_of_date.append(date_index)
            else:
                if other_query_day_count > 0:
                    list_index_of_date.append(assigning_date_index)
                    other_query_day_count -= 1
                else:
                    date_index = random.choice(excluded_list)
                    list_index_of_date.append(date_index)

        return list_index_of_date, assigning_date_index


    def generate_test_data(self, exists, multiple_max_cookies_enable, num_unique_cookies, num_cookies, num_dates):
        cookies = self.cookie_generator(num_unique_cookies)
        dates = [self.date_generator() for i in range(num_dates)]
        counts = self.generate_count_each_unique_cookies(num_unique_cookies, num_cookies, multiple_max_cookies_enable)
        most_frequency = max(counts)
        list_index_of_date, assigning_date_index = self.generate_list_of_indices_each_unique_cookies\
            (counts, multiple_max_cookies_enable, num_dates)
        test_data, test_solutions = []
        test_solutions = set()
        selected_date = dates[
            assigning_date_index] if exists else self.date_generator()
        # create the data
        for cookie_num in range(num_unique_cookies):
            rows = []
            cookie, num_rows = cookies[cookie_num], counts[cookie_num]
            date = dates[list_index_of_date[cookie_num]]
            for row_num in range(num_rows):
                rows.append([cookie, date])
            if num_rows == most_frequency and date == selected_date:
                test_solutions.add(cookie)
            test_data.extend(rows)
        self.csv_writer(test_data)
        return selected_date.split("T")[0], test_solutions

    def csv_writer(self, data):
        with open("data.csv", "w") as test_file:
            csv_writer = csv.writer(test_file)
            csv_writer.writerow(["cookie", "timestamp"])
            for row in data:
                csv_writer.writerow(row)


class CookieProcessorTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_generator = CSV_FileCreator()

    def simple_test1(self):
        log_processor = LogProcessor()
        test_date, solutions = self.csv_generator.generate_test_data(True, True, 10, 20, 2)
        log_processor.process_cookies("data.csv")
        computed_cookies = log_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def simple_test2(self):
        log_processor = LogProcessor()
        test_date, solutions = self.csv_generator.generate_test_data(True, True, 15, 45, 3)
        log_processor.process_cookies("data.csv")
        computed_cookies = log_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def simple_test3(self):
        log_processor = LogProcessor()
        test_date, solutions = self.csv_generator.generate_test_data(True, False, 10, 20, 1)
        log_processor.process_cookies("data.csv")
        computed_cookies = log_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def medium_test1(self):
        log_processor = LogProcessor()
        test_date, solutions = self.csv_generator.generate_test_data(True, True, 200, 5000, 10)
        log_processor.process_cookies("data.csv")
        computed_cookies = log_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def medium_test2(self):
        log_processor = LogProcessor()
        test_date, solutions = self.csv_generator.generate_test_data(True, False, 200, 5000, 10)
        log_processor.process_cookies("data.csv")
        computed_cookies = log_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def large_test(self):
        log_processor = LogProcessor()
        test_date, solutions = self.csv_generator.generate_test_data(True, True, 800, 50000, 10)
        log_processor.process_cookies("data.csv")
        computed_cookies = log_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)


    # def test_all_multiple_iter(self, iterations=10):
    #     for iteration in range(iterations):
    #         self.simple_test1()
    #         self.simple_test2()
    #         self.simple_test3()
    #         self.medium_test1()
    #         self.medium_test2()
    #         self.large_test()


if __name__ == '__main__':
    unittest.main()



