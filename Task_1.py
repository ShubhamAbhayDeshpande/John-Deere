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
        mdc_mdc_contenttype = item["mdc.ContentType"]
        mdc_mdc_sessionguide = item["mdc.SessionGuid"]
        message_timestamp = item["@message"]["timestamp"]
        message_sequence = item["@message"]["sequence"]
        message_logger_class = item["@message"]["loggerClassName"]
        message_logger_name = item["@message"]["loggerName"]
        message_level = item["@message"]["level"]
        message_message = item["@message"]["message"]
        message_thread_name = item["@message"]["threadName"]
        message_thread_id = item["@message"]["threadId"]
        mdc_sessionguide = item["@message"]["mdc"]["SessionGuid"]
        mdc_orgid = item["@message"]["mdc"]["OrgId"]
        mdc_awsrequest = item["@message"]["mdc"]["AwsRequestId"]
        mdc_jobsiteid = item["@message"]["mdc"]["JobsiteId"]
        mdc_eventid = item["@message"]["mdc"]["EventID"]
        mdc_machineid = item["@message"]["mdc"]["MachineId"]
        mdc_sequencenumber = item["@message"]["mdc"]["SequenceNumber"]
        mdc_contenttype = item["@message"]["mdc"]["ContentType"]
        mdc_frequency = item["@message"]["mdc"]["frequency"]
        ndc = item["@message"]["ndc"]
        host_name = item["@message"]["hostName"]
        process_name = item["@message"]["processName"]
        process_id = item["@message"]["processId"]

        records.append([date_time, mdc_mdc_contenttype, mdc_mdc_sessionguide, message_timestamp,
                        message_sequence, message_logger_class, message_logger_name, message_level,
                        message_message, message_thread_name, message_thread_id, mdc_sessionguide,
                        mdc_orgid, mdc_awsrequest, mdc_jobsiteid, mdc_eventid, mdc_machineid,
                        mdc_sequencenumber, mdc_contenttype, mdc_frequency, ndc, host_name,
                        process_name, process_id])

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
    column_names = ['Date/Time', 'mdc.ContentType', 'mdc.SessionGuid', '@message.timestamp',
                         '@message.sequence', '@message.loggerClassName', '@message.loggerName',
                         '@message.level', '@message.message', '@message.threadName',
                         '@message.threadId', '@message.mdc.SessionGuid', '@message.mdc.OrgId',
                         '@message.mdc.AwsRequestId', '@message.mdc.JobsiteId',
                         '@message.mdc.EventId', '@message.mdc.MachineId',
                         '@message.mdc.SequenceNumber', '@message.mdc.ContentType',
                         '@message.mdc.frequency', '@message.ndc', '@message.hostName',
                         '@message.processName', '@message.processId']

    data = []
    for nested_values in records:
        data_row = {col: value for col, value in zip(column_names, nested_values)}
        data.append(data_row)

    with open(csv_file, 'w', newline='') as file:
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
