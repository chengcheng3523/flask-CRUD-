import mysql.connector

# 接下來的程式碼


# 設定 MySQL 連接參數
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "pydb"
}

try:
    # 連接 MySQL 伺服器
    connection = mysql.connector.connect(**db_config)

    # 創建游標
    cursor = connection.cursor()

    # 執行 SQL 查詢
    query = "SELECT * FROM your_table_name"
    cursor.execute(query)

    # 獲取查詢結果
    result = cursor.fetchall()

    # 顯示結果
    for row in result:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # 無論如何都關閉游標和連接
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
