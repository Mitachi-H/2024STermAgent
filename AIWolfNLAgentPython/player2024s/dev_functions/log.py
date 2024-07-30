def log(agent_id: int, msg_list: list[str]):
    """
    ログを出力

    TODO:
    - ログを消去する関数を作る
    """
    if type(agent_id) != int:
        agent_id = int(agent_id)

    with open(f"player2024s/dev_functions/logs/agent_{agent_id}_log.txt", "a", encoding="utf-8") as f:
        for msg in msg_list:
            print(msg, file=f)

def clear_log(agent_id: int):
    """
    ログを消去する
    """

    if type(agent_id) != int:
        agent_id = int(agent_id)
    
    filename = f"player2024s/dev_functions/logs/agent_{agent_id}_log.txt"

    with open(filename, "w", encoding="utf-8") as f:
        pass
