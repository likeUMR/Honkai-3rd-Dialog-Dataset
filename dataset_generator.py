import os
import json
import random

def read_dialog_files(directory):
    dialogs = []
    for filename in os.listdir(directory):
        if filename.startswith("dialog_") and filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                dialogs.append(file.readlines())
    return dialogs

def generate_data(dialogs):
    data = {}
    for dialog in dialogs:
        history = []
        
        for i, line in enumerate(dialog):
            speaker, utterance = line.split(": ", 1)
            
            if speaker == '旁白':
                continue
            
            query = speaker+":"
            response = utterance.strip()
            
            if speaker not in data:
                data[speaker] = []
            
            if len(history) > 0:
                history_portion = random.randint(3, 7) #随机挑选3-7个历史对话作为上下文
                selected_history = history[-history_portion:]
                history_format = [[dialog[x].split(": ", 1)[0]+":", dialog[x].split(": ", 1)[1].strip()] for x in selected_history]
                data[speaker].append({"query": query, "response": response, "history": history_format})
            else:
                data[speaker].append({"query": query, "response": response, "history": []})
            
            if response:
                history.append(i)

    return data

def save_data(data, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for speaker, dialogues in data.items():
        count = len(dialogues)
        if count > 5:  # 只有当说话人的对话条目数大于5时才保存
            filename = f"{speaker}_{count}.json"
            with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as f:
                json.dump(dialogues, f, ensure_ascii=False, indent=2)


# Main script
input_directory = "orgin_text"  # 更改为对话文件的实际目录
output_directory = "formatted_json"  # 更改为保存输出文件的实际目录

dialogs = read_dialog_files(input_directory)
data = generate_data(dialogs)
save_data(data, output_directory)

print("数据集生成完成。")