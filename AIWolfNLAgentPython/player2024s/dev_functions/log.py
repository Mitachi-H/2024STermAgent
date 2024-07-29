def log(agent_id: int, msg_list: list[str]):
    """
    ログを出力

    TODO:
    - agent_idが1のときと"01"のときでログの出力先が変わることに対処
    - ログを消去する関数を作る
    """
    with open(f"player2024s/dev_functions/logs/agent_{agent_id}_log.txt", "a", encoding="utf-8") as f:
        for msg in msg_list:
            print(msg, file=f)
