import gspread

#Connect google service account
gs = gspread.service_account(filename = "/content/drive/MyDrive/Personal/learntech-368417-7990b46d1304.json")

#Open existing google sheet with name 'Data1'
sh = gs.open("Data1")

#Get specific sheet name
wks = sh.worksheet("Sheet1")

#wks.update('A1', 'Welcome to all')

#print(wks.get('A1'))

wks.delete_rows(1)

print('Welcome')
