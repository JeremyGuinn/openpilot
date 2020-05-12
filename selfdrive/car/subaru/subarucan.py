import copy
from cereal import car

VisualAlert = car.CarControl.HUDControl.VisualAlert

def create_steering_control(packer, apply_steer, frame, steer_step):

  # counts from 0 to 15 then back to 0 + 16 for enable bit
  idx = (frame / steer_step) % 16

  values = {
    "Counter": idx,
    "LKAS_Output": apply_steer,
    "LKAS_Request": 1 if apply_steer != 0 else 0,
    "SET_1": 1
  }

  elif car_fingerprint in (CAR.OUTBACK, CAR.LEGACY):

    if apply_steer != 0:
      chksm_steer = apply_steer * -1
      chksm_engage = 1
    else:
      chksm_steer = 0
      chksm_engage = 0

    # counts from 0 to 7 then back to 0
    idx = (frame / steer_step) % 8
    steer2 = (chksm_steer >> 8) & 0x1F
    steer1 =  chksm_steer - (steer2 << 8)
    checksum = (idx + steer2 + steer1 + chksm_engage) % 256

    values = {
      "Counter": idx,
      "LKAS_Output": apply_steer,
      "LKAS_Request": 1 if apply_steer != 0 else 0,
      "Checksum": checksum
    }

  return packer.make_can_msg("ES_LKAS", 0, values)

def create_steering_status(packer, apply_steer, frame, steer_step):
  return packer.make_can_msg("ES_LKAS_State", 0, {})

def create_es_distance(packer, es_distance_msg, pcm_cancel_cmd):

  values = copy.copy(es_distance_msg)
  if pcm_cancel_cmd:
    values["Main"] = 1

  return packer.make_can_msg("ES_Distance", 0, values)

def create_es_lkas(packer, es_lkas_msg, visual_alert, left_line, right_line):

  values = copy.copy(es_lkas_msg)
  if visual_alert == VisualAlert.steerRequired:
    values["Keep_Hands_On_Wheel"] = 1

  values["LKAS_Left_Line_Visible"] = int(left_line)
  values["LKAS_Right_Line_Visible"] = int(right_line)

  return packer.make_can_msg("ES_LKAS_State", 0, values)

def create_door_control(packer, body_info_msg):
  values = copy.copy(body_info_msg)
  values["DOOR_OPEN_FR"] = 1
  values["_UNKNOWN"] = 5

  return packer.make_can_msg("BodyInfo", 2, values)

