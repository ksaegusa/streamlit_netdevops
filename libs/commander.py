
from netmiko import ConnectHandler


def st_commander(st):
    st.title("Commander")
    # NOTE: 適当にピックアップ
    #       Netmikoのプラットフォーム対応は下記を参照
    #       https://ktbyers.github.io/netmiko/PLATFORMS.html
    device_type_list =[
        "cisco_ios",
        "cisco_asa",
        "cisco_nxos",
        "cisco_xe",
        "cisco_xr",
        "linux",
        "vyos",
        "yamaha",
    ]

    with st.expander("認証情報"):
        address = st.text_input("アドレス","X.X.X.X")
        user = st.text_input("ユーザー","admin")
        password = st.text_input("パスワード", "password")
        port = st.number_input("ポート",22),
        secret = st.text_input("enableパスワード", "")
        device_type = st.selectbox("デバイスタイプ", device_type_list)

    command = st.text_input("コマンド","show ip route")

    device = {
        "device_type": device_type,
        "host": address,
        "username": user,
        "password": password,
        "port": port[0],
        "secret": secret
    }

    if st.button("実行"):
        with ConnectHandler(**device) as net_connect:
            if secret:
                net_connect.enable()
            output = net_connect.send_command(command)

        commander_container = st.container(border=True, height=700)
        commander_container.code(output, language="log")
        st.download_button(
            label="テキストダウンロード",
            data=output,
            file_name=f"{address}_{command.replace(' ','_').replace('|','_')}.txt"
        )
