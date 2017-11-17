from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os
import authenticator.authenticator as auth
import argparse as ap
import bell.alert as alert
import selenium
import credentials_handler.cred_handle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

url = "https://markattendance.webapps.snu.edu.in/"

#define a threshold for the attendance.
threshold = 75.0

#define a frequency sequence in Hz for beep and its duration in ms for low attendance.
freqs = [2000, 5000, 1000, 500]
duration = 100

# define a frequency sequence for no attendance initiation.
freq_No_att = [1000, 1000, 1000]

# define a frequency sequence for attendance marked.
freq_marked = [1000,1000,1000,1000]

# define the argument parser.
parser = ap.ArgumentParser()
parser.add_argument('-m', action = "store_true", help = "Pass this to mark the attendance.")
parser.add_argument('-r', action = "store_true", help = "Pass this to get summary of your attendance.")
parser.add_argument('--off', action = "store_true", help = "Pass this to turn off the beep.")
args = parser.parse_args()


def app(sound = True):
    def attendance_record():
        trs = tbody.find_elements_by_tag_name('tr')

        att_less_in = {}

        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            counter = 0
            current_subject_details = []

            for td in tds:
                if counter <= 6:
                    if counter == 0:
                        print "COURSE CODE: "+td.text
                        counter+=1
                    elif counter == 1:
                        print "COURSE NAME: "+td.text
                        print '--'*len(td.text)
                        counter+=1
                    elif counter == 2:
                        print "\t\tENROLLMENT DATE: "+td.text
                        counter+=1
                    elif counter == 3:
                        print "\t\tCLASSES CONDUCTED: "+td.text
                        counter+=1
                    elif counter == 4:
                        print "\t\tCLASSES ATTENDED: "+td.text
                        counter+=1
                    elif counter == 5:
                        print "\t\tOFFICIAL LEAVE: "+td.text
                        counter+=1
                    elif counter == 6:
                        print "\t\tATTENDANCE: "+td.text
                        counter+=1

                    #skip enrollment date
                    if counter != 3:
                        current_subject_details.append(td.text)
                else:
                    counter = 0

            # check if the attendance is low in this subject.
            try:
                if float(current_subject_details[-1]) < threshold:
                    att_less_in.update({current_subject_details[1]:[current_subject_details[-1]
                    , current_subject_details[-3], current_subject_details[-4]]})
            except:
                pass

            print '\n'

        # beeping the alarm if the threshold is not maintained.
        if att_less_in != {}:
            if sound == True:
                for freq in freqs:
                    alert.beep(freq, duration)

            print "\n\n\nYour attendance is below the threshold in the following subjects.\n".upper()
            print '#'*len("Your attendance is below the threshold in the following subjects.\n".upper())
            print '\n\n'
            for subj in att_less_in:
                print subj
                subj_data = att_less_in[subj]

                print '\t\tAttendance:    ', subj_data[0]
                # mathematical formula.
                classes_attended = int(subj_data[1])
                classes_done = int(subj_data[2])
                classes_needed = (classes_done*threshold - 100*classes_attended)*(100 - threshold)**(-1)

                if classes_needed > int(classes_needed):
                    classes_needed = int(classes_needed) + 1

                print '\t\tClasses needed ', int(classes_needed)

    def mark():
        # first see if the attendance portal is open or not.
        try:
            # try to find the submit button.
            submit = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/form/div/button')

            # if found, click it to mark the attendance.
            print "Marking the attendance ... "
            submit.click()

            # beep the frequency.
            if sound == True:
                for frq in freq_marked:
                    alert.beep(frq, duration)

            print "Attendance marked successfully."
        except:
            print "There is no class right now. Or, you can check if the attendance is initiated or not."

            if sound == True:
                for f in freq_No_att:
                    alert.beep(f, duration)

    # define the driver.
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    user, passw = auth.USER()
    # define the chrome driver
    chromium = os.path.dirname(os.path.abspath(sys.argv[0]))
    chromium  = os.path.join(chromium, 'chromedriver.exe')
    driver = webdriver.Chrome(chromium, chrome_options = options)
    # issue a request with url.
    driver.get(url)
    print "Listening to "+url+" ... \n"

    username = driver.find_element_by_xpath('//*[@id="login_user_name"]')
    username.send_keys(user)

    password = driver.find_element_by_xpath('//*[@id="login_password"]')
    password.send_keys(passw)

    print "Logging you in ... "
    # this is the login button
    driver.find_element_by_xpath('//*[@id="tab-1"]/div/div/form/div[3]/div[2]/button').click()

    try:
        #first find the table.
        #table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/table')))
        table = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/table')
    except selenium.common.exceptions.NoSuchElementException:
        try:
            table = driver.find_element_by_xpath('/html/body/div/table')
        except selenium.common.exceptions.NoSuchElementException:
            # the table tag is not found, that probably means that wrong credentials were given.
            print "Wrong credentials given: Login failed!\n"
            print '\nClick Remove Net ID button and sign up again with correct details.'

            return

        #return from the app to the __main__.


    tbody = table.find_element_by_tag_name('tbody')

    # print a welcome message for the student.
    student = driver.find_element_by_xpath('/html/body/nav/div[2]/ul/li[5]/a').text
    print "\nWelcome "+student+"\n"

    # handle the arguments while logged in.
    if args.m and not args.r:
        mark()

    elif args.r and not args.m:
        print "\nLoading... \n"
        attendance_record()

    elif args.r and args.m:
        mark()
        print '\nLoading attendance record ... \n'
        attendance_record()

    # this is the logout button.
    print "\n\nLogging you out ... \n"

    # click the drop down
    driver.find_element_by_xpath('/html/body/nav/div[2]/ul/li[5]/a').click()
    # click logout button
    driver.find_element_by_xpath('/html/body/nav/div[2]/ul/li[5]/ul/li[1]/a').click()
    print "Logged out."


# first make sure that user has either passed -m or -r.
if not args.r and not args.m:
    print "Either mark the attendance or ask for summary.\n\n"
    time.sleep(2)
    print "Found blank request.\n"
    print "Forcing webdriver to stop the initiation...\n"
    time.sleep(3)
    print "Abort"
    os.system('exit')

else:
    if args.off:
        app(False)
    else:
        app()
