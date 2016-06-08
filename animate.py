def is_animated(commands):
    return any(filter(lambda tup: tup[0] in {'frames', 'vary', 'basename'}, commands))

def num_frames(commands):
    for cmd in commands:
        if cmd[0] == 'frames':
            return cmd[1]
    else:
        raise AttributeError('Please specify the number of frames using the following command: frames <number>')

def get_basename(commands):
    for cmd in commands:
        if cmd[0] == 'basename':
            return cmd[1]
    else:
        raise AttributeError('Please specify the filename prefix using the following command: basename <prefix>')

def make_knobs(commands, frames):
    # Truncated `vary` commands
    vcmds = [cmd[1:] for cmd in commands if cmd[0] == 'vary']
    # Dict of arrays of knob values
    knobs = {knob: [float('nan')] * frames for knob in [t[0] for t in vcmds]}
    # Set the knob values
    for knob, t0, t1, x0, x1 in vcmds:
        # We allow t1 to be the length so that some animations involving rotations can be done smoothly
        if 0 <= t0 < t1 <= frames:
            x = knobs[knob]
            for t in range(t0, min(t1 + 1, frames)):
                # Derived from point-slope form
                x[t] = x0 + (float(x1) - x0) * (t - t0) / (t1 - t0)
        elif t0 >= t1:
            raise ValueError('You inserted the first and last frame numbers backwards!')
        else:
            raise ValueError('First and last frame numbers out of bounds: %d, %d.  Total number of frames: %d' % (frame0, frame1, frames))
    # After looping
    return knobs
