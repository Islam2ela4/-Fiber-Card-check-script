from netmiko import ConnectHandler
import time
import openpyxl
from pathlib import Path

delayFactor = 2
#"Fuckingnobes2020"
Username = input("Enter your username: ")
Aterm_Password = input("Enter your Aterm password: ")
Password = input("Enter your Domain password: ")

ATermo = {"host": '213.158.187.244',

          "username": Username,

          "password": Aterm_Password,

          "device_type": "linux",

          "port": "9090",

          "session_log": 'nw.txt',
          }
Connection = ConnectHandler(**ATermo)
xlsx_file = Path('PythonFiber', 'input.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
excel_out = wb_obj.active
count = 2
while True:
    Index_of_IP_Cabinet = "A" + str(count)
    Index_of_Code_Cabinet = "B" + str(count)

    IP_Cabinet = str(excel_out[Index_of_IP_Cabinet].value).strip()
    Code_Cabinet = str(excel_out[Index_of_Code_Cabinet].value).strip()
    if excel_out[Index_of_IP_Cabinet].value is None:
        print('Thank You')
        break

    else:
        try:
            output_1 = Connection.send_command("ssh islam.y80143@" + IP_Cabinet + " \n ", delay_factor=2, read_timeout=20, expect_string=r'[?|:]')

            print("The IP Address is ", IP_Cabinet)
            print(output_1)
            time.sleep(5)

            if str(output_1).lower().__contains__('continue'):
                output_1 = Connection.send_command_timing('yes \n')
                print(output_1)
                time.sleep(2)

                output_3 = Connection.send_command_timing(Password + '\n')
                print(output_3)
                # time.sleep(3)

                output_4 = Connection.send_command_timing("enable\n")
                print(output_4)
                output_5 = Connection.send_command_timing('scroll 512')
                output_6 = Connection.send_command_timing("display board 0\n")
                time.sleep(3)
                print(output_6)

                output_6 = output_6.split("\n")

                for i in output_6:
                    if ("H802OPGE" in i) or ("H803OPGE" in i):
                        print(i[0:8])
                        s = i[0:8]
                        file = open('PythonFiber\\output.txt', 'a')
                        file.write(IP_Cabinet + ' , ')
                        file.write(Code_Cabinet + ' , ')
                        file.write("Yes 'Exist OPG Card'" + '\n')
                        file.close()
                        break

                output_15 = Connection.send_command_timing("quit\n")
                print(output_15)
                time.sleep(2)
                output_15 = Connection.send_command_timing("y\n")
                time.sleep(5)

            elif str(output_1).lower().__contains__('password'):
                output_3 = Connection.send_command_timing(Password + '\n')
                print(output_3)
                # time.sleep(6)

                output_4 = Connection.send_command_timing("enable\n")
                print(output_4)
                output_5 = Connection.send_command_timing('scroll 512')
                output_6 = Connection.send_command_timing("display board 0\n")
                time.sleep(3)
                print(output_6)

                output_6 = output_6.split("\n")

                for i in output_6:
                    if ("H802OPGE" in i) or ("H803OPGE" in i):
                        print(i[0:8])
                        s = i[0:8]
                        file = open('PythonFiber\\output.txt', 'a')
                        file.write(IP_Cabinet + ' , ')
                        file.write(Code_Cabinet + ' , ')
                        file.write("Yes 'Exist OPG Card'" + '\n')
                        file.close()
                        break

                output_15 = Connection.send_command_timing("quit\n")
                print(output_15)
                time.sleep(2)
                output_15 = Connection.send_command_timing("y\n")
                time.sleep(5)

            else:
                file = open('PythonFiber\\down.txt', 'a')
                file.write(IP_Cabinet + ' , ')
                file.write(Code_Cabinet + ' , ')
                if str(output_1).lower().__contains__('network is unreachable'):
                    file.write("Cabinet down" + '\n')
                elif len(str(output_1).strip()) == 0:
                    file.write("Cabinet down" + '\n')
                    Connection.disconnect()
                    Connection = ConnectHandler(**ATermo)
                else:
                    file.write("Error" + '\n')

                file.close()
        except:
            file = open('PythonFiber\\down.txt', 'a')
            file.write(IP_Cabinet + ' , ')
            file.write(Code_Cabinet + ' , ')
            file.write("Cabinet down" + '\n')
            Connection.disconnect()
            Connection = ConnectHandler(**ATermo)
        count += 1
