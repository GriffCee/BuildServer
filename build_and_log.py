import mysql.connector
import subprocess

local_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "build_stats_db",
)

cursor = local_db.cursor(buffered=True)
cursor.execute("SELECT rdi_id, status, artifacts_dir_name FROM build_stats ORDER BY rdi_id DESC")
result_raw = cursor.fetchone()
dirName = result_raw[2]
rdi = result_raw[0]

if result_raw[1] == None:
    subprocess.run(["/home/griffin/repos/build_prep.sh", dirName])
    print("Build prep completed! Updating status.")

    query = "UPDATE build_stats SET build_time = NOW(), status = 'Building' WHERE rdi_id = " + str(rdi)
    cursor.execute(query)
    local_db.commit()
    print("Status updated.")

    output = subprocess.check_output(["/home/griffin/repos/build.sh", dirName])
    print("Build script completed.")
    print("Output: " + str(output))

    if len(str(output)) > 5:
        query = "UPDATE build_stats SET build_end_time = NOW(), status = 'Success' WHERE rdi_id =" + str(rdi)
        print("Build successful!")
        cursor.execute(query)
        local_db.commit()

    else:
        query = query = "UPDATE build_stats SET build_end_time = NOW(), status = 'Failure' WHERE rdi_id =" + str(rdi)
        print("Build unsuccessful...")
        cursor.execute(query)
        local_db.commit()

    subprocess.run(["/home/griffin/repos/artifacts_publish.sh", dirName])
    subprocess.run(["/home/griffin/repos/cleanup.sh", dirName])

else:
    print("No new projects detected")

local_db.close()
