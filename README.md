# AI 智能私教

基于 DeepSeek API 和 Streamlit 构建的智能对话机器人。用户可自定义私教人格（姓名/性格），实现个性化健身指导，支持多轮对话与历史记录管理。

## 功能特点

- 🧠 **自定义人格**：可自由设定私教的姓名、性格风格（如硬核/温柔/数据流）
- 💬 **多轮对话**：支持连续对话，具备短期记忆
- 💾 **会话管理**：支持新建、保存、删除历史会话记录

## 技术栈

- Python 3.9+
- Streamlit
- DeepSeek API
- Git

## 快速开始

1. 克隆项目
   '''bash
   git clone https://github.com/gpwjy/wgp_project.git
   cd wgp_project
  ''' 
2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置密钥
   在根目录创建 `.env` 文件，填入你的 DeepSeek API Key：
   ```
   DEEPSEEK_API_KEY=你的密钥
   ```

4. 启动应用
   ```bash
   streamlit run AI-Smart-Trainer.py
   ```
