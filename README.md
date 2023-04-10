# OnSite_game
## 回放测试方法
回放测试方法是一种基于自然驾驶数据，重构现实背景交通参与者轨迹，利用仿真环境对现实场景进行再现，将待测智能汽车仿真模型置于回放环境中进行测试的方法。  

要使用回放测试工具，首先需要安装python第三方库：  
`pip install onsite`  
之后，在任意目录下新建文件夹（这里命名为replay_demo），replay_demo中包含两个文件夹inputs和planner。可从[OnSite官网](https://onsite.run/)下载任意OpenX格式的场景文件（这里以0027follow27场景为例），将0027follow27场景放于inputs文件夹下。
test_conf.py文件的作用是设置测试方法及可视化选择。

然后，在planner文件夹下编写__main__.py文件，这是规控器的主函数，也可作为onsite库与规控算法之间的接口。
需要注意的是，这里设置action = (1,0)，即仿真中每一步的本车加速度和转向角均为1m/s2和0°，用户在使用时可将自己开发的规控算法输入action。

直接在编译器中运行__main__.py，或在命令行中执行python planner，即可进行回放测试。测试完成后会在replay_demo目录下生成outputs文件夹，里面有输出文件0027follow27_exam.csv，这一文件包含了测试过程中本车和其他背景车辆的完整轨迹信息。
