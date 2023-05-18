"""
    Task two from the list of tasks

    : author:
        - Shubham Abhay Deshpande <dsa14071996@gmail.com>

"""

import json
import logging
import re

if __name__ == "__main__":

    logging.basicConfig(filemode='a', level=logging.INFO, format='Task_2::%(message)s')

    with open(r".\\input.json", 'r') as f:
        read_file = json.load(f)

    session_id_lst = []
    time_lst = {}

    # Read json file
    for item in read_file:
        mdc_mdc_sessionguide = item["mdc.SessionGuid"]
        # Append all session ids to a list and find all unique ids
        session_id_lst.append(mdc_mdc_sessionguide)

    unique_session_ids = list(set(session_id_lst))

    for session in unique_session_ids:
        time_lst[str(session)] = []
        for item in read_file:
            if re.search(str(session), item["mdc.SessionGuid"]):
                time_lst[str(session)].append(item["@timestamp"])

    logging.info(f" SessionID: {unique_session_ids[0]} "
                 f"\nStart time: {time_lst[unique_session_ids[0]][0]} "
                 f"\nEnd time: {time_lst[unique_session_ids[0]][-1]} "
                 f"\n# of frames: {len(time_lst[unique_session_ids[0]])}"
                 f"\n"
                 f"\nSessionID: {unique_session_ids[1]}"
                 f"\nStart time: {time_lst[unique_session_ids[1]][0]} "
                 f"\nEnd time: {time_lst[unique_session_ids[1]][-1]} "
                 f"\n# of frames: {len(time_lst[unique_session_ids[1]])}"
                 )
