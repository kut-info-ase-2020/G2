import calWBGT

if __name__ == '__main__':
    #setup()
    try:
        print("危なかったら１、危なくなかったら０、故障していたらー１が返ってくるはずです!")
        print("データは「dataWBGT.csv」に入っています!")
        print(calWBGT.calWBGT())
    except KeyboardInterrupt:
        destroy()
        #print("tyuusi")
