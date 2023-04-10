# OnSite_game
## 回放测试方法
回放测试方法是一种基于自然驾驶数据，重构现实背景交通参与者轨迹，利用仿真环境对现实场景进行再现，将待测智能汽车仿真模型置于回放环境中进行测试的方法。  

要使用回放测试工具，首先需要安装python第三方库：  
`pip install onsite`  

之后，在任意目录下新建文件夹（这里命名为replay_demo），replay_demo中包含两个文件夹inputs和planner。可从[OnSite官网](https://onsite.run/)下载任意OpenX格式的场景文件（这里以0027follow27场景为例），将0027follow27场景放于inputs文件夹下,同时编写test_conf.py文件如下：  
`config = {  
        'test_settings': {  
            'mode': 'replay',   # 设置测试方法，replay表示回放测试  
            'visualize': False,  # 设置测试过程可视化，True表示开启，False表示关闭  
        },  
}`  
test_conf.py文件的作用是设置测试方法及可视化选择。

然后，在planner文件夹下编写__main__.py文件，这是规控器的主函数，也可作为onsite库与规控算法之间的接口。__main__.py中代码编写如下：
`from onsite import scenarioOrganizer, env`
`import os`

`def check_dir(target_dir):`
    `if not os.path.exists(target_dir):`
        `os.makedirs(target_dir)`

`if __name__ == "__main__":`
    `# 指定输入输出文件夹位置`
    `input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../inputs'))`
    `output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../outputs'))`

    # 检查输出路径
    check_dir(output_dir)
    # 实例化场景管理模块（ScenairoOrganizer）和场景测试模块（Env）
    so = scenarioOrganizer.ScenarioOrganizer()
    envi = env.Env()
    # 根据配置文件config.py装载场景，指定输入文件夹即可，会自动检索配置文件
    so.load(input_dir, output_dir)

    while True:
        # 使用场景管理模块给出下一个待测场景
        scenario_to_test = so.next()
        if scenario_to_test is None:
            break  # 如果场景管理模块给出None，意味着所有场景已测试完毕。
        # 如果场景管理模块不是None，则意味着还有场景需要测试，进行测试流程。
        # 使用env.make方法初始化当前测试场景
        observation, traj = envi.make(scenario=scenario_to_test)
        # 当测试还未进行完毕，即观察值中test_setting['end']还是-1的时候
        while observation['test_setting']['end'] == -1:
            action = (1,0)  # 规划控制模块做出决策，这里设定加速度为1，转向角为0。
            observation = envi.step(action)  # 根据车辆的action，更新场景，并返回新的观测值。
        # 如果测试完毕，将测试结果传回场景管理模块（ScenarioOrganizer)
        so.add_result(scenario_to_test, observation['test_setting']['end'])`
        
需要注意的是，这里设置action = (1,0)，即仿真中每一步的本车加速度和转向角均为1m/s2和0°，用户在使用时可将自己开发的规控算法输入action。  
文件架构如下：  
`REPLAY_DEMO  
    ├── inputs  
    │   └── 0027follow27  
    │      ├── 0027follow27_exam.xosc  
    │      ├── highD_2.xodr  
    │      └── test_conf.py  
    ├── planner  
    │   └── _main_.py`  

直接在编译器中运行__main__.py，或在命令行中执行python planner，即可进行回放测试。测试完成后会在replay_demo目录下生成outputs文件夹，里面有输出文件0027follow27_exam.csv，这一文件包含了测试过程中本车和其他背景车辆的完整轨迹信息。
