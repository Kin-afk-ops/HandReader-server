from flask import Blueprint, jsonify
import psycopg2
import os

db_routes = Blueprint("db_routes", __name__)

@db_routes.route("/db/tables", methods=["GET"])
def list_tables():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT", 5432)
        )
        cur = conn.cursor()

        # Lấy danh sách bảng từ schema "public"
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cur.fetchall()

        result = []

        for (table_name,) in tables:
            cur.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s;
            """, (table_name,))
            columns = cur.fetchall()
            result.append({
                "table": table_name,
                "columns": [{"name": col[0], "type": col[1]} for col in columns]
            })

        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
