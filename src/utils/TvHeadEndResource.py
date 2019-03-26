import json
import requests
from src import parameters


class TvHeadEndResource():
    def find_and_delete_recordings(self, title, end_real=None, plot=None):
        """
        Asks TVHeadend for all recordings where title matches the current broadcasts title or
        current broadcasts plot matches a plot within recordings list.

        :param1 title: current broadcasts title
        :param2 end_real: current broadcasts end time
        :param3 plot: current broadcasts plot

        :return: None
        """
        if title == "":
            print('No title specified. Cannot delete recordings')
            return

        search_filter = [{
            "field": "disp_title",
            "type": "string",
            "value": title
        }]
        if end_real:
            search_filter.append({
                "field": "stop_real",
                "type": "numeric",
                "value": end_real,
                "comparison": "eq"
            })
        # # limitation: tvh doesn't filter by plot when the description contains [ or ]!!!!!
        # if plot:
        #     search_filter.append({
        #         "field": "disp_description",
        #         "type": "string",
        #         "value": plot
        #     })

        r = requests.get(parameters.TVHEADEND_URL + '/dvr/entry/grid?filter=' + json.dumps(search_filter))
        response = r.json()
        for entry in response['entries']:
            uuid = entry['uuid']
            if entry['disp_title'] != title:
                print("going too far, should only delete once. possible filter error")
            elif plot and plot != entry['disp_description']:
                print("good title, wrong plot")
            else:
                print("Deleting : ", title, uuid)
                r = requests.post(parameters.TVHEADEND_URL + '/dvr/entry/remove',
                                  data={"uuid": uuid})
