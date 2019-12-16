"""
Module to put all pytest hooks for various
"""
import os
import json


def pytest_json_modifyreport(json_report):
    """
    * The function is called by pytest-json-report plugin to only output warnings in json format.
    * Everything else is removed due to it already being saved by junitxml
    * --json-omit flag in does not allow us to remove everything but the warnings
    * (the environment metadata is one example of unremoveable data)
    * The json warning outputs are meant to be read by jenkins
    """
    warnings_flag = "warnings"
    if warnings_flag in json_report:
        warnings = json_report[warnings_flag]
        json_report.clear()
        json_report[warnings_flag] = warnings
    else:
        json_report = {}
    return json_report


def create_file_name(dir_path, file_name_postfix, num=0):
    """
    Used to create file name with this given
    structure: TEST_SUITE + "_" + file_name_postfile + "_ " + num.json
    The env variable TEST_SUITE is set in jenkinsfile

    This was necessary cause Pytest is run multiple times and we need to make sure old pytest
    warning json files are not being overwritten.
    """
    name = dir_path + "/"
    if "TEST_SUITE" in os.environ:
        name = name + os.environ["TEST_SUITE"] + "_"
    name = name + file_name_postfix
    if num != 0:
        name = name + "_" + str(num)
    return name + ".json"


def pytest_sessionfinish(session):
    """
    Since multiple pytests are running,
    this makes sure warnings from different run are not overwritten
    """
    dir_path = "test_root/log"
    file_name_postfix = "pytest_warnings"
    num = 0
    # to make sure this doesn't loop forever, putting a maximum
    while (
        os.path.isfile(create_file_name(dir_path, file_name_postfix, num)) and num < 100
    ):
        num += 1

    report = session.config._json_report.report

    with open(create_file_name(dir_path, file_name_postfix, num), "w") as outfile:
        json.dump(report, outfile)
