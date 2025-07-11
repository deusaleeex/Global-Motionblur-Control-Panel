from GlobalControlPanel import ControlPanel

def addGBPanel():
    global GBPanel
    GBPanel = ControlPanel()
    return GBPanel.addToPane()

paneMenu = nuke.menu('Pane')
paneMenu.addCommand('Global Control Panel', addGBPanel)
nukescripts.registerPanel('NukePanel.GBCP', addGBPanel)
