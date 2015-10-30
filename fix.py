import os
import MySQLdb
import shutil
import time

def get_info(n, projectName, path):
    count1=0.0
    model = ""
    version_against = ""
    
    directory = projectName
    fileName = directory+"/"+n
    project1 = os.path.splitext(fileName)[0]
    project = project1[len(directory)+1:]
    url = "dump/"+n
    
    for i in project:
        if i is '_':
            a = project.rfind('_')
            version_against = project[a+1:]     #Naive way of getting version_against. In case better method does not work
            break
    
    #open the txt file and scan through, line by line, to find all other info
    searchfile = open(path, "r")
    count = 0
    for line in searchfile:
        if "</span></td><td" in line:
            count+=1
        if "Failed" in line or "Warning" in line:
            count1+=1
        if "The current package revision is:" in line:
            str1 = line.split(',')[0]
            c = str1.index("The current package revision is:")
            str2 = str1[c:]
            b = str2.index("</div>")
            str2 = str2[:b]
            version_against= str2.replace("The current package revision is:", '')
        elif "The release version is" in line:
            str1 = line.split(',')[0]
            c = str1.index("The release version is")
            str2 = str1[c:]
            b = str2.index("</div>")
            str2 = str2[:b]
            version_against= str2.replace("The release version is", '')
        elif "The current platform number is" in line:  
            str1 = line.split(',')[0]
            c = str1.index("The current platform number is")
            str2 = str1[c:]
            b = str2.index("</div>")
            str2 = str2[:b]
            model= str2.replace("The current platform number is", '')
        elif "The current Platform is:" in line:  
            str1 = line.split(',')[0]
            c = str1.index("The current Platform is:")
            str2 = str1[c:]
            b = str2.index("</div>")
            str2 = str2[:b]
            model= str2.replace("The current Platform is:", '')

    a = ""                  
    last = line.split()    
    
    for i in last[1:4]:
        a = a+i
    a = a.replace('class="table_cell">', '')
    a = a.replace('</td><td', '')
    
    "FIXING THE DATE/TIME to fit format (add 0 in 7/07/2015)....."
    for i in range(len(a)):
        if a[i]== '/' and a[i+2]=='/':
            b = a[:i+1] + "0" + a[i+1:]
            break
        else:
            b = a
    
    if b[1]=='/':
        b ="0"+b
    #now make final_time in time stamp format. ex. 1945-03-07 14:24:59
    for i in b:
        if i=="-":
            b = b.replace("-", " ")
    for i in b:
        if i=='/':
            b = b.replace('/', '-')
    sub = b[6:10]+'-'
    b = sub+b[0:5] + b[10:]    
    final_time = b

    searchfile.close()
    count = count-1
    percent = round(((count-count1)/count)*100, 2) #round the mathematical percent to 2 decimal places

    #edit backup file
    f = open("T:\\eng\\TEG\\777_UFTWEBserver\\BackupFiles.txt", 'a')
    f.write(final_time)
    f.write('\t')
    f.write(directory)
    f.write('\t')
    f.write(project)
    f.write('\t')
    f.write(str(count))
    f.write('\t')
    f.write(version_against)
    f.write('\t')
    f.write(str(percent))
    f.write('\t')
    f.write(model)
    f.write('\t')
    f.write(url)
    f.write('\n')
    f.close

    #Access MySQL database and upload the information to the database
    #Enter in the database information here (db = database)
    db=MySQLdb.connect(host="", user="", passwd="", db="")
    c = db.cursor()
    try:
        c.execute("""INSERT INTO test VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (final_time, directory, project, count, version_against, percent, model, url))
        db.commit()
    except:
        db.rollback()
        
    db.close()


def checkForNewFiles():
    array1 = []
    file1 = open("T:\\eng\\TEG\\WEBserver\\allfilenames.txt", 'r')
    for line in file1:
        line = line.strip('\n')
        array1.append(line)
    file1.close()
    
    file1 = open("T:\\eng\\TEG\\WEBserver\\allfilenames.txt", 'a')
    for root, dirs, files in os.walk("T:\\wte\\TEG\\11_Auto\\CWE"):
        path = root.split('/')  
        #NOTE:
        #The folder storing test results must have the word "result" in it, so that the program can skip over 
        #all other folders that do not store results. Without this, the program will take must longer
        if 'result' in os.path.basename(root) or 'Result' in os.path.basename(root) or "results" in os.path.basename(root):
            for file in files:
                if file.endswith('.html'):
                    if file not in array1:
                        file1.write(file)           #Amend allfilesname.txt to include new file name
                        file1.write('\n')

                        path1 = root+"\\"+file
                        a = path1[29:]
                        index1 = a.index("\\")
                        project = a[:index1]        #Get the project name from path
                        print "Updating! New file: "+file+ " ---- " + project
                        get_info(file, project, path1)      #Call get_info to extract all information
                        shutil.copyfile(path1, 'C:\\xampp\\htdocs\\dump\\'+file)    #Copy the file to dump so hyperlink works
        else:
            continue

#Actually execute the script with function calls
#Start an infinite loop that pauses for one hour and then updates everything in about 5 minutes
while True:
    time.sleep(7200)
    checkForNewFiles()

