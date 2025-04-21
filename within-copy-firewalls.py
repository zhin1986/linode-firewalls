import requests
import json

# 请替换下面的API密钥和防火墙ID
API_KEY = 'your_api_key'
FIREWALL_ID = 'your_firewall_id'

def export_firewall_rules_and_create_new():
    # 获取现有防火墙的规则
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # 获取防火墙规则
    rules_response = requests.get(f'https://api.linode.com/v4/networking/firewalls/{FIREWALL_ID}/rules', headers=headers)
    try:
        rules_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"获取防火墙规则失败：{e}")
        return
    rules_data = rules_response.json()
    print("获取的防火墙规则：", json.dumps(rules_data, indent=2))

    # 创建一个新的防火墙
    new_firewall_data = {
        "label": "new_firewall",
        "rules": {  # 确保包含规则字段
            "inbound_policy": rules_data['inbound_policy'],
            "outbound_policy": rules_data['outbound_policy'],
            "inbound": rules_data['inbound'],
            "outbound": rules_data['outbound']
        }
    }

    print("发送的创建请求数据：", json.dumps(new_firewall_data, indent=2))

    create_response = requests.post('https://api.linode.com/v4/networking/firewalls', headers=headers, json=new_firewall_data)
    try:
        create_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"创建防火墙失败：{e}")
        print("响应内容：", create_response.text)
        return

    new_firewall = create_response.json()
    print("新防火墙创建成功！防火墙ID:", new_firewall['id'])

# 调用函数
export_firewall_rules_and_create_new()
