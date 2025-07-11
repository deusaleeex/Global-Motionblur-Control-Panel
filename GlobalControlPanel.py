import nuke
import nukescripts
from rotoMB import RotoClass
from scanlineMB import ScanlineClass
from transformMB import TransformClass

class ControlPanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Global Control Panel', 'NukePanel.GBCP')
        # Title and description
        self.title = nuke.Text_Knob('title', '')
        self.title.setValue('<h1> Global Motion Blur Controls v1.0</h1>')
        self.addKnob(self.title)

        self.description = nuke.Text_Knob('description', '')
        self.description.setValue('<b>Adjust <i>motion blur</i> settings of relevant nodes across the entire script.</b>')
        self.addKnob(self.description)
    
        self.addDivider()

        # Create instance of RotoClass
        self.roto_instance = RotoClass()
        self.scanline_instance = ScanlineClass()
        self.transform_instance = TransformClass()

        # Add imported knobs to the panel
        self.roto_instance.create_roto_knobs(self)

        self.addDivider()

        self.scanline_instance.create_scanline_knobs(self)

        self.addDivider()

        self.transform_instance.create_transform_knobs(self)

        self.addDivider()

    def addDivider(self):
        self.div = nuke.Text_Knob('divider', '')
        self.addKnob(self.div)
        self.div.setFlag(nuke.STARTLINE)

    def knobChanged(self, knob):
        # Check if the changed knob belongs to the instanced modules
        if knob in self.roto_instance.roto_knobs:
            self.roto_instance.knobChanged(knob)
        elif knob in self.scanline_instance.scanline_knobs:
            self.scanline_instance.knobChanged(knob)
        elif knob in self.transform_instance.transform_knobs:
            self.transform_instance.knobChanged(knob)
