"""
main.py

todo:
Animate wavetable modification over time.
Try white noise as initial wavetable.
"""

import os.path

import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import numpy as np

# todo: avoid global state!
x = np.linspace(-2, 2, 200)
duration = 2
fig, ax = plt.subplots()

def get_filepath(filename):
    return os.path.join('data', filename)

def plus_minus_ones(num_samples):
    """Generate an array of {-1, 1} chosen at random."""
    return (2*np.random.randint(0, 2, num_samples) - 1).astype(np.float32)

def plot_wavetable():
    num_samples = 100
    wavetable = plus_minus_ones(num_samples)

    plt.figure()
    plt.plot(wavetable)
    plt.show()

def make_frame(t):
    ax.clear()
    ax.plot(x, np.sinc(x**2) + np.sin(x + 2*np.pi/duration * t), lw=3)
    ax.set_ylim(-1.5, 2.5)
    return mplfig_to_npimage(fig)

def generate_animation():
    animation = VideoClip(make_frame, duration=duration)
    animation.write_gif(get_filepath('matplotlib.gif'), fps=20)

def main():
    # plot_wavetable()
    generate_animation()

if __name__ == '__main__':
    main()
