import sys, traceback

try:
    from gs_factory import GSFactory
    from db_factory import DBFactory

    gsf = GSFactory(spreadsheet_url='https://docs.google.com/spreadsheets/d/1sdklQqjhOrLHGKLp3iRqsABTDV0993voqUAVbpczRds/edit#gid=0')
    gs_data = gsf.read_data()

    if len(gs_data) > 0:
        header = gs_data[0]
        gs_data = gs_data[1:]
        row_index = 1
        dbf = DBFactory()

        for row in gs_data:
            row_index+=1
            cdb_industry = None
            cdb_sub_industry = None

            li_industry = row[0]
            industry, sub_industry = dbf.select_industry_subindustry(li_industry=li_industry)
            
            if sub_industry:
                cdb_industry = industry.get('name') + '[' + str(industry.get('id')) + ']'
                cdb_sub_industry = sub_industry.get('name') + '[' + str(sub_industry.get('id')) + ']'
            elif industry:
                cdb_industry = industry.get('name') + '[' + str(industry.get('id')) + ']'
            
            gsf.write_data(cdb_industry=cdb_industry, cdb_sub_industry=cdb_sub_industry, row_index=row_index)

except Exception as e:
    type, value, tcb = sys.exc_info()
    print(type)
    print(value)
    print(repr(traceback.format_tb(tcb)))