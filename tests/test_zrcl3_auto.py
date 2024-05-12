
from time import sleep
from zrcl4.logging import basic_debug

def test_memorized_auto():
    from zrcl3_uses.file import startApp
    from zrcl4.screeninfo import wnd_to_primary
    import zrcl4.pygetwindow as gwe
    import zrcl3_uses.automation as automation
    import pyautogui as pg
    basic_debug()
    startApp("notepad")
    sleep(2)
    wnd = gwe.get_visible_process_wnds("Notepad")
    assert wnd
    wnd = wnd[0]
    wnd_to_primary(wnd)
    
    sleep(1)
    
    token = automation.AutoToken(
        image="tests/image.png",
        wnd=wnd,
    )
    #token.screenshot().show()
    res = automation.waitFor(token)
    pg.moveTo(*res)
    sleep(2)
    wnd.moveRel(200, 30)
    print(res)
    print(token.interestedRegion)

    sleep(2)
    ftoken = automation.FrozenToken(token)
    
    pg.moveTo(*ftoken.normalizedResult)
    print(ftoken.normalizedResult)
    print(ftoken.interestedRegion)

    wnd.close()