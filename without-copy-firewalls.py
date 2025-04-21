import requests
import json

# 源账号API密钥和防火墙ID
SOURCE_API_KEY = 'source_account_api_key'
SOURCE_FIREWALL_ID = 'source_firewall_id'

# 目标账号API密钥
TARGET_API_KEY = 'target_account_api_key'

def export_firewall_rules_and_create_new():
    # 获取现有防火墙的规则
    headers_source = {
        'Authorization': f'Bearer {SOURCE_API_KEY}',
        'Content-Type': 'application/json'
    }

    # 获取防火墙基本信息
    response = requests.get(f'https://api.linode.com/v4/networking/firewalls/{SOURCE_FIREWALL_ID}', headers=headers_source)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"获取防火墙基本信息失败：{e}")
        return
    firewall_data = response.json()
    print("获取的防火墙基本信息：", json.dumps(firewall_data, indent=2))

    # 获取防火墙规则
    rules_response = requests.get(f'https://api.linode.com/v4/networking/firewalls/{SOURCE_FIREWALL_ID}/rules', headers=headers_source)
    try:
        rules_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"获取防火墙规则失败：{e}")
        return
    rules_data = rules_response.json()
    print("获取的防火墙规则：", json.dumps(rules_data, indent=2))

    # 创建一个新的防火墙
    headers_target = {
        'Authorization': f'Bearer {TARGET_API_KEY}',
        'Content-Type': 'application/json'
    }

    new_firewall_data = {
        "label": firewall_data['label'],  # 使用源防火墙的标签名称
        "rules": {
            "inbound_policy": rules_data['inbound_policy'],
            "outbound_policy": rules_data['outbound_policy'],
            "inbound": rules_data['inbound'],
            "outbound": rules_data['outbound']
        }
    }

    print("发送的创建请求数据：", json.dumps(new_firewall_data, indent=2))

    create_response = requests.post('https://api.linode.com/v4/networking/firewalls', headers=headers_target, json=new_firewall_data)
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
