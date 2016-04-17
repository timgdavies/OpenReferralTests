import requests
import csv
import os
import zipfile

api_key = "keytjhOk41ho5Dxdv"
base = "appF2ra39YCuPIlg5"

headers = {'Authorization': 'Bearer %s' % api_key}

def fetch_table(table_name,fieldnames = None):
    r = requests.get("https://api.airtable.com/v0/"+base+"/" + table_name, headers=headers)
    data = r.json()
    fieldnames = {}
    output = []
    for row in data['records']:
        output.append(row['fields'])

        for key in row['fields'].keys():
            fieldnames[key] = True

    print fieldnames
    print output
    with open("output/"+table_name+".csv", 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Write product rows
        for row in output:
            writer.writerow(row)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


fetch_table("organizations")
fetch_table("locations")
fetch_table("physical_address")
fetch_table("postal_address")
fetch_table("contacts")
fetch_table("phones")
fetch_table("services")
fetch_table("programs")
fetch_table("regular_schedules")
fetch_table("holiday_schedules")

zipf = zipfile.ZipFile('hsds_package.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('output/', zipf)
zipf.close()

