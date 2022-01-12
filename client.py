import json
import socket
from datetime import datetime
from config import HOST, PORT


def main():
    print("------- MP Daily Covid-19 -------")
    print("สำหรับเช็คจำนวนผู้ติดเชื้อโควิด-19 รายวัน\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        while True:
            input_province = input(
                'กรุณากรอกชื่อจังหวัดที่ต้องการตรวจสอบ: ')
            if input_province:
                client.send(input_province.encode())
                response = json.loads(client.recv(1024).decode())
                if response['Status'] == 200:
                    print('\nรายงานการติดเชิ้อโควิดวันที่: {}'.format(
                        datetime.fromisoformat(response['Data']['txn_date']).strftime("%d/%m/%Y"),))
                    print('ประจำจังหวัด: {}'.format(
                        response["Data"]['province']))
                    print('จำนวนผู้ติดเชื้อรายใหม่: {} คน'.format(
                        response['Data']['new_case']))
                    print('จำนวนผู้เสียชีวิตรายใหม่: {} คน'.format(
                        response['Data']['new_death']))
                    print('จำนวนผู้ติดเชื้อสะสม: {} คน'.format(
                        response['Data']['total_case']))
                    print('จำนวนผู้เสียชีวิตสะสม: {} คน'.format(
                        response['Data']['total_death']))
                    print(response)
                else:
                    print(response['Status_line'])
                break
            else:
                print("กรุณากรอกชื่อจังหวัด")
        client.close()


if __name__ == '__main__':
    main()
