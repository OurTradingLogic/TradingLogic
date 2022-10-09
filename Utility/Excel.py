import xlsxwriter 

def WriteFromList(list, xlsxFileName):
    with xlsxwriter.Workbook(xlsxFileName) as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(list):
            colnum = 0
            if row_num == 0:
                worksheet.write_row(row_num, 0, data)

            for item in data:
                worksheet.write(row_num+1, colnum, data[item])
                colnum = colnum + 1