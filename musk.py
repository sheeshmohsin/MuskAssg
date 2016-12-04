import re
import requests
import dropbox
import datetime

from bs4 import BeautifulSoup
from settings import ACCESS_TOKEN


class Scrapload:

    def __init__(self, tinNumber, ACCESS_TOKEN):
        self.url = "http://www.tinxsys.com/TinxsysInternetWeb/dealerControllerServlet?tinNumber=" + tinNumber + "&searchBy=TIN&backPage=searchByTin_Inter.jsp"
        self.dbx = dropbox.Dropbox(ACCESS_TOKEN)

    def getData(self):
        res = requests.get(self.url)
        return res

    def validateTin(self, res):
        self.soup = BeautifulSoup(res.text)
        l = self.soup(text=re.compile('Dealer Not Found'))
        if len(l) > 0:
            return False
        return True

    def parseData(self):
        l1 = self.soup.findAll("td", {"width" : "30%"})
        l2 = self.soup.findAll("td", {"width" : "70%"})
        string = ""
        for key, value in zip(l1, l2):
            string = string + str(key.getText(strip=True)) + " : " + str(value.getText(strip=True)) + "\n"
        return string

    def getFileFolderName(self):
        folder_name = '/' + str(datetime.datetime.now())
        file_name = folder_name + '/details.txt'
        return folder_name, file_name

    def modifyDropbox(self, folder_name, file_name, string):
        self.dbx.files_create_folder(folder_name)
        self.dbx.files_upload(string, file_name)
        return

if __name__ == '__main__':
    tinNumber = raw_input("Enter TIN Number : ")
    obj = Scrapload(tinNumber, ACCESS_TOKEN)
    res = obj.getData()
    if obj.validateTin(res):
        string = obj.parseData()
        folder_name, file_name = obj.getFileFolderName()
        obj.modifyDropbox(folder_name, file_name, string)
        print("Dealer Found and Details updated in Dropbox")
    else:
        print("Dealer Not Found")



