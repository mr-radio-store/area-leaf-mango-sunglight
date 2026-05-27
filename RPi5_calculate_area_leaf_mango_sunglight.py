import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# ================================
# Calcuate sunligh cover on mango leaves in Cambodia between sun rise and sun set
# 1. Mango tree parameters
# ================================
N_leaves = 5000
A_leaf = 0.015
A_total = N_leaves * A_leaf

S = 0.5                     # canopy shading factor
alpha_max = 70              # max sun elevation at noon
daylight_hours = 12
dt = 0.1

# ================================
# 2. Time array
# ================================
time = np.arange(0, daylight_hours, dt)
T = daylight_hours

# ================================
# 3. Sun elevation over day
# ================================
sun_angle = alpha_max * np.sin(np.pi * time / T)  # degrees
sun_angle_rad = np.radians(sun_angle)

# ================================
# 4. Environmental noise
# ================================
# Clouds: reduce sunlight 50%-100%
cloud_factor = np.random.uniform(0.5, 1.0, len(time))

# Random airplane or bird shadows: temporary block 0-20%
shadow_factor = 1 - np.random.binomial(1, 0.02, len(time)) * np.random.uniform(0.1, 0.2, len(time))

# Dust/haze factor: reduce solar intensity 90%-100%
dust_factor = np.random.uniform(0.9, 1.0, len(time))

# Orientation variation: some leaves not perfectly random
orientation_factor = 0.4 + np.random.rand(len(time))*0.2  # between 0.4 and 0.6

# ================================
# 5. Sunlit leaf area over day
# ================================
A_sunlit = orientation_factor * S * A_total * np.sin(sun_angle_rad) * cloud_factor * shadow_factor * dust_factor

# ================================
# 6. Animation MP4
# ================================
fig, ax = plt.subplots(figsize=(10,5))
line, = ax.plot([], [], color='orange', lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
ax.set_xlim(0, daylight_hours)
ax.set_ylim(0, np.max(A_sunlit)*1.1)
ax.set_xlabel("Time (hours since sunrise)")
ax.set_ylabel("Sunlit Leaf Area (m²)")
ax.set_title("Sunlit Leaf Area of a Mango Tree in Cambodia (Noisy Environment)")
ax.grid(True, linestyle='--', alpha=0.5)

def animate(i):
    line.set_data(time[:i+1], A_sunlit[:i+1])
    time_text.set_text(f"Time: {time[i]:.2f} h")
    return line, time_text

anim = FuncAnimation(fig, animate, frames=len(time), interval=50)
writer = FFMpegWriter(fps=20)
anim.save("mango_tree_sunlit_area_noisy.mp4", writer=writer)
plt.close()

# ================================
# 7. Save tracking graph JPEG
# ================================
plt.figure(figsize=(10,5))
plt.plot(time, A_sunlit, color='orange', lw=2)
plt.xlabel("Time (hours since sunrise)")
plt.ylabel("Sunlit Leaf Area (m²)")
plt.title("Sunlit Leaf Area of a Mango Tree in Cambodia (Noisy Environment)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("mango_tree_sunlit_area_noisy_tracking.jpeg", dpi=150)
plt.show()

# ================================
# 8. Total sunlight exposure
# ================================
A_day = np.sum(A_sunlit * dt)
print(f"Estimated total sunlit leaf area over the day (noisy environment): {A_day:.2f} m²·hours")
