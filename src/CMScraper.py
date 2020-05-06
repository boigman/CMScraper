'''
Created on Mar 27, 2020
Updated May 5, 2020

@author: 08925
'''

import os,sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as bs 




#===============================================================================
# class ChromeDriverWindows():
# 
#     def test(self):
#         # Instantiate Chrome Browser Command
#         driver = webdriver.Chrome(executable_path="C:\\Users\\08925\\Downloads\\chromedriver.exe")
#         # Open the provided URL
#         driver.get("http://www.letskodeit.com")
# 
# cc = ChromeDriverWindows()
# cc.test()
#===============================================================================

# Instantiate Chrome Browser Command
#driver = webdriver.Chrome(executable_path="C:\\Users\\08925\\Downloads\\chromedriver.exe")
#driver = webdriver.Chrome()
#chrome_options = webdriver.ChromeOptions(); 
#chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
#driver = webdriver.Chrome(options=chrome_options);
#driver = webdriver.Chrome()  
# Open the provided URL

class FindByLinkText():

    def test(self):
        baseUrl = "https://lacledegas.sysaidit.com/SREdit.jsp?id=$CMNUM$&fromId=ChangesList".replace("$CMNUM$",cm_num)
        driver = webdriver.Ie()
        driver.get(baseUrl)
        web_iframe = driver.find_element_by_id("contentFrame");
        driver.switch_to.frame(web_iframe)
        freq = 0.5 # seconds
        timeout = 6
        try:
            myFrame = WebDriverWait(driver, timeout, freq, ignored_exceptions=[NoSuchElementException\
                ]).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sr_title']")))
        except TimeoutException:
            x = 1
        
        title = driver.find_element_by_xpath("//div[@class='sr_title']").get_attribute("title").replace(" Normal Change -","")
        #=======================================================================
        # loginName = driver.find_element_by_xpath("//input[@name='userName']")
        # loginName.send_keys('08925')
        # passwd = driver.find_element_by_xpath("//input[@name='password']")
        # passwd.send_keys('xxxxxxxxxx')
        # clickBtn = driver.find_element_by_xpath("//input[@id='loginBtn']")
        # clickBtn.click()
        # driver.implicitly_wait(20)
        #=======================================================================
        for approv_type in ['Initial Approval','CAB Approval']:
            body_line = ("Hello all. I have a Change (#$CMNUM$ - $TITLE$) in $APPROV_TYPE$ status, awaiting your approval. Could you please review at your next opportunity?"+\
            "\nLet me know if you have any questions."+\
            "\n\n$URL$").replace("$CMNUM$",cm_num).replace("$TITLE$",title).replace("$URL$",baseUrl).replace('$APPROV_TYPE$',approv_type)
            my_xpath = "//span[contains(., '$APPROV_TYPE$')]".replace('$APPROV_TYPE$',approv_type)
            try:
                cabApprovalBtn = driver.find_element_by_xpath(my_xpath)
            except:
                print(approv_type + " Tab not found.")
                continue
            parent = cabApprovalBtn.find_element_by_xpath("./..")
            my_xpath += "//parent::td/img"
            img = driver.find_element_by_xpath(my_xpath)
            img_type =img.get_attribute("src")
            if(img_type.find("Disabled")>=0):
                print("For CM #$CMNUM$, $APPROV_TYPE$ link is disabled".replace('$APPROV_TYPE$',approv_type).replace("$CMNUM$",cm_num))
            elif(img_type.find("Completed")>=0):
                print("For CM #$CMNUM$, $APPROV_TYPE$ process is completed".replace('$APPROV_TYPE$',approv_type).replace("$CMNUM$",cm_num))
            else:
                onclick = parent.get_attribute("onclick")
                driver.execute_script(onclick);
                freq = 0.5 # seconds
                timeout = 6
                try:
                    myFrame = WebDriverWait(driver, timeout, freq, ignored_exceptions=[NoSuchElementException\
                        ]).until(EC.presence_of_element_located((By.XPATH, "//input[@type='hidden' and @name='selectedTabCaption' and @value='$APPROV_TYPE$']".replace('$APPROV_TYPE$',approv_type))))
                except TimeoutException:
                    x = 1
                tabStrip = driver.find_element_by_xpath("//td[@class='TabStrip wf_tabs'][1]")
                ele_source = tabStrip.get_attribute("outerHTML")
                try:
                    yesno = driver.find_element_by_xpath("//select[contains(@name,'yesnoappr')]/option[@selected='']").text
                except:
                    yesno = "Not Reviewed"
                approver_name = driver.find_element_by_xpath("//label[@title='Individual assignment']/parent::*//span[@class='defaultText']").text
                approvers = []
                yesno_list = []
                appr_names = []
                yesno_list.append(yesno)
                appr_names.append(approver_name)
                bs_content = bs(ele_source, "lxml")
                for span in bs_content.find_all("span"):
                    approvers.append(span.text.replace("\n",""))
                for ii in range(1, len(approvers)):
                    approver = approvers[ii]
                    xpath = "//span[contains(text(),'"+approver+"')]"
                    elementByLinkText = driver.find_element_by_xpath(xpath)
                    parent = elementByLinkText.find_element_by_xpath("./..")
                    onclick = parent.get_attribute("onclick")
                    wait_path = "//input[@type='hidden' and @name='selectedSubTabCaption' and @value='$APPROVER$']".replace('$APPROVER$',approver)
                    driver.execute_script(onclick);
                    try:
                        myFrame = WebDriverWait(driver, timeout, freq, ignored_exceptions=[NoSuchElementException\
                            ]).until(EC.presence_of_element_located((By.XPATH, wait_path)))
                    except TimeoutException:
                        x = 1
                    try:
                        yesno = driver.find_element_by_xpath("//select[contains(@name,'yesnoappr')]/option[@selected='']").text
                    except:
                        yesno = "Not Reviewed"
                    approver_name = driver.find_element_by_xpath("//label[@title='Individual assignment']/parent::*//span[@class='defaultText']").text
                    yesno_list.append(yesno)
                    appr_names.append(approver_name)
                to_line = "TO: "
                subj_line = "SUBJ: "
                print("APPROVALS\n---------")
                for ii in range(0, len(approvers)):
                    print("Title: "+approvers[ii]+", Name: "+appr_names[ii]+", Approval Status:"+yesno_list[ii])
                    if(yesno_list[ii] =="Not Reviewed"):
                        to_line += appr_names[ii][12:]+"; "
                subj_line += "Change #$CMNUM$ in $APPROV_TYPE$ status awaiting your review".replace("$CMNUM$",cm_num).replace('$APPROV_TYPE$',approv_type)
                print("\n"+to_line)
                print("CC: Ali, Mir")
                print(subj_line)
                print("\n"+body_line+"\n")
                break
        driver.quit()
            
cm_num = sys.argv[1]
ff = FindByLinkText()
ff.test()
print("Finished")

