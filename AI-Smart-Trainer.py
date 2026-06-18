import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

from requests import delete
from streamlit import session_state

st.set_page_config(
    page_title="AI健身私教",
    page_icon="🤖",
    #控制整个网页的布局
    layout="wide",
    #控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)
#保存会话信息函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_date = {
            "nick_name": session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        # 如果sessions目录不存在，则创建
        if not os.path.exists('sessions'):
            os.mkdir('sessions')
        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", 'w', encoding='utf-8') as f:
            json.dump(session_date, f, ensure_ascii=False, indent=4)
#生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


#加载所有的会话列表信息
def load_session_list():
    session_list = []
    #加载session目录下的文件
    if os.path.exists('sessions'):
        file_list = os.listdir('sessions')
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)#排序，降序排序
    return session_list

#加载指定的会话信息
def load_specific_session(session_name):
    try:
        if os.path.exists(f'sessions/{session_name}.json'):
            #读取会话数据
            with open(f'sessions/{session_name}.json', 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                st.session_state.messages = session_data['messages']
                st.session_state.nick_name = session_data['nick_name']
                st.session_state.nature = session_data['nature']
                st.session_state.current_session = session_name
    except Exception as e:
                st.error(f"加载会话失败：{e}")


#删除会话信息的函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")#删除文件
            #如果删除的是当前会话，则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
            st.error(f"删除会话失败：{e}")



#大标题
st.title("AI健身私教")

#logo
st.logo("./AI健身私教/resources/logo.png")

#系统提示词
system_prompt ="""
        你叫%s，现在是用户的AI健身私教，请完全代入私教角色。
        
        规则：
        1. 每次只回1条消息
        2. 禁止任何场景或状态描述性文字
        3. 匹配用户的语言风格
        4. 回复简短有力，像微信聊天一样，别发大段论文
        5. 适当使用💪🔥🏋️‍♂️✅等emoji增加感染力
        6. 用符合私教性格的方式对话
        7. 回复内容要充分体现私教的性格特征和专业感
        
        私教性格：
        - %s
        
        额外专业约束：
        - 涉及动作指导时，优先强调“安全第一”，提示“如有不适立即停止”
        - 涉及饮食建议时，加一句“本建议仅供参考，特殊体质请咨询医师”
        - 不替用户做医疗诊断，只说训练建议
        
        你必须严格遵守上述规则来回复用户。
"""

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "铁教练"
#性格
if "nature" not in st.session_state:
    st.session_state.nature = "专业严谨、充满激情、注重科学训练方法的资深健身教练"
#会话的标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()
#展示聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.messages:#{"role": "user", "content": prompt}
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])



# 创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是Deepseek的API_KEY的值）
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#左侧的侧边栏 -with:streamlit中上下文管理
# st.sidebar.subheader("伴侣信息")
# nick_name = st.sidebar.text_input("昵称")
with st.sidebar:
    #会话信息✏️
    st.subheader("训练控制台")

#新建会话
    if st.button("新建会话",width="stretch",icon="✏️"):
        #1.保存当前会话信息
        save_session()

        #2.创建新的会话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun ()#刷新页面

#会话历史
    st.text("会话历史")

    session_list = load_session_list()
    for session in session_list:
        # st.button(session,width="stretch",icon="📝")
        # st.button("",width="stretch",icon="❌️")
        col1,col2 = st.columns([4,1])
        with col1:
            #加载会话信息
            #三元运算符：如果条件为真，则返回第一个表达式，否则返回第二个表达式---> 语法：值1 if 条件 else 值2
            if st.button(session,width="stretch",icon="📝",key=f"load_{session}",type="primary"if session == st.session_state.current_session else "secondary"):
                load_specific_session(session)
                st.rerun ()

        with col2:
            #删除会话信息
            if st.button("",width="stretch",icon="❌️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()
#分割线
    st.divider()

#私教信息
    st.subheader("私教信息")
    #昵称输入框
    nick_name = st.text_input("教练昵称",placeholder="请输入教练昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    #性格输入框
    nature = st.text_area("教学风格",placeholder="请输入教学风格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


#消息输入框
prompt = st.chat_input("请输入您的健身咨询")
if prompt:#字符串自动转换为布尔值，如果字符串不为空，则返回True；否则返回False
    st.chat_message("user").write(prompt)
    print("--------------> 调用AI大模型，提示词： ", prompt)
    #添加用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    #调用AI大模型
    # print([
    #     {"role": "system", "content": system_prompt},
    #     *st.session_state.messages,
    # ])


    # 与AI大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system","content": system_prompt % (st.session_state.nick_name,st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True,
    )
    # 输出大模型返回的结果
    #非流式输出的解析方式
    # print("<----------- 大模型返回结果： ", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #流失输出的解析方式
    response_message = st.empty()#创建一个空的组件，用于显示大模型返回的结果
    full_response = ""#完整的响应
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content#一个字或者一个词
            full_response += content
            response_message.chat_message("assistant").write(full_response)


    # #添加大模型返回的答案
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})#非流式


    # 添加大模型返回的答案
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    #保存会话信息
    save_session()
