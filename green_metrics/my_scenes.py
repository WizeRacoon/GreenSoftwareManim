from manim import *

class HeavyScene(Scene):
    def construct(self):
        # Generate 500 individual Mobjects (heavy initial allocation)
        circles = VGroup(*[Circle(radius=0.1) for _ in range(500)])
        circles.arrange_in_grid(rows=20, cols=25)
        
        # Generate 500 target Mobjects
        squares = VGroup(*[Square(side_length=0.2) for _ in range(500)])
        squares.arrange_in_grid(rows=20, cols=25)
        
        # The Transform forces heavy Bezier calculations across hundreds of arrays
        self.play(Transform(circles, squares), run_time=5)
        self.wait(1)
