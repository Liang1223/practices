import requests, json, os, time

# 登入url
url = 'https://apigw.tibame.com/tibame-biz-emp/v1/login'

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"

user_email_id = input('帳號(Email):')

passw = input('密碼:')



# 登入資料
data = {'email': user_email_id,
        'password': passw,
        'rememberMe': 'true'}

# 登入headers
headers = {
    "origin": "https://108thmr.tibame.com",
    'referer': 'https://108thmr.tibame.com/login',
    "user-agent": ua,
    "content-type": "application/json"
}

# 建立連線
rs = requests.session()

# 登入
re = rs.post(url, data=json.dumps(data), headers=headers)

print(f"登入狀況: {re}")

if re.status_code == requests.codes.ok:

    re_json = json.loads(re.text)

    # 畫面1
    print(f"登入--{re_json['data']['bizInfo'][0]['bizCompanyName']}-----")
    print(f"名稱--{re_json['data']['userName']}-----")

    re_companyname = re_json['data']['bizInfo'][0]['companyUid']
    re_token = re_json['data']['token']
    re_bizDomain = re_json['data']['bizInfo'][0]['bizDomain']

    # 選取課程url
    url = 'https://api-c2c.tibame.com/v1/x2b/company/36/user/myTraining'

    # 課程headers
    headers = {
        "origin": "https://"+re_bizDomain+".tibame.com",
        "referer": "https://"+re_bizDomain+".tibame.com/learningcenter/course",
        "x-access-token": re_token,
        "user-agent": ua
    }

    # 選課
    re = rs.get(url, headers=headers)

    print(f"登入課程狀況: {re}")

    re_json = json.loads(re.text)

    # 建立課程dict
    course_dict = {"course_name":[]}


    for i in re_json['data'][0]['courseData']:
        course_dict['course_name'].append([i['courseUid'],i['courseName'],i['missionCount']])

    print('選擇下載課程[數字編號]')

    while_check = True
    while while_check:
        for i_int,i in enumerate(course_dict['course_name']):
            print(f'{i_int}.{i[1]}')
        print('99.全選')
        print('999.退出')
        select_id = int(input('選擇:'))

        if select_id != 99 and select_id != 999:
            try:
                course_do = str(course_dict['course_name'][select_id][0])
                print(f"正在下載----{course_dict['course_name'][select_id][1]}")
                course_dir_name = course_dict['course_name'][select_id][1]
                check = 0
            except:
                check = 1
                print('輸入錯誤!')

            if check == 0:
                url = "https://api.tibame.com/learningCenter/user/stagelist/"+course_do+"?isBiz=1&companyUid="+re_bizDomain

                headers = {
                    "x-access-token": re_token,
                    "user-agent": ua
                }

                re = rs.get(url, headers=headers)
                print(f"課程選擇狀況: {re}")

                # 建立資料夾
                if os.path.isdir(course_dir_name):
                    pass
                else:
                    os.mkdir(course_dir_name)
                

                re_json = json.loads(re.text)  

                for i in re_json['data']['stageList']:

                    i['stageName'] = i['stageName'].replace("\t","")

                    # 建立資料夾
                    if os.path.isdir(course_dir_name+"\\"+i['stageName']):
                        pass
                    else:
                        os.mkdir(course_dir_name+"\\"+i['stageName'])    

                    for i2 in i['missions']:
                        url = i2['filePath']
                        
                        if url != None:

                            i2['missionName'] = i2['missionName'].replace("\t","")
                            i2['missionName'] = i2['missionName'].replace(":","")
                            i2['missionName'] = i2['missionName'].replace(" ","")
                            i2['missionName'] = i2['missionName'].replace("?","")

                            if os.path.isfile(course_dir_name+"\\"+i['stageName']+"\\"+i2['missionName']+'.mp4'):
                                print(f"{course_dir_name}----已存在:{i2['missionName']}----------")
                            else:
                                headers = {'referer': "https://108thmr.tibame.com/course/"+course_do+"/mission/"+str(i2['muid'])}
                                re = rs.get(url, headers = headers)

                                with open(course_dir_name+"\\"+i['stageName']+"\\"+i2['missionName']+'.mp4', 'wb') as f:
                                    f.write(re.content)
                                    print(f"{course_dir_name}------下載完成:{i2['missionName']}----------")
                                time.sleep(10)
                        

        elif select_id == 99:
#改課程編號
            cu_list = [5,8,9,13,14]
            for i in cu_list:
                try:
                    course_do = str(course_dict['course_name'][i][0])
                    print(f"正在下載----{course_dict['course_name'][i][1]}")
                    course_dir_name = course_dict['course_name'][i][1]
                    check = 0
                except:
                    check = 1
                    print('輸入錯誤!')

                if check == 0:
                    url = "https://api.tibame.com/learningCenter/user/stagelist/"+course_do+"?isBiz=1&companyUid="+re_bizDomain

                    headers = {
                        "x-access-token": re_token,
                        "user-agent": ua
                    }

                    re = rs.get(url, headers=headers)
                    print(f"課程選擇狀況: {re}")

                    # 建立資料夾
                    if os.path.isdir(course_dir_name):
                        pass
                    else:
                        os.mkdir(course_dir_name)
                    

                    re_json = json.loads(re.text)  
                    print(re_json)
                    for i in re_json['data']['stageList']:

                        i['stageName'] = i['stageName'].replace("\t","")                        

                        # 建立資料夾
                        if os.path.isdir(course_dir_name+"\\"+i['stageName']):
                            pass
                        else:
                            os.mkdir(course_dir_name+"\\"+i['stageName'])    

                        for i2 in i['missions']:
                            url = i2['filePath']
                            

                            if url != None:

                                i2['missionName'] = i2['missionName'].replace("\t","")
                                i2['missionName'] = i2['missionName'].replace(":","")
                                i2['missionName'] = i2['missionName'].replace(" ","")
                                i2['missionName'] = i2['missionName'].replace("?","")

                                if os.path.isfile(course_dir_name+"\\"+i['stageName']+"\\"+i2['missionName']+'.mp4'):
                                    print(f"{course_dir_name}----已存在:{i2['missionName']}----------")
                                else:
                                    headers = {'referer': "https://108thmr.tibame.com/course/"+course_do+"/mission/"+str(i2['muid'])}
                                    re = rs.get(url, headers = headers)

                                    with open(course_dir_name+"\\"+i['stageName']+"\\"+i2['missionName']+'.mp4', 'wb') as f:
                                        f.write(re.content)
                                        print(f"{course_dir_name}------下載完成:{i2['missionName']}----------")
                                    time.sleep(10)  

        elif select_id == 999:
            while_check = False                           

                    
else:
    print('登入失敗!')
