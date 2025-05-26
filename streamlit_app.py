import warnings
import streamlit as st
import re
import random

warnings.simplefilter(action="ignore", category=FutureWarning)

# Must be the first Streamlit command
st.set_page_config(page_title="静躁独行", layout="wide")

def load_story():
    try:
        with open('静躁独行.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到本体部分
        body_start = content.find("本体部分:")
        if body_start == -1:
            st.error("找不到本体部分")
            return {}
            
        content = content[body_start:]
        
        # 使用更宽松的正则表达式匹配所有段落
        pattern = r"\$t1 == '(\d+)'\?\s*`([\s\S]*?)`,"
        matches = re.findall(pattern, content)
        
        story_dict = {}
        for num, text in matches:
            # 清理文本
            text = text.strip()
            # 移除开头的换行符
            text = re.sub(r'^\n+', '', text)
            # 将换行符替换为HTML的br标签
            text = text.replace('\n', '<br>')
            story_dict[num] = text
        
        return story_dict
    except Exception as e:
        st.error(f"加载文本文件时出错：{str(e)}")
        return {}

def show_preface():
    st.title("静躁独行 - 互动小说")
    
    st.markdown("### 前言")
    preface = """
我常开玩笑说，我是在《The Blair With Project》的那片森林里长大的。

我们家的四周被两公里宽的国家森林团团围住。在这样一个黑暗粘稠压抑、屋外的声音经常无法分辨的地方长大，我学会了欣赏自然带来的恐怖——这种恐怖在人潮汹涌的大城市是不存在的。我学会享受在家时所感受到的保护，即使这种保护实际上虚无缥缈。这是原木墙和泥砖将寒冷和黑暗阻隔在外的感觉，即使有东西轻轻地爬过我卧室窗户的声音实际上……司空见惯。

《静噪独行》是我尝试以克苏鲁神话的视角看待寂静原野的一次尝试。我尝试给予玩家强烈的孤离感。将场景设置在 90 年代也让我得以展示克苏鲁的呼唤可以适用于各种设定——现代为1920 年代所不存在的恐怖展开了舞台，例如，来源不明的吓人录像带。

祝愿克苏鲁的呼唤的新老玩家都能在本作中体会这种之前或许从未体会过的恐怖。特别是，祝愿大家能从本作中找到灵感，在游戏中描绘自己的神话恐怖故事。

B. W. Holland，于墨尔本，2022年。
    """
    st.markdown(preface)
    
    # 添加下一页按钮
    if st.button("下一页 - 选择角色"):
        st.session_state.page = "character_selection"
        st.rerun()

def generate_luck():
    """生成幸运值：3个1-6的随机数之和乘以5"""
    dice_sum = sum(random.randint(1, 6) for _ in range(3))
    return dice_sum * 5

def show_character_selection(story_dict):
    st.title("选择你的角色")
    
    # 添加前言描述
    st.markdown("""
### 前言
在被人遗忘的荒野，在松针铺满森林地面的地方，有东西颤动着。

风吹过黑山峰，吹向熊、兔子和鸟都从不会造访的地方。周遭森林的树木颤抖着。在湿润的土地下面，有东西苏醒了。

在土壤下面移动着，它无声地破土而出。它的现身震撼了荒野。在远方，一头狼为了将要逝去的而哀嚎。

它从黑暗和喘息中抽身。

它眨了眨眼。

现在请选择你的角色，并下载一份记录卡。

在游戏中，有些条目会指示你在记录表上勾选特定的选项。另一些条目会根据记录表上一些选项是否勾选提供额外的选项。还有一些条目会禁止你选择一些选项，要求你必须转到特定的条目。以上这些都以你做出的行动为前提。                               
    """)
    
    # 添加记录卡下载按钮
    st.markdown("### 下载记录卡")
    st.markdown("请下载并打印记录卡，在游戏过程中记录你的选择。")
    if st.button("下载记录卡", key="download_card"):
        st.markdown(f'<a href="https://gchat.qpic.cn/gchatpic_new/2700037224/928603289-2675160794-943AD91C0535666ED11289D8B24804DE/0?term=2&is_origin=0" target="_blank">点击这里下载记录卡</a>', unsafe_allow_html=True)
    
    # 检查是否成功加载了角色卡
    if '372' not in story_dict:
        st.error("无法加载角色卡，请检查文本文件是否正确。")
        return
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    # 在左侧显示选中的角色卡（如果有）
    if 'selected_character' in st.session_state:
        # 清除侧边栏的所有内容
        st.sidebar.empty()
        # 显示选中的角色卡
        st.sidebar.markdown("### 你的角色卡")
        if st.session_state.selected_character == '373':
            # 显示查理的角色卡
            charlie_card = f"""
### 查理
**职业：** 护士  
**出生地：** 皮尔，南达科他州  
**现居地：** 皮尔，南达科他州  

**属性：**  
力量 60 | 体型 65 | 体质 70 | 意志 60  
敏捷 60 | 外貌 75 | 智力 65 | 教育 70  

**其他属性：**  
HP 13 | MP 12 | DB +1D4  
信用评级 30  
闪避 30  
幸运 {st.session_state.luck_value}  

**技能：**  
格斗（斗殴） 55  
急救 70  
恐吓 45  
母语（英语） 70  
聆听 60  
博物学 40  
导航 20  
说服 50  
心理学 60  
科学（生物学） 25  
科学（化学） 25  
侦查 65  
潜行 30  

**背景故事：**  
查理和亚历克斯在一起已经快五年了。他们的关系最近有些裂痕。也许独处一段时间有助于修补关系，但是，实话实说，感觉不太靠谱……

**思想信念：** 罪业报应。  
**重要之人：** 亚历克斯，不论好坏……  
**重要之地：** 亚历克斯旧公寓对面的长椅，两人第一次接吻的地方。  
**重要之物：** 家传的求婚戒指。  
**个人特质：** 绝望的、异想天开的。  
**财富：** 开销水平200，现金1200，资产 $30000。
            """
            st.sidebar.markdown(charlie_card)
        elif st.session_state.selected_character == '372':
            # 显示亚历克斯的角色卡
            alex_card = f"""
### 亚历克斯
**职业：** 销售员  
**出生地：** 戴德伍德，南达科他州  
**现居地：** 皮尔，南达科他州  
**年龄：** 32  

**属性：**  
力量 70 | 体型 75 | 体质 60 | 意志 50  
敏捷 65 | 外貌 60 | 智力 55 | 教育 65  

**其他属性：**  
HP 13 | MP 10 | DB +1D4  
会计 20  
信用评级 40  
闪避 32  
幸运 {st.session_state.luck_value}  

**技能：**  
汽车驾驶 45  
格斗（斗殴） 55  
急救 40  
恐吓 60  
母语（英语） 65  
聆听 50  
博物学 30  
导航 40  
说服 60  
心理学 45  
侦查 35  
潜行 35  

**背景故事：**  
亚历克斯与查理在一起已经快五年了。查理最近越来越不开心。查理的哥哥马克建议去他的度假小屋独处一段时间。这曾经帮到了马克和他妻子朱莉。这也可能对亚历克斯和查理有用……

**个人描述：** 粗犷或邋遢，取决于你的仁慈程度。  
**思想信念：** 我只相信亲自看到的。  
**重要之人：** 查理，尽管发生了这一切……  
**重要之地：** 第一次约会时查理订的餐馆。  
**重要之物：** 查理写的情书。  
**个人特质：** 无可救药的浪漫派。充满保护欲。  
**财富：** 开销水平200，现金1600，资产 $40000。
            """
            st.sidebar.markdown(alex_card)
        else:
            st.sidebar.markdown(story_dict[st.session_state.selected_character], unsafe_allow_html=True)
    
    # 在右侧显示角色选项
    with col1:
        st.markdown("### 角色选项 1 - 亚历克斯")
        alex_card = """
### 亚历克斯
**职业：** 销售员  
**出生地：** 戴德伍德，南达科他州  
**现居地：** 皮尔，南达科他州  
**年龄：** 32  

**属性：**  
力量 70 | 体型 75 | 体质 60 | 意志 50  
敏捷 65 | 外貌 60 | 智力 55 | 教育 65  

**其他属性：**  
HP 13 | MP 10 | DB +1D4  
会计 20  
信用评级 40  
闪避 32  

**技能：**  
汽车驾驶 45  
格斗（斗殴） 55  
急救 40  
恐吓 60  
母语（英语） 65  
聆听 50  
博物学 30  
导航 40  
说服 60  
心理学 45  
侦查 35  
潜行 35  

**背景故事：**  
亚历克斯与查理在一起已经快五年了。查理最近越来越不开心。查理的哥哥马克建议去他的度假小屋独处一段时间。这曾经帮到了马克和他妻子朱莉。这也可能对亚历克斯和查理有用……

**个人描述：** 粗犷或邋遢，取决于你的仁慈程度。  
**思想信念：** 我只相信亲自看到的。  
**重要之人：** 查理，尽管发生了这一切……  
**重要之地：** 第一次约会时查理订的餐馆。  
**重要之物：** 查理写的情书。  
**个人特质：** 无可救药的浪漫派。充满保护欲。  
**财富：** 开销水平200，现金1600，资产 $40000。
        """
        st.markdown(alex_card)
        if st.button("选择角色 1", key="char1"):
            st.session_state.selected_character = '372'
            st.session_state.luck_value = generate_luck()
            st.rerun()
    
    with col2:
        st.markdown("### 角色选项 2 - 查理")
        charlie_card = """
### 查理
**职业：** 护士  
**出生地：** 皮尔，南达科他州  
**现居地：** 皮尔，南达科他州  

**属性：**  
力量 60 | 体型 65 | 体质 70 | 意志 60  
敏捷 60 | 外貌 75 | 智力 65 | 教育 70  

**其他属性：**  
HP 13 | MP 12 | DB +1D4  
信用评级 30  
闪避 30  

**技能：**  
格斗（斗殴） 55  
急救 70  
恐吓 45  
母语（英语） 70  
聆听 60  
博物学 40  
导航 20  
说服 50  
心理学 60  
科学（生物学） 25  
科学（化学） 25  
侦查 65  
潜行 30  

**背景故事：**  
查理和亚历克斯在一起已经快五年了。他们的关系最近有些裂痕。也许独处一段时间有助于修补关系，但是，实话实说，感觉不太靠谱……

**思想信念：** 罪业报应。  
**重要之人：** 亚历克斯，不论好坏……  
**重要之地：** 亚历克斯旧公寓对面的长椅，两人第一次接吻的地方。  
**重要之物：** 家传的求婚戒指。  
**个人特质：** 绝望的、异想天开的。  
**财富：** 开销水平200，现金1200，资产 $30000。
        """
        st.markdown(charlie_card)
        if st.button("选择角色 2", key="char2"):
            st.session_state.selected_character = '373'
            st.session_state.luck_value = generate_luck()
            st.rerun()
    
    # 如果已经选择了角色，显示开始游戏按钮
    if 'selected_character' in st.session_state:
        # 显示背景故事
        st.markdown("### 背景故事")
        background_story = """
亚历克斯与查理在一起已经快五年了。查理最近越来越不开心。查理的哥哥马克建议去他的度假小屋独处一段时间。这曾经帮到了马克和他妻子朱莉。这也可能对亚历克斯和查理有用……
        """
        st.markdown(background_story)
        
        if st.button("开始游戏"):
            st.session_state.page = "game"
            st.rerun()

def get_skill_value(character, skill_name):
    """获取角色特定技能或属性的值"""
    # 检查是否是幸运鉴定
    if skill_name == "幸运":
        return st.session_state.luck_value
        
    if character == '373':  # 查理
        # 属性值
        attributes = {
            '力量': 60,
            '体型': 65,
            '体质': 70,
            '意志': 60,  # 理智鉴定使用意志值
            '敏捷': 60,
            '外貌': 75,
            '智力': 65,
            '教育': 70
        }
        # 技能值
        skill_values = {
            '格斗': 55,
            '急救': 70,
            '恐吓': 45,
            '母语': 70,
            '聆听': 60,
            '博物学': 40,
            '导航': 20,
            '说服': 50,
            '心理学': 60,
            '科学': 25,  # 生物学和化学都是25
            '侦查': 65,
            '潜行': 30
        }
        # 处理特殊情况，如"科学（生物学）"或"科学（化学）"
        if skill_name.startswith('科学'):
            return skill_values['科学']
        # 先检查是否是属性
        if skill_name in attributes:
            return attributes[skill_name]
        # 再检查是否是技能
        return skill_values.get(skill_name, 0)
    elif character == '372':  # 亚历克斯
        # 属性值
        attributes = {
            '力量': 70,
            '体型': 75,
            '体质': 60,
            '意志': 50,  # 理智鉴定使用意志值
            '敏捷': 65,
            '外貌': 60,
            '智力': 55,
            '教育': 65
        }
        # 技能值
        skill_values = {
            '会计': 20,
            '汽车驾驶': 45,
            '格斗': 55,
            '急救': 40,
            '恐吓': 60,
            '母语': 65,
            '聆听': 50,
            '博物学': 30,
            '导航': 40,
            '说服': 60,
            '心理学': 45,
            '侦查': 35,
            '潜行': 35
        }
        # 先检查是否是属性
        if skill_name in attributes:
            return attributes[skill_name]
        # 再检查是否是技能
        return skill_values.get(skill_name, 0)
    else:
        return 50  # 默认值

def check_skill_check(content, character):
    """检查内容中是否包含技能鉴定提示，并返回相关信息"""
    # 匹配多种鉴定提示模式
    patterns = [
        r"进行(.*?)鉴定",  # 进行心理学鉴定
        r"进行(.*?)检定",  # 进行心理学检定
        r"进行(.*?)判定",  # 进行心理学判定
        r"进行(.*?)检查",  # 进行心理学检查
        r"进行(.*?)测试",  # 进行心理学测试
        r"进行(.*?)判定",  # 进行心理学判定
        r"进行一次(.*?)检定",  # 进行一次心理学检定
        r"进行一次(.*?)鉴定",  # 进行一次心理学鉴定
        r"进行一次(.*?)判定",  # 进行一次心理学判定
        r"进行一次(.*?)检查",  # 进行一次心理学检查
        r"进行一次(.*?)测试",  # 进行一次心理学测试
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            skill_name = match.group(1).strip()
            # 处理一些特殊情况
            if "理智" in skill_name:
                return True, "意志"  # 理智鉴定使用意志值
            if "幸运" in skill_name:
                return True, "幸运"  # 幸运鉴定
            if "心理学" in skill_name:
                return True, "心理学"
            if "侦查" in skill_name:
                return True, "侦查"
            if "聆听" in skill_name:
                return True, "聆听"
            if "格斗" in skill_name:
                return True, "格斗"
            if "急救" in skill_name:
                return True, "急救"
            if "恐吓" in skill_name:
                return True, "恐吓"
            if "母语" in skill_name:
                return True, "母语"
            if "博物学" in skill_name:
                return True, "博物学"
            if "导航" in skill_name:
                return True, "导航"
            if "说服" in skill_name:
                return True, "说服"
            if "科学" in skill_name:
                return True, "科学"
            if "潜行" in skill_name:
                return True, "潜行"
            # 添加属性检查
            if "力量" in skill_name:
                return True, "力量"
            if "体型" in skill_name:
                return True, "体型"
            if "体质" in skill_name:
                return True, "体质"
            if "意志" in skill_name:
                return True, "意志"
            if "敏捷" in skill_name:
                return True, "敏捷"
            if "外貌" in skill_name:
                return True, "外貌"
            if "智力" in skill_name:
                return True, "智力"
            if "教育" in skill_name:
                return True, "教育"
            return True, skill_name
    return False, None

def show_game(story_dict):
    st.title("静躁独行 - 互动小说")
    
    # 在左侧显示选中的角色卡
    if 'selected_character' in st.session_state:
        # 清除侧边栏的所有内容
        st.sidebar.empty()
        # 显示选中的角色卡
        st.sidebar.markdown("### 你的角色卡")
        if st.session_state.selected_character == '373':
            # 显示查理的角色卡
            charlie_card = """
### 查理
**职业：** 护士  
**出生地：** 皮尔，南达科他州  
**现居地：** 皮尔，南达科他州  

**属性：**  
力量 60 | 体型 65 | 体质 70 | 意志 60  
敏捷 60 | 外貌 75 | 智力 65 | 教育 70  

**其他属性：**  
HP 13 | MP 12 | DB +1D4  
信用评级 30  
闪避 30  

**技能：**  
格斗（斗殴） 55  
急救 70  
恐吓 45  
母语（英语） 70  
聆听 60  
博物学 40  
导航 20  
说服 50  
心理学 60  
科学（生物学） 25  
科学（化学） 25  
侦查 65  
潜行 30  

**背景故事：**  
查理和亚历克斯在一起已经快五年了。他们的关系最近有些裂痕。也许独处一段时间有助于修补关系，但是，实话实说，感觉不太靠谱……

**思想信念：** 罪业报应。  
**重要之人：** 亚历克斯，不论好坏……  
**重要之地：** 亚历克斯旧公寓对面的长椅，两人第一次接吻的地方。  
**重要之物：** 家传的求婚戒指。  
**个人特质：** 绝望的、异想天开的。  
**财富：** 开销水平200，现金1200，资产 $30000。
            """
            st.sidebar.markdown(charlie_card)
        else:
            st.sidebar.markdown(story_dict[st.session_state.selected_character], unsafe_allow_html=True)
    
    # 显示可用的编号示例
    st.markdown("### 使用说明")
    st.markdown("""
    1. 请输入段落编号（纯数字）
    2. 编号范围：0-373
    3. 示例编号：0, 1, 2, 3, 4, 5
    4. 要开始游戏，请输入0
    """)
    
    # 创建输入框
    user_input = st.text_input("请输入段落编号", "")
    
    if user_input:
        try:
            # 检查输入是否为纯数字
            if not user_input.isdigit():
                st.error("请输入纯数字编号！")
                return
                
            # 检查编号是否在有效范围内
            if int(user_input) < 0 or int(user_input) > 373:
                st.error("编号必须在0-373之间！")
                return
                
            # 尝试获取对应段落的内容
            content = story_dict.get(user_input)
            if content:
                st.markdown("### 故事内容")
                st.markdown(content, unsafe_allow_html=True)
                
                # 检查是否需要技能鉴定
                needs_check, skill_name = check_skill_check(content, st.session_state.selected_character)
                if needs_check:
                    st.markdown(f"### 需要进行{skill_name}鉴定")
                    if st.button("进行鉴定"):
                        # 生成随机数
                        roll = random.randint(1, 100)
                        # 获取角色技能值
                        skill_value = get_skill_value(st.session_state.selected_character, skill_name)
                        # 显示结果
                        st.markdown(f"### 鉴定结果")
                        st.markdown(f"随机数：{roll}")
                        st.markdown(f"技能值：{skill_value}")
                        
                        # 查找成功和失败的跳转目标
                        success_target = None
                        failure_target = None
                        
                        # 使用正则表达式查找跳转目标
                        success_pattern = r"如果检定成功，转到(\d+)。"
                        failure_pattern = r"如果检定失败，转到(\d+)。"
                        
                        success_match = re.search(success_pattern, content)
                        failure_match = re.search(failure_pattern, content)
                        
                        if success_match:
                            success_target = success_match.group(1)
                        if failure_match:
                            failure_target = failure_match.group(1)
                        
                        if roll <= skill_value:
                            st.success("鉴定成功！")
                            if success_target:
                                st.info(f"如果检定成功，转到 {success_target}")
                        else:
                            st.error("鉴定失败！")
                            if failure_target:
                                st.info(f"如果检定失败，转到 {failure_target}")
            else:
                st.warning(f"未找到编号 {user_input} 的段落，请检查输入是否正确。")
        except Exception as e:
            st.error(f"发生错误：{str(e)}")

def main():
    # 初始化session state
    if 'page' not in st.session_state:
        st.session_state.page = "preface"
    if 'current_paragraph' not in st.session_state:
        st.session_state.current_paragraph = None
    if 'luck_value' not in st.session_state:
        st.session_state.luck_value = None
    
    # 加载故事内容
    story_dict = load_story()
    
    # 根据当前页面显示不同内容
    if st.session_state.page == "preface":
        show_preface()
    elif st.session_state.page == "character_selection":
        show_character_selection(story_dict)
    elif st.session_state.page == "game":
        show_game(story_dict)

if __name__ == "__main__":
    main()
