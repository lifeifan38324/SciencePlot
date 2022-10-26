# from matplotlib import font_manager  # 导入字体管理模块
from MyPlot import *

if __name__ == "__main__":
    # # 获取文件列表
    filepath = r"E:\OneDrive\OneDrive - mail.scut.edu.cn\课题组事务\数据测试\实验数据\新视界测试数据\220925"
    lst = Line()
    device_list = ["A1", "T1"]
    # write_files_to_excel(path=filepath)
    # lst.plot_all_IDVD(filepath, device_list, isSave=True)
    # lst.plot_all_IDVG(filepath, device_list, isSave=True)
    # lst.plot_all_CsdVd(filepath, device_list, isSave=True)
    lst.plot_all_CsgVg(filepath, device_list, isSave=True)
    # print('执行完成')
    pass

