import numpy as np
import pickle
import os
 
concrete_grades = {
    'M20': [0, 0, 0, 0, 0],
    'M25': [1, 0, 0, 0, 0],
    'M30': [0, 1, 0, 0, 0],
    'M35': [0, 0, 1, 0, 0],
    'M40': [0, 0, 0, 1, 0],
    'M45': [0, 0, 0, 0, 1]
}
 
wc_ratio_ranges = {
    'M20': (0.55, 0.75),
    'M25': (0.5, 0.7),
    'M30': (0.45, 0.65),
    'M35': (0.4, 0.6),
    'M40': (0.35, 0.55),
    'M45': (0.3, 0.5),
}

#importing the trained model
model_path = os.path.join(os.path.dirname(__file__), '..\static\model.pkl')
model = pickle.load(open(model_path, 'rb'))
 
def get_concrete_strength(mix_proportion, concrete_grade, wc_ratio):


  # mix proportion
  mix_proportion = list(map(float, mix_proportion.split(":")))
  if len(mix_proportion) == 3:
    mix_proportion.append(0)
  elif len(mix_proportion) == 4:
    pass
  else:
    return 'Please enter a valid Mix Proportion'
  
  # concrete grade
  if concrete_grade not in concrete_grades.keys():
    return 'Please select a valid Concrete Grade between M20 and M55'
  
  # W/C ratio and checking whether it is in the range depending upon the concrete grade
  try:
    wc_ratio = float(wc_ratio)
  except:
    return 'Please enter an appropriate numerical value'
  if not (wc_ratio_ranges[concrete_grade][0] <= wc_ratio <= wc_ratio_ranges[concrete_grade][1]):
    return 'Please enter a value in the specified range W/C ratio'
  #setting up values for feeding to the model for prediction
  val = list(mix_proportion)
  val.append(wc_ratio)
  val.extend(concrete_grades[concrete_grade])
  val = np.array(val).reshape(1, -1)

	#predicting the value
  concreteStrength = model.predict(val)

  concreteStrength = float(np.round(concreteStrength, 2))
  return ('''
  <strong>Mix Proportion:</strong> {0}<br>
  <strong>Concrete Grade:</strong> {1}<br>
  <strong>WC Ratio:</strong> {2}<br>
  <strong>Compressive Concrete Strength:</strong> {3}MPa'''.format(":".join(map(str, mix_proportion)), concrete_grade, wc_ratio, concreteStrength))

 
 