import tkinter as tk
import math

class AirplaneInstruments(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airplane Instruments")
        self.geometry("800x400")
        
        self.heading = 0
        self.pitch = 0
        self.roll = 0

        # Heading Indicator
        self.canvas_heading = tk.Canvas(self, width=300, height=300, bg='white')
        self.canvas_heading.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Attitude Indicator
        self.canvas_attitude = tk.Canvas(self, width=300, height=300, bg='white')
        self.canvas_attitude.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.update_instruments()

    def update_instruments(self):
        self.update_heading_indicator()
        self.update_attitude_indicator()
        self.after(100, self.update_instruments)

    def update_heading(self, new_heading):
        self.heading = new_heading

    def update_attitude(self, new_pitch, new_roll):
        self.pitch = new_pitch
        self.roll = new_roll

    def update_heading_indicator(self):
        self.canvas_heading.delete("all")
        center_x, center_y = 150, 150
        radius = 100
        
        self.canvas_heading.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black")
        self.canvas_heading.create_text(center_x, center_y, text="N", font=("Arial", 12))
        
        for angle in range(0, 360, 30):
            angle_rad = math.radians(angle)
            x = center_x + radius * math.sin(angle_rad)
            y = center_y - radius * math.cos(angle_rad)
            self.canvas_heading.create_text(x, y, text=str(angle), font=("Arial", 10))

        heading_angle = math.radians(self.heading)
        heading_x = center_x + radius * math.sin(heading_angle)
        heading_y = center_y - radius * math.cos(heading_angle)
        
        self.canvas_heading.create_line(center_x, center_y, heading_x, heading_y, fill="red", width=2)
        self.canvas_heading.create_text(center_x, center_y + radius + 40, text=f"Heading: {self.heading}°", font=("Arial", 12))

    def update_attitude_indicator(self):
        self.canvas_attitude.delete("all")
        center_x, center_y = 150, 150
        radius = 100
        
        # Draw the circle
        self.canvas_attitude.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black")
        
        # Calculate horizon line endpoints based on roll angle and pitch
        pitch_offset = self.pitch * 2  # Scale pitch for better visualization
        roll_angle = math.radians(self.roll)
        
        horizon_line_length = 2 * radius
        half_length = horizon_line_length / 2
        sin_roll = math.sin(roll_angle)
        cos_roll = math.cos(roll_angle)
        
        x1 = center_x - half_length * cos_roll
        y1 = center_y + pitch_offset - half_length * sin_roll
        x2 = center_x + half_length * cos_roll
        y2 = center_y + pitch_offset + half_length * sin_roll
        
        # Clip the horizon line to the edges of the circle
        def clip_line_to_circle(x1, y1, x2, y2, center_x, center_y, radius):
            dx = x2 - x1
            dy = y2 - y1
            dr = math.sqrt(dx**2 + dy**2)
            D = x1 * y2 - x2 * y1
            delta = radius**2 * dr**2 - D**2
            if delta < 0:
                return None
            sign_dy = 1 if dy >= 0 else -1
            sqrt_delta = math.sqrt(delta)
            x_intersect1 = (D * dy + sign_dy * dx * sqrt_delta) / (dr**2) + center_x
            y_intersect1 = (-D * dx + abs(dy) * sqrt_delta) / (dr**2) + center_y
            x_intersect2 = (D * dy - sign_dy * dx * sqrt_delta) / (dr**2) + center_x
            y_intersect2 = (-D * dx - abs(dy) * sqrt_delta) / (dr**2) + center_y
            return (x_intersect1, y_intersect1), (x_intersect2, y_intersect2)

        intersections = clip_line_to_circle(x1, y1, x2, y2, center_x, center_y, radius)
        if intersections:
            (x1, y1), (x2, y2) = intersections

        # Draw the horizon line
        self.canvas_attitude.create_line(x1, y1, x2, y2, fill="green", width=2)
        
        # Draw the perpendicular line for roll
        perpendicular_length = 20
        x_perpendicular1 = center_x + perpendicular_length * math.cos(roll_angle + math.pi / 2)
        y_perpendicular1 = center_y + perpendicular_length * math.sin(roll_angle + math.pi / 2)
        x_perpendicular2 = center_x + perpendicular_length * math.cos(roll_angle - math.pi / 2)
        y_perpendicular2 = center_y + perpendicular_length * math.sin(roll_angle - math.pi / 2)
        self.canvas_attitude.create_line(x_perpendicular1, y_perpendicular1, x_perpendicular2, y_perpendicular2, fill="black", width=2)
        
        # Draw the airplane wings
        self.canvas_attitude.create_line(center_x - 20, center_y, center_x + 20, center_y, fill="black", width=3)
        self.canvas_attitude.create_line(center_x, center_y - 20, center_x, center_y + 20, fill="black", width=3)
        
        # Draw roll ticks
        for angle in range(-180, 181, 10):
            tick_angle_rad = math.radians(angle)
            tick_x_inner = center_x + (radius - 10) * math.sin(tick_angle_rad)
            tick_y_inner = center_y - (radius - 10) * math.cos(tick_angle_rad)
            tick_x_outer = center_x + radius * math.sin(tick_angle_rad)
            tick_y_outer = center_y - radius * math.cos(tick_angle_rad)
            self.canvas_attitude.create_line(tick_x_inner, tick_y_inner, tick_x_outer, tick_y_outer, fill="green", width=2)
            if angle % 30 == 0:
                tick_label_x = center_x + (radius + 20) * math.sin(tick_angle_rad)
                tick_label_y = center_y - (radius + 20) * math.cos(tick_angle_rad)
                if angle < 0:
                    angle_label = 360 + angle
                else:
                    angle_label = angle
                self.canvas_attitude.create_text(tick_label_x, tick_label_y, text=str(angle_label), font=("Arial", 8), fill="green")
        
        self.canvas_attitude.create_text(center_x, center_y + radius + 40, text=f"Pitch: {self.pitch}° Roll: {self.roll}°", font=("Arial", 12))