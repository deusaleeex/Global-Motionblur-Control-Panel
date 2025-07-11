import nuke

class TransformClass:
    def __init__(self):
        self.transform_knobs = []
        
        # Transform control knobs
        self.title = nuke.Text_Knob('heading', '')
        self.title.setValue('<h2>Transforms  </h2>')
        self.transform_knobs.append(self.title)
        
        self.include_transform = nuke.Boolean_Knob('include', 'enable')
        self.transform_knobs.append(self.include_transform)
        self.selected_transform = nuke.Boolean_Knob('selected_transform', 'apply to selected only')
        self.selected_transform.setEnabled(False)
        self.transform_knobs.append(self.selected_transform)

        self.transform_mb_amount = nuke.Double_Knob('transform_amount', 'motionblur')
        self.transform_mb_amount.setRange(0, 4)
        self.transform_mb_amount.setValue(0)
        self.transform_mb_amount.setEnabled(False)
        self.transform_knobs.append(self.transform_mb_amount)

        self.transform_shutter = nuke.Double_Knob('transform_shutter', 'shutter')
        self.transform_shutter.setRange(0, 2)
        self.transform_shutter.setValue(0.5)
        self.transform_shutter.setEnabled(False)
        self.transform_knobs.append(self.transform_shutter)

        self.transform_shutter_offset = nuke.Enumeration_Knob('transform_offset', 'shutter offset', ['start', 'centered', 'end', 'custom'])
        self.transform_shutter_offset.setValue('start')
        self.transform_shutter_offset.setEnabled(False)
        self.transform_knobs.append(self.transform_shutter_offset)

        self.transform_shutter_offset_amount = nuke.Double_Knob('transform_offset_amount', '')
        self.transform_shutter_offset_amount.setRange(-1, 1)
        self.transform_shutter_offset_amount.setValue(0)
        self.transform_shutter_offset_amount.setEnabled(False)
        self.transform_shutter_offset_amount.clearFlag(nuke.STARTLINE)  
        self.transform_knobs.append(self.transform_shutter_offset_amount)

    def create_transform_knobs(self, panel_instance):      
        # Add Transform knobs to the panel_instance
        for knob in self.transform_knobs:
            panel_instance.addKnob(knob)

    def knobChanged(self, knob):
        # Handle changes in the UI
        enable_transform_controls = {self.include_transform}
        relevant_transform_knobs = {self.transform_mb_amount, self.transform_shutter, self.transform_shutter_offset, self.transform_shutter_offset_amount}
        enable_transform_shutter_amount = {self.transform_shutter_offset}
        
        if knob in enable_transform_controls:
            self.transformEnable()
        if knob in relevant_transform_knobs:
            self.applyMBTransform()
        if knob in enable_transform_shutter_amount:
            self.enableTransformShutterAmount()

# Transform functions
    def transformEnable(self):       
        if self.include_transform.value():
            self.selected_transform.setEnabled(True)
            self.transform_mb_amount.setEnabled(True)
            self.transform_shutter.setEnabled(True)
            self.transform_shutter_offset.setEnabled(True)
        else:
            self.selected_transform.setEnabled(False)
            self.transform_mb_amount.setEnabled(False)
            self.transform_shutter.setEnabled(False)
            self.transform_shutter_offset.setEnabled(False)

    def enableTransformShutterAmount(self):
        if self.transform_shutter_offset.value() == 'custom':
            self.transform_shutter_offset_amount.setEnabled(True)
        else:
            self.transform_shutter_offset_amount.setEnabled(False)
            
    def applyMBTransform(self):
        transform_node_knobs = {
            'motionblur': self.transform_mb_amount,
            'shutter': self.transform_shutter,
            'shutteroffset': self.transform_shutter_offset,
            'shuttercustomoffset': self.transform_shutter_offset_amount
        }
        # Get the selected nodes
        selected_transform_nodes = nuke.selectedNodes()

        if self.selected_transform.value():
            nodes_to_apply = [node for node in selected_transform_nodes if node.Class() == 'Transform']
        else:
            nodes_to_apply = [node for node in nuke.allNodes() if node.Class() == 'Transform']

        for node in nodes_to_apply:
            for knob_name, custom_knob in transform_node_knobs.items():
                if knob_name in node.knobs():
                    node[knob_name].setValue(custom_knob.value())                
