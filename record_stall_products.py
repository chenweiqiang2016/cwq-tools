from openpyxl import load_workbook

wb = load_workbook("2015_2016_vvic_products_info.xlsx")

print wb.get_sheet_names()