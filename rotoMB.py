import nuke

class RotoClass:
    def __init__(self):

        self.roto_knobs = []

        self.name = nuke.Text_Knob('heading', '')
        self.name.setValue('<h2>Rotos  </h2>')
        self.roto_knobs.append(self.name)

        self.include_roto = nuke.Boolean_Knob('include', 'enable')
        self.roto_knobs.append(self.include_roto)

        self.selected_roto = nuke.Boolean_Knob('selected_roto', 'apply to selected only')
        self.selected_roto.setEnabled(False)
        self.roto_knobs.append(self.selected_roto)
        
        self.include_paint = nuke.Boolean_Knob('include_paint', 'include RotoPaint nodes')
        self.include_paint.setEnabled(False)
        self.roto_knobs.append(self.include_paint)

        self.mb_mode = nuke.Radio_Knob('mode', 'method', ('shape', 'global'))
        self.mb_mode.setEnabled(False)
        self.roto_knobs.append(self.mb_mode)

        self.roto_mb_amount = nuke.Double_Knob('amount', 'motionblur')
        self.roto_mb_amount.setRange(0, 4)
        self.roto_mb_amount.setValue(1)
        self.roto_mb_amount.setEnabled(False)
        self.roto_knobs.append(self.roto_mb_amount)

        self.roto_shutter = nuke.Double_Knob('shutter', 'shutter')
        self.roto_shutter.setRange(-1, 2)
        self.roto_shutter.setValue(0.5)
        self.roto_shutter.setEnabled(False)
        self.roto_knobs.append(self.roto_shutter)

        self.roto_shutter_offset = nuke.Enumeration_Knob('offset', 'shutter offset', ['start', 'centered', 'end', 'custom'])
        self.roto_shutter_offset.setValue('centered')
        self.roto_shutter_offset.setEnabled(False)
        self.roto_knobs.append(self.roto_shutter_offset)

        self.roto_shutter_offset_amount = nuke.Double_Knob('offsetamount', '')
        self.roto_shutter_offset_amount.setRange(-1, 1)
        self.roto_shutter_offset_amount.setValue(0)
        self.roto_shutter_offset_amount.setEnabled(False)
        self.roto_shutter_offset_amount.clearFlag(nuke.STARTLINE)  
        self.roto_knobs.append(self.roto_shutter_offset_amount)
    
    def create_roto_knobs(self, panel_instance):
        # Add Roto knobs to the panel_instance
        for knob in self.roto_knobs:
            panel_instance.addKnob(knob)

    def knobChanged(self, knob):
        # Handle changes in the UI for the Roto class
        enable_roto_controls = [self.include_roto]
        relevant_roto_knobs = [self.mb_mode, self.roto_mb_amount, self.roto_shutter, self.roto_shutter_offset,
                               self.roto_shutter_offset_amount]

        if knob in enable_roto_controls:
            self.rotoEnable()
        if knob in relevant_roto_knobs:
            self.applyMBRoto()

    def rotoEnable(self):
        # Create a dictionary with all the knobs you want to enable or disable
        knobs_to_toggle = {
            'selected_roto': self.selected_roto,
            'include_paint': self.include_paint,
            'mb_mode': self.mb_mode,
            'roto_mb_amount': self.roto_mb_amount,
            'roto_shutter': self.roto_shutter,
            'roto_shutter_offset': self.roto_shutter_offset,
            'roto_shutter_offset_amount': self.roto_shutter_offset_amount
        }

        # Set the enabled state based on include_roto's value
        enabled = self.include_roto.value()

        # Loop through the dictionary and set each knob's enabled state
        for knob in knobs_to_toggle.values():
            knob.setEnabled(enabled)

    def applyMBRoto(self):
        # list of node knob names
        roto_node_knobs = {
            'motionblur_mode': self.mb_mode,
            'motionblur': self.roto_mb_amount,
            'motionblur_shutter': self.roto_shutter,
            'motionblur_shutter_offset_type': self.roto_shutter_offset,
            'motionblur_shutter_offset': self.roto_shutter_offset_amount
        }
        
        # Prefix for global knobs
        global_prefix = 'global_'
        global_knobs = {}

        # Get the selected nodes
        selected_nodes = nuke.selectedNodes()
        
        # if apply to selected only is ticked, then get a list of the nodes we are applying to changes to. Otherwise nuke.allNodes() is used
        if self.selected_roto.value():
            
            if self.include_paint.value():
                nodes_to_apply = [node for node in selected_nodes if node.Class() in ('Roto', 'RotoPaint')]
            else:
                nodes_to_apply = [node for node in selected_nodes if node.Class() == 'Roto']
        else:
            # Filter all nodes based on class (Roto and optionally Paint)
            if self.include_paint.value():
                nodes_to_apply = [node for node in nuke.allNodes() if node.Class() in ('Roto', 'RotoPaint')]
            else:
                nodes_to_apply = [node for node in nuke.allNodes() if node.Class() == 'Roto']
        
        if self.mb_mode.value() == 'shape':
            for node in nodes_to_apply:
                for knob_name, custom_knob in roto_node_knobs.items():
                    if knob_name in node.knobs():
                        node[knob_name].setValue(custom_knob.value())
                        
        else:
            if self.mb_mode.value() == 'global':
                # Build the global_knobs dictionary with the prefix applied to all but the first key, this is because the first key is motionblur_mode, which doesn't need the global_ prefix.
                for index, (knob_name, custom_knob) in enumerate(roto_node_knobs.items()):
                    if index == 0:
                        global_knobs[knob_name] = custom_knob.value()  # Keep the first key unchanged
                    else:
                        global_knobs[global_prefix + knob_name] = custom_knob.value()  # Add prefix to other keys
                
                # Apply global knob values to the nodes
                for node in nodes_to_apply:
                    for knob_name in global_knobs:
                        if knob_name in node.knobs():
                            node[knob_name].setValue(global_knobs[knob_name])

