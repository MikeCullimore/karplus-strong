"""
main.py

todo:
Animate wavetable modification over time.
    Plot single frame.
    Return all wavetables and final waveform.
Tuning trick in original paper p8 to get closer to desired frequency.
Try white noise as initial wavetable.
Write up as IPython notebook?
"""

import os.path

import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import numpy as np

# todo: avoid global state!
# x = np.linspace(-2, 2, 200)
# duration = 2
# fig, ax = plt.subplots()

def get_filepath(filename):
    return os.path.join('data', filename)

def plus_minus_ones(num_samples):
    """Generate an array of {-1, 1} chosen at random."""
    return (2*np.random.randint(0, 2, num_samples) - 1).astype(np.float32)

def karplus_strong(frequency, num_samples, stretch_factor=1., sampling_frequency=44100):
    # Initialise wavetable.
    # wavetable_size = np.floor(sampling_frequency/frequency).astype(int)
    wavetable_size = np.around(sampling_frequency/frequency).astype(int)
    wavetable = plus_minus_ones(wavetable_size)

    # The actual frequency could be slightly off because the wavetable length is an integer.
    # The effect will be more pronounced at high frequencies.
    # Higher sampling frequencies should mitigate the issue?
    # todo: plot error_percent vs frequency.
    # actual_frequency = sampling_frequency/wavetable_size
    # error = actual_frequency - frequency
    # error_percent = 100*error/frequency
    # print(f'Desired frequency: {frequency}')
    # print(f'Actual frequency: {actual_frequency}')
    # print(f'Error: {error}')
    # print(f'Error [%]: {error_percent}')

    signal = np.zeros(num_samples, dtype=np.float32)
    current_sample = 0
    k = 1 - 1/stretch_factor
    for i in range(1, num_samples):
        r = np.random.binomial(1, k)
        if r == 0:
            wavetable[current_sample] = 0.5*(wavetable[current_sample] + signal[i-1])
        signal[i] = wavetable[current_sample]
        current_sample = (current_sample + 1) % wavetable_size
    
    # Remove DC offset.
    signal -= np.mean(signal)
    
    return signal

# def make_frame(t):
#     """todo: start by plotting waveform with vertical line moving to indicate time."""
#     print(t)
#     ax.clear()
#     ax.plot(x, np.sinc(x**2) + np.sin(x + 2*np.pi/duration * t), lw=3)
#     ax.set_ylim(-1.5, 2.5)
#     return mplfig_to_npimage(fig)

# def generate_animation():
#     animation = VideoClip(make_frame, duration=duration)
#     animation.write_gif(get_filepath('matplotlib.gif'), fps=20)

def plot_stretch_factors():
    # frequency = 27.5  # Lowest note on a piano.
    frequency = 220
    # frequency = 440
    # frequency = 4186  # Highest note on a piano. Discrepancy is higher: why?
    
    plt.figure()
    stretch_factors = [1, 2.1, 3.5, 4, 8]
    for i, stretch_factor in enumerate(stretch_factors):
        signal = karplus_strong(frequency, 100000, stretch_factor, sampling_frequency=8000)
        plt.plot(signal + i)
    
    plt.show()

def main():
    # generate_animation()
    plot_stretch_factors()

if __name__ == '__main__':
    main()
