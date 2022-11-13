import gspread
import Utility.Constant as cons
import Helper.JsonReader as json

class GSheet(object):
    Sheet = None
    def __init__(self, filename):
        secret_key_path = json.getnodedata('Google_Service_Account_Credentials')
        #Connect google service account
        self._sc = gspread.service_account(filename = secret_key_path)
        self._file = self._sc.open(filename)

    def __del__(self):
        self.Sheet = None
        self._file = None
        self._sc = None

    def sheet(self, sheetname):
        #Get specific sheet name
        return self._file.worksheet(sheetname)
