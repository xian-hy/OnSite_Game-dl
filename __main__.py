from onsite import scenarioOrganizer, env
from idm import IDM
import time
import os
import matplotlib.pyplot as plt


def check_dir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


if __name__ == "__main__":
    # 指定输入输出文件夹位置
    input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/24545/Desktop/A_test'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/24545/Desktop/A_test/outputs'))

    # check dir
    check_dir(output_dir)
    # 记录测试时间，用于评估效率，没有特殊用途
    tic = time.time()
    # 实例化场景管理模块（ScenairoOrganizer）和场景测试模块（Env）
    so = scenarioOrganizer.ScenarioOrganizer()
    envi = env.Env()
    # 初始化IDM规控器
    planner = IDM()
    # 根据配置文件config.py装载场景，指定输入文件夹即可，会自动检索配置文件
    so.load(input_dir, output_dir)
    print(f"<测试参数>\n{so.config}")
    
    while True:
        # 使用场景管理模块给出下一个待测场景
        scenario_to_test = so.next()
        if scenario_to_test is None:
            break  # 如果场景管理模块给出None，意味着所有场景已测试完毕。
        print(f"<scene-{scenario_to_test['data']['scene_name']}>")
        # 如果场景管理模块不是None，则意味着还有场景需要测试，进行测试流程。
        # 使用env.make方法初始化当前测试场景，可通过visilize选择是否可视化，默认关闭
        observation, traj = envi.make(scenario=scenario_to_test)

        # 当测试还未进行完毕，即观察值中test_setting['end']还是-1的时候
        while observation['test_setting']['end'] == -1:
            action = planner.act(observation, traj)  # 规划控制模块做出决策，得到本车加速度和方向盘转角。
            observation = envi.step(action)  # 根据车辆的action，更新场景，并返回新的观测值。
        # 如果测试完毕，将测试结果传回场景管理模块（ScenarioOrganizer)
        so.add_result(scenario_to_test, observation['test_setting']['end'])
        # 在每一次测试最后都关闭可视化界面，避免同时存在多个可视化
        plt.close()
    toc = time.time()
    print(toc - tic)
