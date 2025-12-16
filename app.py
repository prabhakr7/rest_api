from flask import Flask, jsonify
import oracledb
import os

app = Flask(__name__)

# cs = '''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.ap-mumbai-1.oraclecloud.com))(connect_data=(service_name=g2528f9311cb5d2_pyapex_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
# # Create connection once (Railway container reuse friendly)
conn=oracledb.connect(
     config_dir="/app/my_wallet",
     user="ADMIN",
     password=os.getenv("ORACLE_PASSWORD"),
     dsn="pyapex_high",
     wallet_location="/app/my_wallet",
     wallet_password=os.getenv("WALLET_PASSWORD"))

@app.route("/")
def health():
    return "Flask + Oracle ADB (TLS) is running ✅"

# @app.route("/db-check")
# def db_check():
#     with conn.cursor() as cur:
#         cur.execute("select sysdate from dual")
#         row = cur.fetchone()
#     return jsonify({"sysdate": str(row[0])})

@app.route("/db-check")
def db_check():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM EBA_DEMO_CARD_EMP")
        columns = [col[0] for col in cur.description]  # get column names
        rows = cur.fetchall()  # fetch all rows

        # Convert rows to list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

# from flask import Flask, jsonify, request
# import oracledb
# import os
# from wallet_setup import setup_wallet

# app = Flask(__name__)

# @app.route('/api/v1/details', methods=['GET'])
# def get_effort_summary():

#     # Example fixed response (normally fetched from DB or logic)
#     response = {
#         "period": {
#             "start_date": "2025-01-01",
#             "end_date": "2025-01-31"
#         },
#         "employees": [
#             {"id": 101, "total_effort": 176},
#             {"id": 102, "total_effort": 160},
#             {"id": 103, "total_effort": 184}
#         ],
#         "overall_effort": 520
#     }

#     return jsonify(response), 200

# @app.route('/process-user/<int:user_id>', methods=['POST'])
# def process_user(user_id):

#     try:
#         conn = oracledb.connect(
#             user="ADMIN",
#             password="your_password",
#             dsn="your_adb_medium"
#         )
#         cur = conn.cursor()

#         # Fetch user
#         cur.execute("""
#             SELECT USER_ID, NAME, EMAIL, STATUS 
#             FROM USERS
#             WHERE USER_ID = :id
#         """, [user_id])

#         row = cur.fetchone()

#         if not row:
#             return jsonify({"error": "User not found"}), 404

#         # Modify data
#         updated_status = "ACTIVE"
#         updated_name = row[1].upper()

#         # Update DB
#         cur.execute("""
#             UPDATE USERS
#             SET STATUS = :status, NAME = :name
#             WHERE USER_ID = :id
#         """, [updated_status, updated_name, user_id])

#         conn.commit()

#         return jsonify({
#             "message": "User processed successfully",
#             "updated_data": {
#                 "user_id": user_id,
#                 "name": updated_name,
#                 "email": row[2],
#                 "status": updated_status
#             }
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         try:
#             cur.close()
#             conn.close()
#         except:
#             pass


# @app.route('/')
# def home():
#     return "Hello from this OCI VM!"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000, debug=True)


# # print('Jai SiyaRam')
