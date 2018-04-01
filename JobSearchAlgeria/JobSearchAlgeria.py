from bs4 import BeautifulSoup
from urllib2 import *
import xlsxwriter
### This code retrieve job offers from the following sites:
    # Emploitic.com
    # EmploiPartner.com
    # Emploialgerie.com

### This is a header to add to a request
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}

### Link for offers list
emploitic_info="https://www.emploitic.com/offres-d-emploi/fonction/365-informatique-systemes-d-information-internet"
emploitic_telecom = "https://www.emploitic.com/offres-d-emploi/fonction/366-telecommunication-reseaux"
EmploiPartnerurl = "https://www.emploipartner.com/fr/offre-emploi?function[24]=on&show=20"

### Defind the xlsx file and its sheets
ResultSheet = xlsxwriter.Workbook("JobSearch.xlsx")
EmploitiSheetInf = ResultSheet.add_worksheet("EmploiticInfo")
EmploitiSheetTel = ResultSheet.add_worksheet("EmploiticTelecom")
EmploiParSheet = ResultSheet.add_worksheet("EmploiPartner")

### Adjust format
HeadFormat = ResultSheet.add_format( {'bold': True})
HeadFormat.set_bg_color("yellow")
HeadFormat.set_align('center')
HeadFormat.set_align('vcenter')

Format = ResultSheet.add_format()
Format.set_align('center')
Format.set_align('vcenter')

EmploitiSheetInf.set_column('A:A', 50)
EmploitiSheetInf.set_column('B:C', 40)
EmploitiSheetTel.set_column('A:A', 50)
EmploitiSheetTel.set_column('B:C', 40)
EmploiParSheet.set_column('A:A', 50)
EmploiParSheet.set_column('B:D', 40)

EmploitiSheetInf.write(0,0,"Job",HeadFormat)
EmploitiSheetInf.write(0,1,"Company",HeadFormat)
EmploitiSheetInf.write(0,2,"Location and Date",HeadFormat)

EmploitiSheetTel.write(0,0,"Job",HeadFormat)
EmploitiSheetTel.write(0,1,"Company",HeadFormat)
EmploitiSheetTel.write(0,2,"Location and Date",HeadFormat)

EmploiParSheet.write(0,0,"Job",HeadFormat)
EmploiParSheet.write(0,1,"Company",HeadFormat)
EmploiParSheet.write(0,2,"Date",HeadFormat)
EmploiParSheet.write(0,3,"Location",HeadFormat)

### Get info offers from emploitic
emploitic_info_req = Request(emploitic_info,None,hdr)
emploitic_info_page = urlopen(emploitic_info_req)
emploitic_info_parse = BeautifulSoup(emploitic_info_page, "html.parser" )

divs = emploitic_info_parse.find_all("div",{"class","row-fluid job-details pointer"})

row = 1
for div in divs:
    offer = []
    for line in div.text.splitlines():
        if (line != ''):
            offer.append(line)
    EmploitiSheetInf.write(row, 0, offer[0],Format)
    EmploitiSheetInf.write(row, 1, offer[1],Format)
    EmploitiSheetInf.write(row, 2, offer[2],Format)
    row += 1

### Get Telecom offers from emploitic
emploitic_tele_req = Request(emploitic_telecom,None,hdr)
emploitic_tele_page = urlopen(emploitic_tele_req)
emploitic_tele_parse = BeautifulSoup(emploitic_tele_page, "html.parser" )

divs = emploitic_tele_parse.find_all("div",{"class","row-fluid job-details pointer"})

row=1
row = 1
for div in divs:
    offer = []
    for line in div.text.splitlines():
        if (line != ''):
            offer.append(line)
    EmploitiSheetTel.write(row, 0, offer[0],Format)
    EmploitiSheetTel.write(row, 1, offer[1],Format)
    EmploitiSheetTel.write(row, 2, offer[2],Format)
    row += 1


### Emploi Partner offers
EmploiPartner_req = Request(EmploiPartnerurl,None,hdr)
EmploiPartner_page = urlopen(EmploiPartner_req)
EmploiPartner_parse = BeautifulSoup(EmploiPartner_page, "html.parser" )

divs = EmploiPartner_parse.find_all("div", {"class": "overflow-h margin-bottom-5"})

row = 1
for div in divs:
    offer = []
    for line in div.text.splitlines():
        if (line != ''):
            offer.append(line)
    EmploiParSheet.write(row,0,offer[0],Format)
    EmploiParSheet.write(row,1, offer[5].split("recrute")[0],Format)
    EmploiParSheet.write(row,2, offer[2],Format)
    EmploiParSheet.write(row,3, offer[3] + offer[4],Format)
    row += 1



ResultSheet.close()


print ("Results are stored in the xlsx file")
