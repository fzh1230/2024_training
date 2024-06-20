import pytest
import os
import time
import sys
import json
import threading
import subprocess
import mysql.connector


def insert_my_sql(sql_table, values):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ouJquVbg_4gR",
        database="test"
    )

    cursor = db.cursor()
    if sql_table:
        sql = "INSERT INTO testwork (total, passed, failed, skipped, pass_rate, log_position) VALUES (%s, %s, %s, %s, %s, %s)"
    else:
        sql = "INSERT INTO api_testwork (total, passed, failed, skipped, pass_rate, log_position) VALUES (%s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, values)

    db.commit()
    print(f"插入了 {cursor.rowcount} 条记录")

    cursor.close()
    db.close()


def get_allure_report_data(report_dir):
    summary_file = os.path.join(report_dir, 'html', 'widgets', 'summary.json')
    if not os.path.exists(summary_file):
        print(f"Summary file not found: {summary_file}")
        return 0, 0, 0, 0, 0.0

    with open(summary_file, 'r', encoding='utf-8') as f:
        summary = json.load(f)
        total = summary['statistic']['total']
        passed = summary['statistic']['passed']
        failed = summary['statistic']['failed']
        skipped = summary['statistic']['skipped']
        pass_rate = passed / total * 100 if total > 0 else 0.0
        return total, passed, failed, skipped, pass_rate


def run_search_tests(cur_path, search_report_path, search_html_report_path):
    # 运行百度搜索测试
    pytest.main(["-s", "-m", "baidu_search or test_demo",
                 f"{cur_path}\\TestCase\\baiduSearch.py::TestBaiduSearch", "--alluredir", search_report_path])
    if os.system(f"allure generate {search_report_path} -o {search_html_report_path} --clean") != 0:
        print("Allure 命令未找到，请确保 Allure 已正确安装并添加到系统 PATH 中。")
    else:
        total, passed, failed, skipped, pass_rate = get_allure_report_data(search_report_path)
        print(f"Total tests: {total}")
        print(f"Passed tests: {passed}")
        print(f"Failed tests: {failed}")
        print(f"Skipped tests: {skipped}")
        print(f"Pass rate: {pass_rate:.2f}%")
        values = (total, passed, failed, skipped, pass_rate, search_report_path)
        insert_my_sql(True, values)


def run_api_tests(cur_path, api_report_path, api_html_report_path):
    # 运行API测试
    pytest.main(["-s", "-m", "api_search or test_demo",
                 f"{cur_path}\\TestCase\\baiduApiSearch.py::TestBaiduSearch", "--alluredir", api_report_path])
    if os.system(f"allure generate {api_report_path} -o {api_html_report_path} --clean") != 0:
        print("Allure 命令未找到，请确保 Allure 已正确安装并添加到系统 PATH 中。")
    else:
        api_total, api_passed, api_failed, api_skipped, api_pass_rate = get_allure_report_data(api_report_path)
        print(f"--------------------API TEST----------------------")
        print(f"Total tests: {api_total}")
        print(f"Passed tests: {api_passed}")
        print(f"Failed tests: {api_failed}")
        print(f"Skipped tests: {api_skipped}")
        print(f"Pass rate: {api_pass_rate:.2f}%")
        values = (api_total, api_passed, api_failed, api_skipped, api_pass_rate, api_report_path)
        insert_my_sql(False, values)


def serve_report(report_path, port):
    try:
        process = subprocess.Popen(f"allure serve {report_path} -p {port}", shell=True)
        return process
    except Exception as e:
        print(f"Failed to serve report at {report_path} on port {port}: {e}")
        return None


if __name__ == '__main__':
    now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    cur_path = os.path.dirname(os.path.realpath(__file__))

    # 定义百度搜索测试报告路径
    search_report_path = os.path.join(cur_path, f'Report\\Search\\{now_time}')
    search_html_report_path = os.path.join(search_report_path, 'html')

    # 定义API测试报告路径
    api_now_time = "ApiBaiduTest\\" + now_time
    api_report_path = os.path.join(cur_path, f'Report\\{api_now_time}')
    api_html_report_path = os.path.join(api_report_path, 'html')

    try:
        # 启动多线程
        search_thread = threading.Thread(target=run_search_tests,
                                         args=(cur_path, search_report_path, search_html_report_path))
        api_thread = threading.Thread(target=run_api_tests, args=(cur_path, api_report_path, api_html_report_path))

        search_thread.start()
        api_thread.start()

        # 等待线程完成
        search_thread.join()
        api_thread.join()

    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        print(f"Error position: {e.start}")
        sys.exit(1)

    try:
        # 启动allure服务
        search_report_process = serve_report(search_report_path, 8023)
        api_report_process = serve_report(api_report_path, 8022)

        if search_report_process:
            print(f"百度搜索测试报告已在端口8037启动")

        if api_report_process:
            print(f"API测试报告已在端口8038启动")

    except UnicodeDecodeError as e:
        print(f"端口启动服务错误:{e}")

