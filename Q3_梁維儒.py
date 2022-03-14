import pymysql
import os
import prettytable


e = input('請輸入root密碼：')
f = input('請輸入port：')

if f == "":
    f = "3306"
link = pymysql.connect(host='localhost', user='root', passwd=e, db='lesson20201007', charset='utf8', port=int(f))
os.system('cls')

while 1:
    choose = input("0 關閉程式\n1 新增資料\n2 修改資料\n3 刪除資料\n4 顯示資料\n5 新增會員電話\n6 刪除會員電話\n模式:")

    os.system('cls')

    p2 = prettytable.PrettyTable(["ID", "Name", "Birthday", "Address", '電話'], encoding="utf8")
    cur2 = link.cursor()
    cur2.execute(
        "SELECT `m`.*,`t`.`電話` FROM `member` AS `m` LEFT JOIN `tel` AS `t` ON `m`.`會員編號` = `t`.`會員編號` ORDER BY `會員編號` ASC")
    ret2 = cur2.fetchall()
    d_before = ''
    for d2 in ret2:
        if d2[0] != d_before:
            d_before = d2[0]
            p2.add_row(d2)
        else:
            d2 = ['', '', '', '', d2[4]]
            p2.add_row(d2)
    if choose == '1':
        name = input("姓名：")
        bir = input("生日(xxxx.xx.xx)：")
        live = input("地址：")
        cur2.execute("INSERT INTO `member`(`姓名`,`生日`,`地址`)" + "VALUES(%s,%s,%s)", [name, bir, live])
        link.commit()
        os.system('cls')
    elif choose == '2':
        print(p2)
        # a = input('會員編號:')
        # name = input("姓名：")
        # bir = input("生日(xxxx.xx.xx)：")
        # live = input("地址：")
        # cur.execute("UPDATE `member` SET `姓名`=%s,`生日`= %s,`地址`=%s WHERE `會員編號`=%s", [name, bir, live, a])
        par = {'id': input('會員編號:'), 'name': input("姓名:"), 'bir': input("生日:"), 'live': input('地址:')}
        cur2.execute("UPDATE `member` SET `姓名`=%(name)s,`生日`= %(bir)s,`地址`=%(live)s WHERE `會員編號`=%(id)s",
                     par)
        link.commit()
        os.system('cls')
    elif choose == '3':
        print(p2)
        a = input('會員編號:')
        cur2.execute("DELETE FROM`member` WHERE `會員編號`=%s", [a])
        os.system('cls')
        link.commit()
    elif choose == '4':
        print(p2)
    elif choose == '5':
        print(p2)
        b = input('會員編號:')
        c = input('電話:')
        cur3 = link.cursor()
        cur3.execute("INSERT INTO `tel`(`會員編號`,`電話`)" + "VALUES(%s,%s)", [b, c])
        link.commit()
        os.system('cls')
    elif choose == '6':
        print(p2)
        a = input('選擇要刪除電話的會員編號:')
        os.system('cls')
        p3 = prettytable.PrettyTable(["電話編號", '電話'], encoding="utf8")
        cur3 = link.cursor()
        cur3.execute("SELECT `電話編號`,`電話` FROM `tel` WHERE `會員編號`= %s ORDER BY `會員編號` ASC", [a])
        ret3 = cur3.fetchall()
        for d3 in ret3:
            p3.add_row(d3)
        print(p3)
        b = input('電話編號:')
        cur3.execute("DELETE FROM`tel` WHERE `電話編號`=%s", [b])
        os.system('cls')
        link.commit()
    elif choose == '0':
        break
    else:
        pass
link.close()
