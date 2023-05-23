"""
    Task one from the list of tasks

    : author:
        - Shubham Abhay Deshpande <dsa14071996@gmail.com>

"""

import json
import csv
import logging
import argparse
import os
import re


def make_csv(file: str, csv_file_location: str) -> None:
    """
    Function for reading the json file from given location

    :param file: path to the json file
    :param csv_file_location: The location where csv file will be saved

    """
    with open(file, 'r') as f:
        read_file = json.load(f)

    # Extract information from json file
    records = []

    for idx, item in enumerate(read_file):
        date_time = item["@timestamp"]
        mdc_mdc_sessionguide = item["mdc.SessionGuid"]
        message_message = item["@message"]["message"]
        mdc_machineid = item["@message"]["mdc"]["MachineId"]

        match = re.findall(r"sites/([\w-]+)|sites", message_message)
        job_site_id = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"machines/([\w-]+)|machines", message_message)
        machine_id = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalEngineOperatingTime/([\w-]+)|vrTotalEngineOperatingTime",
                          message_message)
        engine_operating_time = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledWeight/([\w-]+)|vrTotalMilledWeight", message_message)
        milled_weight = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledDistance/([\w-]+)|vrTotalMilledDistance", message_message)
        milled_distance = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledArea/([\w-]+)|vrTotalMilledArea", message_message)
        milled_area = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledDifficultyDistance/([\w-]+)|vrTotalMilledDifficultyDistance",
                          message_message)
        milled_difficulty_distance = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrvrTotalMilledRefinishArea/([\w-]+)|vrTotalMilledRefinishArea",
                          message_message)
        milled_re_finish_area = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalWaterConsumption/([\w-]+)|vrTotalWaterConsumption",
                          message_message)
        total_water_comsumption = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledVolume/([\w-]+)|vrTotalMilledVolume", message_message)
        milled_volume = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalJobDuration/([\w-]+)|vrTotalJobDuration", message_message)
        total_job_duration = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledAdditionalArea/([\w-]+)|vrTotalMilledAdditionalArea",
                          message_message)
        milled_additional_area = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"vrTotalMilledDuration/([\w-]+)|vrTotalMilledDuration", message_message)
        total_milled_duration = [matches if matches != '' else 0 for matches in match]

        match = re.findall(r"productivityTotalStartValues/([\w-]+)|productivityTotalStartValues",
                          message_message)
        start_values = [match if match != '' else 'x' for match in match]

        records.append([date_time, mdc_mdc_sessionguide, job_site_id[0], machine_id[0],
                        engine_operating_time[0], milled_weight[0], milled_distance[0],
                        milled_area[0], milled_difficulty_distance[0], milled_re_finish_area[0],
                        total_water_comsumption[0], milled_volume[0], total_job_duration[0],
                        milled_additional_area[0], total_milled_duration[0], start_values[0],
                        total_job_duration[1], milled_difficulty_distance[1],
                        total_milled_duration[0], total_water_comsumption[1],
                        milled_weight[1], milled_re_finish_area[1], milled_distance[1],
                        milled_additional_area[1],  engine_operating_time[1], milled_volume[1],
                        milled_area[1]])

        # Extracting machine id, date, start time and end time to make file name

        if idx == 0:
            mcid = mdc_machineid
            time_stamp = date_time.split(" ")
            date = time_stamp[0].replace("-", "")
            start_time = time_stamp[1].split(".")[0].replace(":", "")[:-2]

        if idx == len(read_file) - 1:
            end_time = date_time.split(" ")[1].split(".")[0].replace(":", "")[:-2]

    file_name = mcid + '_' + date + '_' + start_time + '_' + end_time + '_' + '.csv'

    csv_file = os.path.join(csv_file_location, file_name)
   
    column_names = ['Date/Time', 'SessionId', 'JobsiteId', 'MachineId',
                         'vrTotalEngineOperatingTime', 'vrTotalMilledWeight', 'vrTotalMilledDistance',
                         'vrTotalMilledArea', 'vrTotalMilledDifficultyDistance', 'vrTotalMilledRefinishArea',
                         'vrTotalWaterConsumption', 'vrTotalMilledVolume', 'vrTotalJobDuration',
                         'vrTotalMilledAdditionalArea', 'vrTotalMilledDuration',
                         'StartValues', 'vrTotalJobDuration',
                         'vrTotalMilledDifficultyDistance', 'vrTotalMilledDuration',
                         'vrTotalWaterConsumption', 'vrTotalMilledWeight', 'vrTotalMilledRefinishArea',
                         'vrTotalMilledDistance', 'vrTotalMilledAdditionalArea', 'vrTotalEngineOperatingTime',
                        'vrTotalMilledVolume', 'vrTotalMilledArea']

    data = []
    for nested_values in records:
        data_row = {col: value for col, value in zip(column_names, nested_values)}
        data.append(data_row)

    with open('new_csv.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--destination', type=str, required=False, default=None,
                        help='Destination where the csv file is stored')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s::%(message)s')

    logging.info('Reading json file')

    if args.destination is not None:
        if not os.path.isdir(args.destination):
            raise FileNotFoundError("The given destination does not exist. Please check provided "
                                    "path for destination")
        else:
            csv_location = args.destination
    else:
        csv_location = r".\\"

    logging.info("Making csv file.")

    make_csv(r".\\input.json", csv_location)

    logging.info("Done making csv file. Check file location.")
