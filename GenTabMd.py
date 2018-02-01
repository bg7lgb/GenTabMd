# GenTabMd.py
# 用于读取mysql指定数据库中的表，生成Markdown格式的数据字典定义
#

import sys
import argparse
import MySQLdb

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='db user name')
    parser.add_argument('-s', '--server', help='db server')
    parser.add_argument('-p', '--port', type=int, help='db port')
    parser.add_argument('-d', '--database', required=True, help='databaes name')
    parser.add_argument('-t', '--table', help='table name')
    args = parser.parse_args()

    user = args.user
    server = args.server
    port = args.port
    database = args.database
    table = args.table

    if user == "" or user is None:
        user = 'root'

    if server == "" or server is None:
        server = 'localhost'
    
    if port is None:
        port = 3306

    #db_passwd = input('db passwd:')
    db_passwd = '51dingqitest'

    conn = MySQLdb.connect(host=server, user=user, port=port, 
    passwd=db_passwd,db='information_schema',charset='utf8')

    cu = conn.cursor()

    title = '|字段|类型|空|默认|注释|'
    justify = '|:---|:---|:-:|:--:|:---|'
    if table != "" or table is not None:
        sql_stmt = """select column_name,data_type,is_nullable,column_default,\
        character_maximum_length,numeric_precision,numeric_scale,column_comment \
        from columns where table_schema=%s and table_name=%s"""
        cu.execute(sql_stmt, (database,table,))
        rows = cu.fetchall()

        # 拼接输出结果的markdown表格内容
        if len(rows) > 0:
            print('###'+table)
            print(title)
            print(justify)

        for i in range(len(rows)):
            col = '|'
            col=col+rows[i][0]
            if rows[i][1] in('int','smallint'):
                col=col + '|'+rows[i][1]+'(' +str(rows[i][5])+')|'
            elif rows[i][1] == 'varchar' or rows[i][1] == 'char' :
                col=col + '|'+rows[i][1]+'(' +str(rows[i][4])+')|'
            elif rows[i][1] in('date','datetime','timestamp'):
                col=col + '|'+rows[i][1]+'|'
            elif rows[i][1] in('decimal'):
                col=col + '|'+rows[i][1]+'(' +str(rows[i][5])+','+str(rows[i][6])+')|'
            
            if rows[i][2] == 'YES':
                col = col + u'是|'
            else:
                col = col + u'否|'
            
            if rows[i][3] is None or rows[i][3] == "":
                col = col + ' |'
            else:
                col = col + rows[i][3]
            
            col =col + rows[i][7]+'|'

            print(col)

    cu.close()
    conn.close()


if __name__ == '__main__':
    main()