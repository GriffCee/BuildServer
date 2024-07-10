from fastapi import FastAPI, File, UploadFile
import mysql.connector
import subprocess
import os
import re
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/files/")
async def post_endpoint(file: UploadFile = File(...)):
    file_check = re.match(r".*\.zip", file.filename)
    if not file_check: 
        return {"Result": "Invalid file format, zips only!"}

    file_location = os.path.join("./", file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    subprocess.run(["./push_file.sh", file.filename])

    return {"Result": "OK"}

@app.get("/")
async def root():
    local_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "build_stats_db",
    )

    cursor = local_db.cursor()
    cursor.execute("SELECT * FROM build_stats")
    result_raw = cursor.fetchall()

    return_vals = []

    for x in result_raw[::-1]:
        val_string = ""
        return_val = []
        return_val.append("Build # " + str(x[0]))
        return_val.append(" Commit tag: " + str(x[1]))
        return_val.append(" Zip file upload date: " + str(x[2]))
        return_val.append(" Build time: " + str(x[3])) if str(x[3]) != "None" else return_val.append(" Project not yet built")
        return_val.append(" Build end time: " + str(x[4])) if str(x[4]) != "None" else return_val.append(" Project build not yet completed")
        return_val.append(" Build status: " + str(x[5])) if str(x[5]) != "None" else return_val.append(" Uploaded")
        return_val.append(" Artifacts directory name: " + x[6]) if str(x[6]) != "None" else return_val.append(" Artifacts not yet committed")
        for x in return_val:
            val_string += x
        return_vals.append(val_string)

    return return_vals

@app.get("/{commit_tag}")
async def get_commit_zip(commit_tag):
    local_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "build_stats_db",
    )

    query = "SELECT artifacts_dir_name FROM build_stats WHERE commit_tag = " + "\"" + commit_tag + "\""
    cursor = local_db.cursor()
    cursor.execute(query)
    dir_name = cursor.fetchone()

    if dir_name == None:
        return {"Result": "Invalid git commit and/or build not completed!"}

    subprocess.run(["./zip_it.sh", dir_name[0]])
    file_path = "./requested_files/" + dir_name[0] + ".zip"
    return FileResponse(file_path)
