import sys
import requests
import time
import constants
import utils


def alarm(down_counter, website):
    if down_counter <= constants.alarm_threshold:
        utils.log_disaster(website)
    else:
        utils.log_disaster(website, critical=True)

    if down_counter == constants.email_threshold:
        utils.alarm_admin(website)


def monitor_website(website):
    period = constants.request_period_in_minutes
    down_counter = 0
    while True:
        try:
            response = requests.get(website)
        except requests.exceptions.Timeout:
            response = None
            down_counter += 1
            alarm(down_counter, website)

        if response:
            if response.status_code/100 != 5:
                down_counter += 1
                alarm(down_counter, website)
            else:
                down_counter = 0

        time.sleep(period)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide an address to a website")
        sys.exit()
    elif len(sys.argv) > 2:
        print("Too many arguments!")
        sys.exit()
    monitor_website(sys.argv[1])
