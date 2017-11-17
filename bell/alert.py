
def beep(frequency, duration):
    try:
        import winsound
    except ImportError:
        import os
        def playsound(fr,dr):
            os.system('modprobe pcspkr')
            os.system('beep -f %s -l %s' % (fr,dr))
        playsound(frequency, duration)
    else:
        def playsound(frequency,duration):
            winsound.Beep(frequency,duration)
