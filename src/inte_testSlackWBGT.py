# -*- coding: utf-8 -*-
import calWBGT
from SlackAPI.SlackAPI_class import SlackAPI

if __name__ == '__main__':
    #setup()
    try:
        print("危なかったら１、危なくなかったら０、故障していたらー１が返ってくるはずです!")
        print("データは「dataWBGT.csv」に入っています!")
        print(calWBGT.calWBGT())
        api = SlackAPI_class.SlackAPI(
            token=os.environ['SLACK_API_TOKEN'], 
            channels = '#zikkenzyou_go'
            )
        api.Visualization_HeatStroke(path='dataWBGT.csv')
    except KeyboardInterrupt:
        destroy()
        #print("tyuusi")
