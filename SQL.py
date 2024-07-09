import sqlite3
def create_table_if_not_exists(conn):
    conn = sqlite3.connect("FaceBase.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Peoples(
            id INTEGER PRIMARY KEY,
            Name TEXT

        )
    ''')
def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM Peoples WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        conn.execute("UPDATE Peoples SET Name=? WHERE id=?", (Name,Id,))

    else:
        conn.execute("INSERT INTO Peoples(id,Name) Values(?,?)", (Id, Name))
    conn.commit()
    conn.close()

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cursor=conn.execute("SELECT * FROM Peoples WHERE id=?", (id,))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
def delete_record_by_id( record_id):
    """
    Xóa một bản ghi dựa theo Id trong cơ sở dữ liệu SQLite.

    :param db_path: Đường dẫn tới tệp cơ sở dữ liệu SQLite.
    :param table_name: Tên của bảng chứa bản ghi cần xóa.
    :param record_id: Id của bản ghi cần xóa.
    """
    try:
        conn = sqlite3.connect("FaceBase.db")
        cursor = conn.cursor()
        sql_delete_query = f"DELETE FROM Peoples WHERE Id = ?"
        cursor.execute(sql_delete_query, (record_id,))
        conn.commit()
        print(f"Record with Id {record_id} has been deleted from Peoples'.")

    except sqlite3.Error as error:
        print(f"Error while connecting to sqlite: {error}")

    finally:
        if conn:
            conn.close()

