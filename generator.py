def frame_generator(start_frame, end_frame, base, step, fill, reverse):
    """Creates a list of unique frames ordered in a way defined by user input"""
    skip_sequence = [base]

    for i in range(step - 1):
        skip = -(-(skip_sequence[i]) // 2)
        skip_sequence.append(skip)
    if fill:
        if skip_sequence[-1] != 1:
            skip_sequence.append(1)

    frame_sequence = []
    if not reverse:
        frame_sequence = [i for s in skip_sequence for i in range(start_frame, end_frame+1, s)]
    else:
        frame_sequence = [i for s in skip_sequence for i in range(end_frame+1, start_frame, -s)]
    frame_sequence = list(dict().fromkeys(frame_sequence))

    frame_list = deadline_format(frame_sequence)
    return frame_list


def deadline_format(raw_list):
    """Turns a frame sequence list into a Deadline formatted string."""
    formatted_list = []
    switch = 0
    for idx, n in enumerate(raw_list):
        if abs(raw_list[(idx + 1) % len(raw_list)] - raw_list[idx]) != 1:
            if switch > 0:
                switch = 0
                pop_val = formatted_list.pop()
                formatted_list.append(pop_val + str(n))
            else:
                formatted_list.append(str(n))
        else:
            switch += 1
            if switch == 1:
                formatted_list.append(str(n) + '-')

    formatted_list = ','.join(formatted_list)
    return formatted_list