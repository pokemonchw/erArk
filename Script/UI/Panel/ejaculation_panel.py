from turtle import position
from typing import Tuple
from types import FunctionType
from Script.Core import cache_control, game_type, get_text, flow_handle, text_handle, constant, py_cmd
from Script.Design import attr_calculation
from Script.UI.Moudle import draw, panel
from Script.Config import game_config, normal_config

import random

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
_: FunctionType = get_text._
""" 翻译api """
line_feed = draw.NormalDraw()
""" 换行绘制对象 """
line_feed.text = "\n"
line_feed.width = 1
window_width: int = normal_config.config_normal.text_width
""" 窗体宽度 """


class Ejaculation_Panel:
    """
    用于显示射精界面面板对象
    Keyword arguments:
    width -- 绘制宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 绘制的最大宽度 """
        self.now_panel = _("身体")
        """ 当前绘制的射精页面 """
        self.handle_panel: panel.PageHandlePanel = None
        """ 当前名字列表控制面板 """

    def draw(self):
        """绘制对象"""
        character_data: game_type.Character = cache.character_data[0]
        target_data: game_type.Character = cache.character_data[character_data.target_character_id]
        title_name = "射精部位选择"
        title_draw = draw.TitleLineDraw(title_name, self.width)
        eja_type_list = [_("身体"), _("服装")]
        position_list = []

        self.handle_panel = panel.PageHandlePanel([], Ejaculation_NameDraw, 20, 6, self.width, 1, 1, 0)
        for i in range(14):
            position_list.append(target_data.dirty.body_semen[i][0])
        self.handle_panel.text_list = position_list
        self.handle_panel.update()

        while 1:
            return_list = []
            title_draw.draw()

            # 绘制射精主面板
            for eja_type in eja_type_list:
                if eja_type == self.now_panel:
                    now_draw = draw.CenterDraw()
                    now_draw.text = f"[{eja_type}]"
                    now_draw.style = "onbutton"
                    now_draw.width = self.width / len(eja_type_list)
                    now_draw.draw()
                else:
                    now_draw = draw.CenterButton(
                        f"[{eja_type}]",
                        eja_type,
                        self.width / len(eja_type_list),
                        cmd_func=self.change_panel,
                        args=(eja_type,),
                    )
                    now_draw.draw()
                    return_list.append(now_draw.return_text)
            line_feed.draw()
            line = draw.LineDraw("+", self.width)
            line.draw()

            # 绘制面板本体
            self.handle_panel.update()
            self.handle_panel.draw()
            return_list.extend(self.handle_panel.return_list)
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)

            # 在非页面切换时退出面板
            if yrn not in ['身体','服装']:
                cache.now_panel_id = constant.Panel.IN_SCENE
                break

    def change_panel(self, eja_type: str):
        """
        切换当前面板显示的射精位置类型
        Keyword arguments:
        eja_type -- 要切换的射精位置类型
        """
        self.now_panel = eja_type
        character_data: game_type.Character = cache.character_data[0]
        target_data: game_type.Character = cache.character_data[character_data.target_character_id]
        position_list = []

        if eja_type == "身体":
            for i in range(14):
                position_list.append(target_data.dirty.body_semen[i][0])
        elif eja_type == "服装":
            for i in range(18):
                position_list.append(target_data.dirty.cloth_semen[i][0])

        self.handle_panel = panel.PageHandlePanel(
            position_list, Ejaculation_NameDraw, 20, 6, self.width, 1, 1, 0
        )
        self.handle_panel.text_list = position_list
        self.handle_panel.update()



class Ejaculation_NameDraw:
    """
    点击后可选择射精部位按钮对象
    Keyword arguments:
    text -- 道具id
    width -- 最大宽度
    is_button -- 绘制按钮
    num_button -- 绘制数字按钮
    button_id -- 数字按钮id
    """

    def __init__(self, text: int, width: int, is_button: bool, num_button: bool, button_id: int):
        """初始化绘制对象"""
        self.text = text
        """ 道具id """
        self.draw_text: str = ""
        """ 道具名字绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """
        self.position_text_list = ["头发","脸部","口腔","胸部","腋部","手部","小穴","后穴","尿道","腿部","脚部","尾巴","兽角","兽耳"]
        """ 位置文本列表 """
        self.cloth_text_list = ["帽子","眼镜","耳部","脖子","嘴部","上衣","内衣（上）","手套","下衣","内衣（下）","袜子","鞋子","武器","附属物1","附属物2","附属物3","附属物4","附属物5"]
        """ 衣服文本列表 """
        self.panel_type = 0
        name_draw = draw.NormalDraw()

        # 区分是位置还是衣服
        if self.text in self.position_text_list:
            position_flag = True
            cloth_flag = False
            self.panel_type = 1
        elif self.text in self.cloth_text_list:
            position_flag = False
            cloth_flag = True
            self.panel_type = 2
        # print("debug self.text = ",self.text," panel_type = ",panel_type)

        if self.panel_type == 1:
            # 根据前一指令的情况来区分小穴/后穴/尿道的出现与否
            if constant.Premise.LAST_CMD_SEX:
                if self.button_id in {7,8}:
                    position_flag = False
            elif constant.Premise.LAST_CMD_A_SEX:
                if self.button_id in {6,8}:
                    position_flag = False
            elif constant.Premise.LAST_CMD_U_SEX:
                if self.button_id in {6,7}:
                    position_flag = False
            else:
                if self.button_id in {6,7,8}:
                    position_flag = False

        if is_button and ( position_flag or cloth_flag ):
            if num_button:
                index_text = text_handle.id_index(button_id)
                button_text = f"{index_text} {self.text}"
                name_draw = draw.LeftButton(
                    button_text, self.button_return, self.width, cmd_func=self.shoot_here
                )
            else:
                button_text = f"[{self.text}]"
                name_draw = draw.CenterButton(
                    button_text, self.text, self.width, cmd_func=self.shoot_here
                )
                self.button_return = self.text
            self.draw_text = button_text
        else:
            name_draw = draw.LeftDraw()
            name_draw.text = f"[{self.text}(未插入)]"
            name_draw.width = self.width
            self.draw_text = name_draw.text
        self.now_draw = name_draw
        """ 绘制的对象 """

    def draw(self):
        """绘制对象"""
        self.now_draw.draw()

    def shoot_here(self):
        py_cmd.clr_cmd()

        character_data: game_type.Character = cache.character_data[0]
        target_data: game_type.Character = cache.character_data[character_data.target_character_id]

        cache.shoot_position = self.button_id
        # 乘以一个随机数补正
        random_weight = random.uniform(0.5, 1.5)

        # 基础射精值，小中多射精区分
        if character_data.orgasm_level[3] % 3 == 0:
            semen_count = int(5 * random_weight)
            semen_text = "射精，射出了" + str(semen_count) + "ml精液"
        if character_data.orgasm_level[3] % 3 == 1:
            semen_count = int(20 * random_weight)
            semen_text = "大量射精，射出了" + str(semen_count) + "ml精液"
        if character_data.orgasm_level[3] % 3 == 2:
            semen_count = int(100 * random_weight)
            semen_text = "超大量射精，射出了" + str(semen_count) + "ml精液"
        character_data.orgasm_level[3] += 1

        # print("debug semen_count = ",semen_count)

        # 更新污浊类里的身体部位精液参数
        if self.panel_type == 1:
            target_data.dirty.body_semen[self.button_id][1] += semen_count
            target_data.dirty.body_semen[self.button_id][3] += semen_count
            target_data.dirty.body_semen[self.button_id][2] = attr_calculation.get_semen_now_level(target_data.dirty.body_semen[self.button_id][1])

            now_text = "在" + target_data.name + "的" + self.position_text_list[self.button_id] + semen_text

        # 更新污浊类里的服装部位精液参数
        elif self.panel_type == 2:
            target_data.dirty.cloth_semen[self.button_id][1] += semen_count
            target_data.dirty.cloth_semen[self.button_id][3] += semen_count
            target_data.dirty.cloth_semen[self.button_id][2] = attr_calculation.get_semen_now_level(target_data.dirty.cloth_semen[self.button_id][1])

            now_text = "在" + target_data.name + "的" + self.cloth_text_list[self.button_id] + semen_text

        now_draw = draw.WaitDraw()
        now_draw.text = now_text
        now_draw.width = window_width
        now_draw.draw()
        line_feed.draw()
        line_feed.draw()
