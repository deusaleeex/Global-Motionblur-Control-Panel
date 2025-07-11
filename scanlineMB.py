import nuke

class ScanlineClass:
    def __init__(self):

        self.scanline_knobs = []  # This will store all the Scanline knobs
        
        # Scanline control knobs
        self.title = nuke.Text_Knob('heading', '')
        self.title.setValue('<h2>Scanline Renders  </h2>')
        self.scanline_knobs.append(self.title)
        
        # Scanline Renders controls
        self.include_scanline = nuke.Boolean_Knob('include', 'enable')
        self.scanline_knobs.append(self.include_scanline)

        self.selected_scanline = nuke.Boolean_Knob('selected_scanline', 'apply to selected only')
        self.selected_scanline.setEnabled(False)
        self.scanline_knobs.append(self.selected_scanline)

        self.scanline_samples_amount = nuke.Double_Knob('scanline_amount', 'samples')
        self.scanline_samples_amount.setRange(1, 50)
        self.scanline_samples_amount.setValue(1)
        self.scanline_samples_amount.setEnabled(False)
        self.scanline_knobs.append(self.scanline_samples_amount)

        self.scanline_shutter = nuke.Double_Knob('scanline_shutter', 'shutter')
        self.scanline_shutter.setRange(0, 2)
        self.scanline_shutter.setValue(0.5)
        self.scanline_shutter.setEnabled(False)
        self.scanline_knobs.append(self.scanline_shutter)

        self.scanline_shutter_offset = nuke.Enumeration_Knob('scanline_offset', 'shutter offset', ['start', 'centered', 'end', 'custom'])
        self.scanline_shutter_offset.setValue('start')
        self.scanline_shutter_offset.setEnabled(False)
        self.scanline_knobs.append(self.scanline_shutter_offset)

        self.scanline_shutter_offset_amount = nuke.Double_Knob('scanline_offset_amount', '')
        self.scanline_shutter_offset_amount.setRange(-1, 1)
        self.scanline_shutter_offset_amount.setValue(0)
        self.scanline_shutter_offset_amount.setEnabled(False)
        self.scanline_shutter_offset_amount.clearFlag(nuke.STARTLINE)
        self.scanline_knobs.append(self.scanline_shutter_offset_amount)
    
    def create_scanline_knobs(self, panel_instance):      
        # Add Scanline knobs to the panel_instance
        for knob in self.scanline_knobs:
            panel_instance.addKnob(knob)

    def knobChanged(self, knob):
        # Handle changes in the UI
        enable_scanline_controls = {self.include_scanline}
        relevant_scanline_knobs = {self.scanline_samples_amount, self.scanline_shutter, self.scanline_shutter_offset, self.scanline_shutter_offset_amount}
        enable_scanline_shutter_amount = {self.scanline_shutter_offset}
        
        if knob in enable_scanline_shutter_amount:
            self.enableScanlineShutterAmount()            
        if knob in enable_scanline_controls:
            self.scanlineEnable()
        if knob in relevant_scanline_knobs:
            self.applySamplesScanline()  

# Scanline Render functions
    def scanlineEnable(self):       
        if self.include_scanline.value():
            self.selected_scanline.setEnabled(True)
            self.scanline_samples_amount.setEnabled(True)
            self.scanline_shutter.setEnabled(True)
            self.scanline_shutter_offset.setEnabled(True)
        else:
            self.selected_scanline.setEnabled(False)
            self.scanline_samples_amount.setEnabled(False)
            self.scanline_shutter.setEnabled(False)
            self.scanline_shutter_offset.setEnabled(False)

    def enableScanlineShutterAmount(self):
        if self.scanline_shutter_offset.value() == 'custom':
            self.scanline_shutter_offset_amount.setEnabled(True)
        else:
            self.scanline_shutter_offset_amount.setEnabled(False)
    
    def applySamplesScanline(self):
        scanline_node_knobs = {
            'samples': self.scanline_samples_amount,
            'shutter': self.scanline_shutter,
            'shutteroffset': self.scanline_shutter_offset,
            'shuttercustomoffset': self.scanline_shutter_offset_amount
        }
        # Get the selected nodes or all nodes
        selected_scanline_nodes = nuke.selectedNodes()

        if self.selected_scanline.value():
            nodes_to_apply = [node for node in selected_scanline_nodes if node.Class() == 'ScanlineRender']
        else:
            nodes_to_apply = [node for node in nuke.allNodes() if node.Class() == 'ScanlineRender']

        for node in nodes_to_apply:
            for knob_name, custom_knob in scanline_node_knobs.items():
                if knob_name in node.knobs():
                    node[knob_name].setValue(custom_knob.value())
