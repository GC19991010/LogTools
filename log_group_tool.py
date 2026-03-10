import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QCheckBox, QTextEdit,
                             QLabel, QGridLayout)
from PyQt5.QtCore import Qt
from datetime import datetime

class LogGroupTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志组掩码计算器")
        self.resize(1000, 800)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 选项卡组件
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.update_log_mask)
        main_layout.addWidget(self.tab_widget)

        # 存储所有日志组复选框的列表
        self.log_group_checkboxes = []

        # 提前创建底部输出区域（先创建对象，避免信号提前触发时报错）
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("勾选复选框后，此处会显示生成的 adb 命令和选中的变量...")

        # 创建日志组选项卡（此时 output_text 已存在）
        self.create_log_tabs()

        # 将输出框添加到布局（放在选项卡下方）
        main_layout.addWidget(self.output_text)

    def create_log_tabs(self):
        """创建三个日志组选项卡：MIVI、Qcom_CAMX、Qcom_CHI"""
        # 定义所有日志组，按前缀分组
        mivi_groups = {
            'Mia2LogGroupCore': 1 << 0,
            'Mia2LogGroupPlugin': 1 << 1,
            'Mia2LogGroupMeta': 1 << 2,
            'Mia2LogGroupService': 1 << 3,
            'Mia2LogGroupDebug': 1 << 4,
            'LogGroupCore': 1 << 5,
            'LogGroupHAL': 1 << 6,
            'LogGroupRT': 1 << 7,
            'Mia2LogGroupAlgorithm': 1 << 8,
            'Mia2LogGroupCallStack': 1 << 9,
            'LogGroupTBM': 1 << 10,
            'Mia2LogGroupCoreRT': 1 << 11,
            'Mia2LogGroupOffCam': 1 << 12,
            'LogGroupSdk': 1 << 13,
            'LogGroupPerf': 1 << 14,
            'Mia2LogGroupPerf': 1 << 15,
        }

        qcom_camx_groups = {
            'CamxLogGroupAFD'           : 1 << 0,
            'CamxLogGroupSensor'        : 1 << 1,
            'CamxLogGroupTracker'       : 1 << 2,
            'CamxLogGroupISP'           : 1 << 3,
            'CamxLogGroupPProc'         : 1 << 4,
            'CamxLogGroupMemMgr'        : 1 << 5,
            'CamxLogGroupPower'         : 1 << 6,
            'CamxLogGroupHAL'           : 1 << 7,
            'CamxLogGroupJPEG'          : 1 << 8,
            'CamxLogGroupStats'         : 1 << 9,
            'CamxLogGroupCSL'           : 1 << 10,
            'CamxLogGroupApp'           : 1 << 11,
            'CamxLogGroupUtils'         : 1 << 12,
            'CamxLogGroupSync'          : 1 << 13,
            'CamxLogGroupMemSpy'        : 1 << 14,
            'CamxLogGroupFormat'        : 1 << 15,
            'CamxLogGroupCore'          : 1 << 16,
            'CamxLogGroupHWL'           : 1 << 17,
            'CamxLogGroupChi'           : 1 << 18,
            'CamxLogGroupDRQ'           : 1 << 19,
            'CamxLogGroupFD'            : 1 << 20,
            'CamxLogGroupIQMod'         : 1 << 21,
            'CamxLogGroupLRME'          : 1 << 22,
            'CamxLogGroupCVP'           : 1 << 22,
            'CamxLogGroupNCS'           : 1 << 23,
            'CamxLogGroupMeta'          : 1 << 24,
            'CamxLogGroupAEC'           : 1 << 25,
            'CamxLogGroupAWB'           : 1 << 26,
            'CamxLogGroupAF'            : 1 << 27,
            'CamxLogGroupSWP'           : 1 << 28,
            'CamxLogGroupHist'          : 1 << 29,
            'CamxLogGroupBPS'           : 1 << 30,
            'CamxLogGroupDebugData'     : 1 << 31,       
            'CamxLogGroupQSAT'          : 1 << 32,
            'CamxLogGroupQLL'           : 1 << 9,
            'CamxLogGroupPSM'           : 1 << 33,
            'CamxLogGroupStatsNN'       : 1 << 34,
            'CamxLogGroupCRE'           : 1 << 35,
            'CamxLogGroupOFE'           : 1 << 36,
            'CamxLogGroupAWBR'          : 1 << 37,
            'CamxLogGroupITOF'          : 1 << 38,
            'CamxLogGroupPerf'          : 1 << 39,
            'CamxLogGroupStatsParse'    : 1 << 40,
            'CamxLogGroupCrop'          : 1 << 41,
        }

        qcom_chi_groups = {
            'ChxLogGroupCore'           :1 << 0,
            'ChxLogGroupUsecase'        :1 << 1,
            'ChxLogGroupF2Core'         :1 << 2,
            'ChxLogGroupMCXCore'        :1 << 3,
            'ChxLogGroupF2GS'           :1 << 4,
            'ChxLogGroupF2Feature'      :1 << 5,
            'ChxLogGroupF2Req'          :1 << 6,
            'ChxLogGroupOffCam'         :1 << 7,
            'ChxLogGroupSBM'            :1 << 8,
            'ChxLogGroupTBM'            :1 << 9,
            'ChxLogGroupUtils'          :1 << 10,
            'ChxLogGroupChiNode'        :1 << 11,
            'ChxLogGroupHMS'            :1 << 12,
            'ChxLogGroupChiMetadata'    :1 << 13,
            'ChxLogGroupProviderExt'    :1 << 14,
            'ChxLogGroupFD'             :1 << 15,
            'ChxLogGroupCrop'           :1 << 16,
            'ChxLogGroupOEMSensor'      :1 << 20,
            'ChxLogGroupOEMActuator'    :1 << 21,
            'ChxLogGroupOEMEEPROM'      :1 << 22,
            'ChxLogGroupOEMOIS'         :1 << 23,
        }

        mtk_groups = {
            '待大佬开发补充'           :1 << 0,
        }

        # 添加选项卡（标题字符串必须与后续判断完全一致）
        self.add_group_tab("MIVI", mivi_groups)
        self.add_group_tab("Qcom_CAMX", qcom_camx_groups)
        self.add_group_tab("Qcom_CHI", qcom_chi_groups)
        self.add_group_tab("MTK", mtk_groups)

    def add_group_tab(self, title, groups_dict):
        """创建一个选项卡，内部包含给定字典的所有复选框"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 标题说明
        label = QLabel(f"请选择需要启用的 {title} 日志组：")
        label.setWordWrap(True)
        layout.addWidget(label)

        # 网格布局放置复选框
        grid = QGridLayout()
        layout.addLayout(grid)

        # 将复选框添加到网格（4列）
        col_count = 4
        for idx, (name, value) in enumerate(groups_dict.items()):
            cb = QCheckBox(name)
            cb.setProperty("bit_value", value)   # 存储位值
            cb.setProperty("tab_title", title)   # 记录所属选项卡
            cb.stateChanged.connect(self.update_log_mask)
            self.log_group_checkboxes.append(cb)  # 加入全局列表

            row = idx // col_count
            col = idx % col_count
            grid.addWidget(cb, row, col)

        # 添加弹性空间
        layout.addStretch()

        self.tab_widget.addTab(tab, title)

    def update_log_mask(self):
        """计算当前选项卡内选中的日志组掩码，并根据选项卡生成不同命令，同时更新选中项的样式"""
        # 获取当前选项卡标题
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_title = self.tab_widget.tabText(current_tab_index)

        mask = 0
        selected_names = []

        # 先更新所有复选框的样式（根据选中状态）
        for cb in self.log_group_checkboxes:
            if cb.isChecked():
                # 选中状态：红色粗体下划线
                cb.setStyleSheet("QCheckBox { color: red; font-weight: bold; text-decoration: underline; }")
                # 如果属于当前选项卡，同时收集数据
                if cb.property("tab_title") == current_tab_title:
                    bit = cb.property("bit_value")
                    mask |= bit
                    selected_names.append(cb.text())
            else:
                # 未选中：恢复默认样式
                cb.setStyleSheet("")  # 清空样式表，恢复系统默认

        # 生成十六进制掩码
        hex_mask = hex(mask)

        # 清空输出区域，显示最新信息
        self.output_text.clear()

        # 根据当前选项卡生成不同的 adb 命令（请根据实际需求调整）
        if current_tab_title == "MIVI":
            adb_cmd = f"adb shell setprop persist.vendor.camera.mivi.groupsEnable {hex_mask}"
        elif current_tab_title == "Qcom_CAMX":
            adb_cmd = f"adb shell setprop persist.vendor.camera.logInfoMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.logCoreCfgMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.logConfigMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.logVerboseMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.logDumpMask {hex_mask}\n"
        elif current_tab_title == "Qcom_CHI":
            adb_cmd = f"adb shell setprop persist.vendor.camera.chiLogInfoMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.chiLogConfigMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.chiLogVerboseMask {hex_mask}\n"
            adb_cmd += f"adb shell setprop persist.vendor.camera.chiLogWarningMask {hex_mask}\n"
        elif current_tab_title == "MTK":
            adb_cmd = f"MTK log 开启过于复杂且不规律，待大佬进行补充"
        else:
            adb_cmd = f"adb shell setprop persist.vendor.camera.mivi.groupsEnable {hex_mask}"
        self.output_text.append(f"{adb_cmd}")

        # 显示当前选项卡内选中的变量名
        if selected_names:
            self.output_text.append(f"\n选中的日志组: {', '.join(selected_names)}")
        else:
            self.output_text.append(f"\n当前未选中任何日志组")

        # 可选：显示当前掩码
        self.output_text.append(f"\n掩码值: {hex_mask} (十进制: {mask})")

    def append_message(self, message):
        """在底部输出区域追加一条带时间戳的消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.append(f"[{timestamp}] {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogGroupTool()
    window.show()
    sys.exit(app.exec_())