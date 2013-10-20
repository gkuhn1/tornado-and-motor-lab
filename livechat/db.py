

import motor
import settings

connection = motor.MotorClient(settings.MONGO_HOST, settings.MONGO_PORT).open_sync()