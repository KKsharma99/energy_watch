from energy_watch import data, classify

bldg_data = data.Data()

bldg_data.replace_nan_0()

bldg_classify = classify.Classify(bldg_data, 30)

print("Classify object created")