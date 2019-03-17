import json
import requests
from src import parameters


def find_and_delete_recordings(title, end_real=None, plot=None):
    if title == "":
        print('No title specified. Cannot delete recordings')
        return

    search_filter = '''[
                {
                    "field" : "disp_title",
                    "type"  : "string",
                    "value" : "''' + title + '''"
                 }'''
    if end_real:
        search_filter += ''',{
                    "field" : "stop_real",
                    "type"  : "numeric",
                    "value" : ''' + str(end_real) + ''',
                    "comparison"  : "eq"
                 }
                '''
    # limition: tvh doesn't filter by plot when the descriptipn contains [ or ]!!!!!
    # if plot:
    #     search_filter += ''',{
    #                 "field" : "disp_description",
    #                 "type"  : "string",
    #                 "value" : "''' + plot + '''"
    #              }
    #             '''
    search_filter += ']'

    print(search_filter)
    r = requests.get(parameters.TVHEADEND_URL + '/dvr/entry/grid?filter=' + search_filter)
    response = r.json()
    print(r.text)
    for entry in response['entries']:
        uuid = entry['uuid']
        if entry['disp_title'] != title:
            print("going too far, should only delete once. possible filter error")
        elif plot and plot != entry['disp_description']:
            print("good title, wrong plot")
        else:
            print("deleting : ", title, uuid)
            r = requests.post(parameters.TVHEADEND_URL + '/dvr/entry/remove',
                          data={"uuid": uuid})
            print(r.status_code, r.text)