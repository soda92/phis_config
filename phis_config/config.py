"""
程序配置文件解析
"""

from pathlib import Path
import logging


def env_write(file_path, line_number, content):
    # 读取文件并将其内容存储到列表中
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 修改指定行的内容（注意列表是从0开始索引的）
    if 1 <= line_number <= len(lines):
        lines[line_number - 1] = content + '\n'
    elif line_number > len(lines):
        # 如果指定的行数超出了文件的总行数，将在末尾添加新行
        lines.extend(['\n'] * (line_number - len(lines) - 1))
        lines.append(content + '\n')

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def get_line_option(env_file: Path, line_number: int) -> str:
    "获取配置文件中第N行数据的值 (格式: KEY:VALUE)"
    config_content = env_file.read_text(encoding='utf8').split('\n')
    line_number_in_file = line_number - 1  # 实际行数从0开始
    if line_number_in_file < 0 or line_number_in_file >= len(config_content):
        logging.fatal('配置文件行数错误！', line_number)
    return config_content[line_number_in_file].replace('：', ':').split(':')[1].strip()


class ProgramConfig:
    """
    程序配置文件解析
    """

    def __init__(self, path):
        self.env_file = Path(path)
        if not self.env_file.exists():
            logging.fatal(f'文件不存在，请检查文件路径是否正确. {self.env_file}')

    def get_raw_string(self, line_number: int) -> str:
        "获取配置文件中第N行数据, 原字符串"
        self.config_content = self.env_file.read_text(encoding='utf8').split('\n')
        line_number_in_file = line_number - 1  # 实际行数从0开始
        return self.config_content[line_number_in_file].strip()

    @property
    def 已完成数量(self):
        return get_line_option(self.env_file, 3)

    @property
    def 机构名称(self):
        return get_line_option(self.env_file, 5)

    @property
    def continue_save_if_already_done_test(self):
        "本季度已做过慢病随访，是否继续保存"
        return get_line_option(self.env_file, 6)

    @property
    def 无糖尿病是否录入空腹血糖(self):
        return get_line_option(self.env_file, 7)

    @property
    def 引入用药起始时间(self):
        return get_line_option(self.env_file, 8)

    @property
    def 引入用药结束时间(self):
        return get_line_option(self.env_file, 9)


def get_raw_string(env_file, line_number: int) -> str:
    "获取配置文件中第N行数据, 原字符串"
    config_content = env_file.read_text(encoding='utf8').split('\n')
    line_number_in_file = line_number - 1  # 实际行数从0开始
    return config_content[line_number_in_file].strip()


class AdminConfig1:
    def __init__(self, path):
        self.env_file = Path(path)
        if not self.env_file.exists():
            logging.fatal(f'文件不存在，请检查文件路径是否正确. {self.env_file}')

    @property
    def 随访新建起始时间(self):
        return get_line_option(self.env_file, 5)

    @property
    def 随访新建结束时间(self):
        return get_line_option(self.env_file, 6)

    @property
    def 登录网址(self):
        return get_raw_string(self.env_file, 1)

    @property
    def 登录用户名(self):
        return get_raw_string(self.env_file, 2)

    @property
    def 登录密码(self):
        return get_raw_string(self.env_file, 3)

    @property
    def 登录科室名称(self):
        return get_raw_string(self.env_file, 4)


Config = ProgramConfig('执行结果/env.txt')
"""执行结果配置"""

AdminConfig = AdminConfig1('文档/admin.txt')
"""Admin配置 （随访新建起始时间，随访新建结束时间）"""


def 重置已完成数量():
    env_write('执行结果/env.txt', 3, f'已完成数量:0')
