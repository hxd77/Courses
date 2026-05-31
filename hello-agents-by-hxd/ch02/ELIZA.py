import re
import random

#定义规则库: 模式(正则表达式)->响应模板列表
rules = {
    r'I need (.*)': [ #输入I need(.*)表示匹配后面的任意内容
        "Why do you need {0}?", #0表示.format()表示的第1个参数放到这里
        "Would it really help you to get {0}?", 
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.*\bmother\b.*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.*\bfather\b.*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

# 定义代词转换规则
pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}

def  swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    words = phrase.lower().split() #小写,拆分成单词
    swapped_words=[pronoun_swap.get(word,word) for word in words] #字典中有则替换没有则保持原样
    return " ".join(swapped_words)

def respond(user_input):
    """
    根据规则库生成响应
    """
    for pattern,responses in rules.items():
        match=re.search(pattern,user_input,re.IGNORECASE) #re.IGNORECASE忽略大小写
        if  match:
            #捕获匹配到的部分
            #如果正则表达式里有括号捕获内容，就取第一个捕获内容；如果没有，就用空字符串
            captured_group=match.group(1) if match.groups() else ''
            #进行代词转换
            swapped_group=swap_pronouns(captured_group)
            #从模板中随机选择一个并格式化
            response=random.choice(responses).format(swapped_group)
            return response
    #如果没有匹配任何特定规则，使用最后的通配符规则
    return random.choice(rules[r'.*'])


#主聊天循环
if __name__=='__main__':
    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input=input("You: ")
        if user_input.lower() in ["quit","exit","bye"]:
            print("Therapist: Goodbye. It was nice talking to you.")
            break
        response=respond(user_input)
        print(f"Therapist: {response}")
