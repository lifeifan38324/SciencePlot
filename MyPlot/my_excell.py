import xlsxwriter
import MyPlot.Line

def write_files_to_excel(path):
    lst = MyPlot.Line()
    file_list = lst.find_all_file(path, r"[^(index)].*.txt")
    if len(file_list) > 0:
        workbook = xlsxwriter.Workbook(path + '\\index.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "absolute_path")
        worksheet.write(0, 1, "date")
        worksheet.write(0, 2, "device")
        worksheet.write(0, 3, "curve_type")
        worksheet.write(0, 4, "label")
        worksheet.write(0, 5, "test_count")
        for i in range(len(file_list)):
            worksheet.write(i + 1, 0, file_list[i].absolute_path)
            worksheet.write_url(i + 1, 0, file_list[i].absolute_path)
            worksheet.write(i + 1, 1, file_list[i].date)
            worksheet.write(i + 1, 2, file_list[i].device)
            worksheet.write(i + 1, 3, file_list[i].curve_type)
            worksheet.write(i + 1, 4, file_list[i].label)
            worksheet.write(i + 1, 5, file_list[i].test_count)
        workbook.close()
        print("文件信息已经写入Excel中")
    else:
        print("没有读取到文件")

if __name__ == "__main__":
    filepath = r"C:\Users\LFF\Desktop\220925"
    lst = MyPlot.Line()