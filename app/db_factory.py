import pymysql as pms

class DBFactory:
    def __init__(self):
        self.conn = pms.connect(host='164.52.209.112', database='bfs_cmdb', port=3306, 
                                user='cmdbuser', passwd='CMDBuser@2019', charset='utf8mb4', 
                                autocommit=True, cursorclass=pms.cursors.DictCursor)
    

    def select_industry_subindustry(self, li_industry):
        industry = None
        sub_industry = None

        select_ind_query = 'select id, name from company_industry where name = %s'
        select_ind_value = (li_industry,)

        select_ind_alt_query = 'select id, name from company_industry where id = %s'
        # select_ind_alt_value = (li_industry,)

        select_sub_ind_query = 'select id, name, industry_id from company_subindustry where name = %s'
        select_sub_ind_value = (li_industry,)

        with self.conn.cursor() as cursor:
            cursor.execute(select_ind_query, select_ind_value)
            industry = cursor.fetchone()
            if not industry:
                cursor.execute(select_sub_ind_query, select_sub_ind_value)
                sub_industry = cursor.fetchone()
                if sub_industry:
                    select_ind_alt_value = (sub_industry.get('industry_id'),)
                    cursor.execute(select_ind_alt_query, select_ind_alt_value)
                    industry = cursor.fetchone()
        
        return industry, sub_industry