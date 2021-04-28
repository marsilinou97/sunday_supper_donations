from genericpath import exists
from django.db.models import query
import xlwt

from input import models
from django.http import HttpResponse
from analytics.vars import QUERY_DATA
from analytics.vars import TABLE_HEADERS_FORMATTED
from analytics.queries import get_model_raw_data_query
import os

def export_tables_to_excel(params):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="test.xls"'
    
    tables_selected = params["tables_selected"]

    filters = params["exact"]

    wb = xlwt.Workbook(encoding='utf-8')

 
    for table_name in tables_selected:
        
        query_info = QUERY_DATA[table_name]
        table_data = get_model_raw_data_query(
            query_info["MODEL"],
            query_info["RAW_DATA_FIELDS"],
            0,
            1000000000000,
            search_keyword="",
            exact=filters
        )

        table_data_ = list(table_data[0])

        ws = wb.add_sheet(table_name)

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        for col_num, column in enumerate(dict(table_data_[0]).keys()):
            ws.write(row_num, col_num, TABLE_HEADERS_FORMATTED[column] , font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()


        for row in table_data[0]:
            row_to_list = list(row.values())
            row_num += 1
            for col_num in range(len(row_to_list)):
                ws.write(row_num, col_num, row_to_list[col_num], font_style)

    if not os.path.exists('./temp_downloads'):
        os.mkdir('./temp_downloads')

    wb.save('./temp_downloads/test.xls')