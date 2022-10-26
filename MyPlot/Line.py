import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,FormatStrFormatter
import matplotlib.ticker as mtick


# 对应一个txt文件
class File:
    def __init__(self, absolute_path: str, date: str, device: str, curve_type: str, label: str, test_count: str):
        self.absolute_path = absolute_path
        self.date = date
        self.device = device
        self.curve_type = curve_type
        self.label = label
        self.test_count = test_count


# 对应一张图
class FigFile:
    def __init__(self, title=None, xaxis_name=None, yaxis_name=None, curve_list=None, *save_path):
        self.title = title
        self.xaxis_name = xaxis_name
        self.yaxis_name = yaxis_name
        self.curve_list = curve_list   # = [{"x_data":[], "y_data": [], "label": "label"}]
        self.save_path = save_path


class Line:
    COLOR = []
    LINE_STYLE = []
    MARK_STYLE = []

    def __init__(self):
        self.count = 0
        pass

    # 获取取所有匹配的文件名
    def find_all_file(self, filepath: str, reg: str) -> list[str]:
        """获取目录中所有匹配的文件的信息"""
        lst = os.listdir(filepath)
        file_list = []
        for file_name in lst:
            if re.match(reg, file_name):
                date = file_name[-23:-5]  # 获取测试时间
                ind = file_name.find("[")
                device = file_name[ind + 1:ind + 6]  # 获取器件名称
                test_count = file_name[ind + 7:ind + 8]  # 获取器件测试编号
                label = file_name.split(" ")[2]  # 获取label
                curve_type = file_name.split(" ")[0]
                full_name = filepath + "\\" + file_name  # 拼串成全路径
                file_list.append(
                    File(full_name, date, device, curve_type=curve_type, label=label, test_count=test_count))
        file_list.sort(key=lambda x: x.date, reverse=True)  # 按照时间排序
        for file in file_list:
            print(file.date, file.absolute_path)
        if len(file_list) != 0:
            print(f"为您匹配到{len(file_list)}个文件")
        return file_list

    # 利用index文件提取所有文件的文件名
    def find_all_file_from_xpath(self, filepath: str, reg: str):
        """利用html文件提取所有文件的信息"""
        from lxml import etree
        tree = etree.parse(filepath + r"\index.html")
        obj_list = tree.xpath('//a/@href')
        file_list = []
        for ele in obj_list:
            full_name = str(ele)
            ind = full_name.rfind("\\")
            new_name = full_name[ind + 1:]  # 文件的文件名 eg:Csg-Vg...2022_9_25 21_55_07].txt
            if re.match(reg, new_name):
                date = new_name[-23:-5]  # 获取测试时间
                ind2 = new_name.find("[")
                device = new_name[ind2 + 1:ind2 + 6]  # 获取器件名称
                test_count = new_name[ind + 7:ind + 8]  # 获取器件测试编号
                label = new_name.split(" ")[3]  # 获取label
                curve_type = new_name.split(" ")[0]
                full_name = filepath + "\\" + new_name
                file_list.append(
                    File(full_name, date, device, curve_type=curve_type, label=label, test_count=test_count))
        file_list.sort(key=lambda x: x.date, reverse=True)  # 按照时间排序
        for file in file_list:
            print(file.date, file.absolute_path)
        return file_list
        pass

    # 取出文件中的数据
    def get_data_of_file(self, file, cols):
        """从file中获取需要的x轴和y轴数据"""
        # frame：文件，字符串或产生器，可以是.gz或bz2压缩文件。
        # dtype：数据类型，可选。默认np.float。
        # delimiter：分隔字符串，默认是任何空格。
        # skiprows：跳过前n行。
        # usecols：读取指定的列。索引，元组类型。
        # unpack：如果是True，读入属性将扽别写入不同数组变量。False读入数据只写入一个数组变量。即数组的转置。 默认为False。
        data = np.loadtxt(file.absolute_path, dtype='float', skiprows=3, usecols=cols)
        x_data = list(data[:, 0])
        y_data = list(data[:, 1])
        data = {'x_data': x_data, 'y_data': y_data}
        return data

    def plot_line(self, data, label):
        plt.plot(data['x_data'], self.change_unit(data['y_data'], 12), label=label)

    def plot_mul_legend_line(self, file_list, axis_name, title):
        """绘制还有多个legend的图像"""
        # 设置通用的图形属性
        self.set_plot()
        # 不同图例的数据、标签不同，其他均相同
        for file in file_list:
            data = self.get_data_of_file(file, (0, 1))
            self.plot_line(data, file.label)

        # 图例在左上方
        plt.legend(loc='upper left')
        # 设置轴的名字
        plt.xlabel(axis_name[0], fontsize=25)
        plt.ylabel(axis_name[1], fontsize=25)
        # 设置刻度的样式
        # plt.xticks(fontsize=20)
        # plt.yticks(fontsize=20)
        # 设置标题标注和字体大小
        plt.title(title, fontsize=30)
        plt.show()

    def plot_fig_file(self, fig_file: FigFile, isSave=False):
        # 设置通用的图形属性
        self.set_plot()
        title = fig_file.title
        x_axis_name = fig_file.xaxis_name
        y_axis_name = fig_file.yaxis_name
        if y_axis_name.startswith("Id") & x_axis_name.startswith("Vg"):
            plt.yscale("log")
        for curve in fig_file.curve_list:
            if y_axis_name.startswith("Id") & x_axis_name.startswith("Vg"):
                curve['y_data'] = list(map(lambda x: x if x > 0 else -x, curve['y_data']))
            plt.plot(curve['x_data'], curve['y_data'], label=curve['label'])
        # 图例在左上方
        plt.legend(loc='upper left')
        if y_axis_name.startswith("C"):
            plt.legend(loc='best')
        # 设置轴的名字
        plt.xlabel(x_axis_name, fontsize=25)
        plt.ylabel(y_axis_name, fontsize=25, )
        # 设置刻度的样式
        # plt.xticks(fontsize=20)
        # plt.yticks(fontsize=20)
        # 设置标题标注和字体大小
        plt.title(title, fontsize=30)
        if isSave:
            plt.savefig(fig_file.save_path, dpi=200)  # dpi     分辨率
            self.count += 1
            print(f"第\t{self.count}个已保存", fig_file.save_path)
        plt.show()
        pass

    def change_unit(self, data_list, num):  # 全部数据*10^num
        """修改数据的数量级"""
        return list(map(lambda x: x * 10 ** num, data_list))

    def set_plot(self):
        """设置绘图的全局样式"""
        # 图片格式设置
        # 图片大小为10*8，每英寸100个像素点
        plt.figure(figsize=(10, 8), dpi=100)  # 设置图片大小，一般默认不设置
        plt.rcParams['savefig.dpi'] = 200  # 图片像素

        # plt.grid(True)  # 绘制网格
        plt.rcParams.update({"font.size": 20})  # 此处必须添加此句代码方可改变标题字体大小
        plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

        # 设置xtick和ytick的方向：in、out、inout
        plt.rcParams.update({'xtick.direction': 'in'})
        plt.rcParams['ytick.direction'] = 'in'
        plt.tick_params(top='in', right='in', which='both')
        # plt.plot()实际上会通过plt.gca()获得当前的Axes对象ax，然后再调用ax.plot()方法实现真正的绘图
        ax = plt.gca()
        # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
        ax.spines['bottom'].set_linewidth(1);  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(1);  ####设置左边坐标轴的粗细
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    def show_all_font(self):
        """显示所有可用的字体"""
        from matplotlib import font_manager
        for font in font_manager.fontManager.ttflist:
            # 查看字体名以及对应的字体文件名
            print(font.name, '-', font.fname)

    def plot_Csd_Vd(self, file_list, title="Csd_Vd曲线图", isSave=False):
        """生成Csd_Vd的fig_file对象并绘图"""
        fig_file = FigFile()
        fig_file.title = title + f" ---器件{file_list[0].device}-{file_list[0].test_count}"  # 设置fig_file的title
        path = file_list[0].absolute_path[:file_list[0].absolute_path.rfind('\\')] + "\\处理结果\\" + file_list[0].device
        if os.path.exists(path) == False:
            os.mkdir(path)
        fig_file.save_path = path + "\\" + fig_file.title + ".png"
        fig_file.xaxis_name = "Vd/V"  # 设置fig_file的坐标轴名字
        fig_file.yaxis_name = "Csd/F"
        fig_file.curve_list = []
        for file in file_list:
            one_cruve = {}
            data = self.get_data_of_file(file, (0, 1))
            one_cruve['x_data'] = data['x_data']
            one_cruve['y_data'] = data['y_data']
            one_cruve['label'] = file.label
            fig_file.curve_list.append(one_cruve)
        self.plot_fig_file(fig_file, isSave)
        pass

    def plot_all_CsdVd(self, filepath, device_list, isSave=False):
        """一键生成所有该路径下的对应器件的Csd-Vd曲线图"""
        for device in device_list:
            for i in range(1, 10):
                for test_count in range(1, 10):
                    reg = r"Csd-Vd.*Vg=\d.*\[" + device + r"\(" + str(i) + r"\)\(" + str(test_count) + r".*.txt"
                    file_list = self.find_all_file(filepath, reg)
                    if len(file_list) > 0:
                        self.plot_Csd_Vd(file_list, isSave=isSave)
        pass

    def plot_Csg_Vg(self, file_list, title="Csg_Vg曲线图", isSave=False):
        """生成Csg_Vg的fig_file对象并绘图"""
        fig_file = FigFile()
        fig_file.title = title + f" ---器件{file_list[0].device}-{file_list[0].test_count}"  # 设置fig_file的title
        path = file_list[0].absolute_path[:file_list[0].absolute_path.rfind('\\')] + "\\处理结果\\" + file_list[0].device
        if os.path.exists(path) == False:
            os.mkdir(path)
        fig_file.save_path = path + "\\" + fig_file.title + ".png"
        fig_file.xaxis_name = "Vg/V"  # 设置fig_file的坐标轴名字
        fig_file.yaxis_name = "Csg/F"
        fig_file.curve_list = []
        for file in file_list:
            one_cruve = {}
            data = self.get_data_of_file(file, (0, 1))
            one_cruve['x_data'] = data['x_data']
            one_cruve['y_data'] = data['y_data']
            one_cruve['label'] = file.label
            fig_file.curve_list.append(one_cruve)
        self.plot_fig_file(fig_file, isSave)
        pass

    def plot_all_CsgVg(self, filepath, device_list, isSave=False):
        """一键生成所有该路径下的对应器件的Csg-Vg曲线图"""
        self.count = 0
        for device in device_list:
            for i in range(1, 10):
                for test_count in range(1,10):
                    reg = r"Csg-Vg.*Vd=.*\[" + device + r"\(" + str(i) + r"\)\(" + str(test_count) + r".*.txt"
                    file_list = self.find_all_file(filepath, reg)
                    if len(file_list) > 0:
                        self.plot_Csg_Vg(file_list, isSave=isSave)
                    pass

    def plot_IDVG(self, file, title="IDVG曲线图", isSave=False):
        """生成IDVG的fig_file对象并绘图"""
        data = self.get_data_of_file(file, (0, 1))
        fig_file = FigFile()
        fig_file.title = title + f" ---器件{file.device}-{file.test_count}"  # 设置fig_file的title
        path = file.absolute_path[:file.absolute_path.rfind('\\')] + "\\处理结果\\" + file.device
        if os.path.exists(path) == False:
            os.mkdir(path)
        fig_file.save_path = path + "\\" + fig_file.title + ".png"
        fig_file.xaxis_name = "Vg/V"        # 设置fig_file的坐标轴名字
        fig_file.yaxis_name = "Id/A"
        fig_file.curve_list = []
        length = int(len(data['x_data']) / 6)
        for i in range(6):
            one_cruve = {}
            one_cruve['x_data'] = data['x_data'][length * i: length * (i + 1)]
            one_cruve['y_data'] = data['y_data'][length * i: length * (i + 1)]
            one_cruve['label'] = 'Vd=' + str(2 * i + 0.1) + 'V'
            fig_file.curve_list.insert(0, one_cruve)
        self.plot_fig_file(fig_file, isSave)
        pass

    def plot_all_IDVG(self, filepath, device_list=None, isSave=False):
        """一键生成所有该路径下的对应器件的Csg-Vg曲线图"""
        reg = r"IDVG.*.txt"
        file_list = self.find_all_file(filepath, reg)
        for file in file_list:
            self.plot_IDVG(file, isSave=isSave)
        pass

    def plot_IDVD(self, file, title="IDVD曲线图", isSave=False):
        """生成IDVD的fig_file对象并绘图"""
        data = self.get_data_of_file(file, (0, 1))
        fig_file = FigFile()
        fig_file.title = title + f" ---器件{file.device}-{file.test_count}"  # 设置fig_file的title
        path = file.absolute_path[:file.absolute_path.rfind('\\')] + "\\处理结果\\" + file.device
        if os.path.exists(path) == False:
            os.mkdir(path)
        fig_file.save_path = path + "\\" + fig_file.title + ".png"
        fig_file.xaxis_name = "Vd/V"        # 设置fig_file的坐标轴名字
        fig_file.yaxis_name = "Id/A"
        fig_file.curve_list = []
        length = int(len(data['x_data']) / 6)
        for i in range(6):
            one_cruve = {}
            one_cruve['x_data'] = data['x_data'][length * i: length * (i + 1)]
            one_cruve['y_data'] = data['y_data'][length * i: length * (i + 1)]
            one_cruve['label'] = 'Vg=' + str(2 * i + 2) + 'V'
            fig_file.curve_list.insert(0, one_cruve)
        self.plot_fig_file(fig_file, isSave)
        pass

    def plot_all_IDVD(self, filepath, device_list=None, isSave=False):
        """一键生成所有该路径下的对应器件的Csg-Vg曲线图"""
        reg = r"IDVD.*.txt"
        file_list = self.find_all_file(filepath, reg)
        for file in file_list:
            self.plot_IDVD(file, isSave=isSave)
        pass





if __name__ == "__main__":
    # # 获取文件列表
    filepath = r"C:\Users\LFF\Desktop\220925"
    # reg = r"Csg-Vg.*Vd=.*\[T1\(5\)\(3.*.txt"
    lst = Line()
    file_list = lst.plot_all_CsgVg(filepath, ["A1", "T1"])
    # lst.plot_Csg_Vg(file_list)

    print('执行完成')
    pass

