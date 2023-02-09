import gspread
import Utility.Constant as cons
import Helper.JsonReader as json
import gspread.exceptions as gsheetexception

class GSheet(object):
    Sheet = None
    def __init__(self, filename):
        secret_key_path = json.getnodedata('Google_Service_Account_Credentials')
        #Connect google service account
        self._sc = gspread.service_account(filename = secret_key_path)
        try:
            self._file = self._sc.open(filename)
        except gsheetexception.SpreadsheetNotFound as e:
            raise Exception('Error occurred. Not able to access input file. Please check whether OurTradingLogic gsheet is exist in google drive and google service account setup.')

    def __del__(self):
        self.Sheet = None
        self._file = None
        self._sc = None

    def sheet(self, sheetname):
        #Get specific sheet name  
        try:
            return self._file.worksheet(sheetname)
        except gsheetexception.WorksheetNotFound as e:
            wks = self._file.add_worksheet(sheetname, 1000, 26)
            return wks
            #raise Exception('Error occurred. Not able to access input work sheet. Please check whether OurTradingLogic gsheet have created with sheet and configure sheet name in data.json')

