from flask import Flask
from flask_restplus import Api, Resource, fields
import RPi.GPIO as GPIO


app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='RESTful Pi',
          description='A RESTful API to control the GPIO pins of a Raspbery Pi',
          doc='/docs')

ns = api.namespace('pins', description='Pin related operations')

pin_model = api.model('pins', {
    'id': fields.Integer(readonly=True, description='The pin unique identifier'),
    'pin_num': fields.Integer(required=True, description='GPIO pin associated with this endpoint'),
    'color': fields.String(required=True, description='LED color'),
    'state': fields.String(required=True, description='LED on or off')
})

byte_model = api.model('byteOutput',{
    'redflag': fields.Integer(required=True, description='Flag to be used in some way'),
    'value': fields.Integer(required=True, description='The number that will be displayed')
    })

class PinUtil(object):
    def __init__(self):
        self.counter = 0
        self.pins = []

    def get(self, id):
        
        for pin in self.pins:
            if pin['id'] == id:
                return pin
        api.abort(404, f"pin {id} doesn't exist.")

    def create(self, data):
        pin = data
        pin['id'] = self.counter = self.counter + 1
        self.pins.append(pin)
        GPIO.setup(pin['pin_num'], GPIO.OUT)

        if pin['state'] == 'off':
            GPIO.output(pin['pin_num'], GPIO.LOW)
        elif pin['state'] == 'on':
            GPIO.output(pin['pin_num'], GPIO.HIGH)
        return pin

    def update(self, id, data):
        pin = self.get(id)
        pin.update(data)  # this is the dict_object update method
        GPIO.setup(pin['pin_num'], GPIO.OUT)

        if pin['state'] == 'off':
            GPIO.output(pin['pin_num'], GPIO.LOW)
        elif pin['state'] == 'on':
            GPIO.output(pin['pin_num'], GPIO.HIGH)

        return pin

    def delete(self, id):
        pin = self.get(id)
        GPIO.output(pin['pin_num'], GPIO.LOW)
        self.pins.remove(pin)


class ByteOutputUtil(object):
    def __init__(self):
        self.counter = 0
        self.value = 256
        self.redflag = 0
        
    def get(self):
        self.value = 0
        self.counter = 9
        multiplicator = 1
        for pin in pin_util.pins:
            tempPin = pin_util.get(self.counter)
            if tempPin['state'] == 'on':
                self.value = self.value + 1*multiplicator 
            self.counter = self.counter -1
            multiplicator = multiplicator *2
            if self.counter == 1: #reached the redflag LED
                tempPin = pin_util.get(self.counter)
                if tempPin['state'] == 'on':
                    self.redflag = 1
                elif tempPin['state'] == 'off':
                    self.redflag = 0
                break        
        return self
    
    def update(self, data):
        
        newByte = data
        newByte.update(data)
        
        
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        
        if newByte['redflag'] == 0:
            GPIO.output(23, GPIO.LOW)
        else:
            GPIO.output(23, GPIO.HIGH)
        
        #set the pins according to the integer
        localValue = newByte['value']
        if localValue > 255:
            GPIO.output(23, GPIO.HIGH)
            newByte['redflag'] == 1
            newByte['value'] == 0
            return newByte
        else:
            GPIO.output(23, GPIO.LOW)
        
        if localValue >= 128:
            GPIO.output(24, GPIO.HIGH)
            localValue = localValue -128
        else:
            GPIO.output(24, GPIO.LOW)
        
        if localValue >= 64:
            GPIO.output(25, GPIO.HIGH)
            localValue = localValue -64
        else:
            GPIO.output(25, GPIO.LOW)
                        
        if localValue >= 32:
            GPIO.output(22, GPIO.HIGH)
            localValue = localValue -32
        else:
            GPIO.output(22, GPIO.LOW)
            
        if localValue >= 16:
            GPIO.output(12, GPIO.HIGH)
            localValue = localValue -16
        else:
            GPIO.output(12, GPIO.LOW)
            
        if localValue >= 8:
            GPIO.output(16, GPIO.HIGH)
            localValue = localValue -8
        else:
            GPIO.output(16, GPIO.LOW)
            
        if localValue >= 4:
            GPIO.output(20, GPIO.HIGH)
            localValue = localValue -4
        else:
            GPIO.output(20, GPIO.LOW)
        
        if localValue >= 2:
            GPIO.output(21, GPIO.HIGH)
            localValue = localValue -2
        else:
            GPIO.output(21, GPIO.LOW)
            
        if localValue >= 1:
            GPIO.output(13, GPIO.HIGH)
            localValue = localValue -1
        else:
            GPIO.output(13, GPIO.LOW)
        
        return self
 
@ns.route('/byte') #get or update a 8Bit value
class ByteValue(Resource):
    @ns.marshal_with(byte_model)
    def get(self):
        return byte_outpututil.get()
    
    @ns.expect(byte_model, validate=True)
    @ns.marshal_with(byte_model)
    def put(self):
        return byte_outpututil.update(api.payload)
   
   
   
@ns.route('/')  # keep in mind this our ns-namespace (pins/)
class PinList(Resource):
    """Shows a list of all pins, and lets you POST to add new pins"""

    @ns.marshal_list_with(pin_model)
    def get(self):
        """List all pins"""
        return pin_util.pins

    @ns.expect(pin_model)
    @ns.marshal_with(pin_model, code=201)
    def post(self):
        """Create a new pin"""
        return pin_util.create(api.payload)


@ns.route('/<int:id>')
@ns.response(404, 'pin not found')
@ns.param('id', 'The pin identifier')
class Pin(Resource):
    """Show a single pin item and lets you update/delete them"""

    @ns.marshal_with(pin_model)
    def get(self, id):
        """Fetch a pin given its resource identifier"""
        return pin_util.get(id)

    @ns.response(204, 'pin deleted')
    def delete(self, id):
        """Delete a pin given its identifier"""
        pin_util.delete(id)
        return '', 204

    @ns.expect(pin_model, validate=True)
    @ns.marshal_with(pin_model)
    def put(self, id):
        """Update a pin given its identifier"""
        return pin_util.update(id, api.payload)
    
    @ns.expect(pin_model)
    @ns.marshal_with(pin_model)   
    def patch(self, id):
        """Partially update a pin given its identifier"""
        return pin_util.update(id, api.payload)


GPIO.setmode(GPIO.BCM)

pin_util = PinUtil()
pin_util.create({'pin_num': 23, 'color': 'red', 'state': 'off'})
pin_util.create({'pin_num': 24, 'color': 'yellow', 'state': 'off'})
pin_util.create({'pin_num': 25, 'color': 'blue', 'state': 'off'})
pin_util.create({'pin_num': 22, 'color': 'red', 'state': 'off'})
pin_util.create({'pin_num': 12, 'color': 'yellow', 'state': 'off'})
pin_util.create({'pin_num': 16, 'color': 'blue', 'state': 'off'})
pin_util.create({'pin_num': 20, 'color': 'red', 'state': 'off'})
pin_util.create({'pin_num': 21, 'color': 'green', 'state': 'off'})
pin_util.create({'pin_num': 13, 'color': 'yellow', 'state': 'off'})

byte_outpututil = ByteOutputUtil()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
