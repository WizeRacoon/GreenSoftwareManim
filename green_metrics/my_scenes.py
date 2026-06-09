from manim import *

class HeavyScene(ThreeDScene):
    def construct(self):
        # 1. Test Flat Shapes & High Object Count
        grid = VGroup(*[Circle(radius=0.1, color=RED) for _ in range(100)]).arrange_in_grid(rows=10, cols=10)
        
        # 2. Test Complex Subpaths (Holes) - FIXED: Swapped Ring for Annulus
        donut = Annulus(inner_radius=0.5, outer_radius=1.0, color=BLUE)
        
        # 3. Test Text Rendering & Font Paths (Hammers subpath logic)
        text = Text("Green Software 2026, Group 8", font="Sans").scale(0.7)
        
        # 4. Test Linear Gradients (Triggers the else branch in set_cairo_context_color)
        gradient_rect = Rectangle(width=4, height=2)
        gradient_rect.set_fill(color=[GOLD, "#800020"], opacity=1.0)  # Standard hex string for burgundy
        gradient_rect.set_stroke(color=WHITE, width=6) # Tests line styles
        
        # Layout everything on screen
        group = VGroup(grid, donut, text, gradient_rect).arrange(RIGHT, buff=1.0)
        self.add(group)
        
        # 5. Massive Interpolation Morph (Stresses bezier.py and path loops simultaneously)
        target_grid = VGroup(*[Square(side_length=0.1, color=WHITE) for _ in range(100)]).arrange_in_grid(rows=10, cols=10)
        target_donut = Star(color=PURPLE).scale(0.5)
        target_text = Text("Test Scene", font="Sans").scale(1.5)
        target_rect = Circle(radius=1.5).set_fill(color=[BLUE, GREEN], opacity=1.0)
        
        target_group = VGroup(target_grid, target_donut, target_text, target_rect).arrange(RIGHT, buff=1.0)
        
        # Play the complex transformation forward
        self.play(ReplacementTransform(group, target_group), run_time=5.0) 
        self.wait(1.0)
        # Morph it back to stretch the execution window safely
        self.play(ReplacementTransform(target_group, group), run_time=5.0)
        self.wait(1.0)
        
        # Quick 3D Sanity Check at the end of construct()
        self.next_section()
        cube = Cube(color=GOLD).scale(1.5)
        
        # FIXED: Changes the perspective instantly without an animation runtime conflict
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES) 
        
        self.play(DrawBorderThenFill(cube))
        self.play(Rotate(cube, angle=PI/2, axis=UP), run_time=2.0)