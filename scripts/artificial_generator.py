# Draw Fingerprint
def fingerprint_draw_r(bldg, r, save=False, show=False, df=df):
    theta = []
    for i in range(0, len(r)):
        theta.append((i%96)/96 * 2 * np.pi)
    r = r.append(pd.Series(r.values[0]))
    theta.append(0)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar', facecolor='white')
    ax.plot(theta, r, c='y')
    ax.set_xticklabels(['12am', '3am', '6am', '9am', '12pm', '3pm', '6pm', '9pm'])
    plt.figure(figsize=(4,4))
    ax.set_rlabel_position(90)
    ax.grid(True)
    ax.grid(linewidth=.3)
    ax.set_rmax(max(r)*1.2)
    ax.set_title("Energy Usage of Building " + bldg +  " (kWh)", va='bottom')
    ax.title.set_position([.5, 1.15])
    if save: fig.savefig('fingerprints/' + bldg + '.png', bbox_inches='tight')
    if show: plt.show()
        
# Draw Cocentric
#draw_cocentric('B')
def draw_cocentric(bldg, ret=False, show=True):
    random_list = []
    base = random.randint(50,400)
    for i in range(0, 96): random_list.append(base + int(base/random.randint(8,15)))
    random_list = pd.Series(random_list)
    if show: fingerprint_draw_r(bldg, show=True, r=random_list)
    if ret: return random_list

# Draw People
#draw_people('B')
def draw_people(bldg, ret=False, show=True):
    random_list = []
    
    # Randomly Determine Sections
    non_people = random.randint(28, 51)
    non_people_1 = int(0.60 * non_people)
    non_people_2 = non_people - non_people_1
    trans_size = random.randint(5, 8)
    people = 96 - non_people - 2 * trans_size
    # Determine Magnitudes
    base = random.randint(50,400)
    people_base = base + random.randint(base, int(1.4*base))
    base_max = base + base//4
    people_base_max = people_base + people_base//4
    base_diff = people_base - base
    # Non People Section
    for i in range(0, non_people_1): random_list.append(random.uniform(base, base_max))
    # Transition
    for i in range(0, trans_size): random_list.append(random.uniform(base_max, people_base))
    # People Section
    for i in range(0, people): random_list.append(random.uniform(people_base, people_base_max))
    # Transition
    for i in range(0, trans_size): random_list.append(random.uniform(base_max, people_base))
    # Non People Section
    for i in range(0, non_people_2): random_list.append(random.uniform(base, base_max))
    # Randomly Rotate Data
    random_list = rotate_list(random_list, random.randint(0,16))
    
    random_list = pd.Series(random_list)
    if show: fingerprint_draw_r(bldg, show=True, r=random_list)
    if ret: return random_list
    
# Draw Schedule
#draw_schedule('B101')
def draw_schedule(bldg, ret=False, show=True):
    random_list = []
    
    # Randomly Determine Sections
    off_time = random.randint(28, 51)
    off_time_1 = int(0.60 * off_time)
    off_time_2 = off_time - off_time_1
    on_time = 96 - off_time
    # Determine Magnitudes
    base = random.randint(50,400)
    higher_base = base + random.randint(base, int(1.2*base))
    base_max = base + base//random.randint(3,7)
    higher_base_max = higher_base + higher_base//random.randint(3,7)
    base_diff = higher_base - base
    # Non People Section
    for i in range(0, off_time_1): random_list.append(random.uniform(base, base_max))
    # People Section
    for i in range(0, on_time): random_list.append(random.uniform(higher_base, higher_base_max))
    # Non People Section
    for i in range(0, off_time_2): random_list.append(random.uniform(base, base_max))
    # Randomly Rotate Data
    random_list = rotate_list(random_list, random.randint(0,16))
    
    random_list = pd.Series(random_list)
    if show: fingerprint_draw_r(bldg, show=True, r=random_list)
    if ret: return random_list
    
# Draw Reverse
# draw_reverse('B')
def draw_reverse(bldg, ret=False, show=True):
    random_list = []
    
    # Randomly Determine Sections
    sect_1 = random.randint(28, 44)
    trans_size = random.randint(5, 10)
    corner_in_ct = int(0.4 * trans_size)
    corner_out_ct = trans_size - corner_in_ct
    sect_2 = 96 - sect_1 - 2 * trans_size
    # Determine Magnitudes
    base = random.randint(50,400)
    base_max = int(base * 1.055)
    corner_in = int(base * 0.798)
    corner_in_max = int(base * 0.852)
    corner_out = int(base * 0.909)
    corner_out_max = int(base * 0.963)
    # Generate Values
    for i in range(0, sect_1): random_list.append(random.uniform(base, base_max))
    for i in range(0, corner_in_ct): random_list.append(random.uniform(corner_in, corner_in_max))
    for i in range(0, corner_out_ct): random_list.append(random.uniform(corner_out, corner_out_max)) 
    for i in range(0, sect_2): random_list.append(random.uniform(base, base_max))
    for i in range(0, corner_out_ct): random_list.append(random.uniform(corner_out, corner_out_max))
    for i in range(0, corner_in_ct): random_list.append(random.uniform(corner_in, corner_in_max))
    # Randomly Rotate Data
    random_list = rotate_list(random_list, random.randint(0,20))

    random_list = pd.Series(random_list)
    if show: fingerprint_draw_r(bldg, show=True, r=random_list )
    if ret: return random_list

# Draw Reverse
# draw_reverse_winter('B')
def draw_reverse_winter(bldg, ret=False, show=True):
    random_list = []

    # Randomly Determine Sections
    off_time = random.randint(36, 46)
    off_time_1 = int(0.60 * off_time)
    off_time_2 = off_time - off_time_1
    on_time = 96 - off_time
    # Determine Magnitudes
    base = random.randint(50,400)
    higher_base = base + random.randint(base, int(1.2*base))
    base_max = base + base//random.randint(3,7)
    higher_base_max = higher_base + higher_base//random.randint(3,7)
    base_diff = higher_base - base
    # Non People Section
    for i in range(0, off_time_1): random_list.append(random.uniform(base, base_max))
    # People Section
    for i in range(0, on_time): random_list.append(random.uniform(higher_base, higher_base_max))
    # Non People Section
    for i in range(0, off_time_2): random_list.append(random.uniform(base, base_max))
    # Randomly Rotate Data
    random_list = rotate_list(random_list, 48)
    
    random_list = pd.Series(random_list)
    if show: fingerprint_draw_r(bldg, show=True, r=random_list)
    if ret: return random_list
    
    
# Draw Random
#draw_random('B')
def draw_random(bldg, ret=False, show=True):
    random_list = []
    base = random.randint(50,400)
    comp_1 = int(base * 0.5)
    comp_2 = int(base * 1.5)
    for i in range(0, 96): random_list.append(random.uniform(1, comp_1) + random.uniform(1, base) + random.uniform(1, comp_2))
    random_list = pd.Series(random_list)
    if show: fingerprint_draw_r('B', show=True, r=random_list)
    if ret: return random_list
    
#Generate Artificial Data
# Classification Types: 0 - Cocentric, 1 - People, 2 - Schedule, 3 - Reverse, 4 - Random 
# Generates a Dataframe of fake data in the form of Time (15 min ) by building. Also returns y with the target values.
def gen_fake_data(rows_per_type, types=[0,1,2,3,4]):
    y = []
    data = []
    for i in types:
        for j in range(0, rows_per_type):
            bldg = str(j)
            y.append(i)
            if i == 0: data.append(draw_cocentric('Cocentric_' + bldg, ret=True, show=False))
            elif i == 1: data.append(draw_people('People_' + bldg, ret=True, show=False)) 
            elif i == 2: data.append(draw_schedule('Schedule_' + bldg, ret=True, show=False))
            elif i == 3: data.append(draw_reverse('Reverse_' + bldg, ret=True, show=False))
            elif i == 4: data.append(draw_random('Random_' + bldg, ret=True, show=False))
    data_df = pd.DataFrame(data)
    y = pd.DataFrame(y).astype('int64')
    return data_df, y