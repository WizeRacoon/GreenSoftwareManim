from __future__ import annotations
from manim import *

class PythagoreanProof(Scene):
    def construct(self):
        a = 3.0
        b = 4.0
        scale = 0.75  # Kept large since we are using a single centered box
        sa = a * scale
        sb = b * scale
        side_length = (a + b) * scale
        
        # Color palette mapping
        color_a = MAROON_B     
        color_b = YELLOW_C     
        color_c = BLUE_C       
        color_tri = TEAL       
        
        # Main Title
        title = Text("Pythagorean Theorem: Geometric Proof", font="Fira Sans").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Bounding container square
        box = Square(side_length=side_length, stroke_color=GRAY).shift(DOWN * 0.3)
        box_label = MathTex("\\text{Total Area: } (", "a", "+" , "b", ")^2").scale(0.6).next_to(box, UP, buff=0.2)
        box_label[1].set_color(color_a)
        box_label[3].set_color(color_b)
        self.play(Create(box), Write(box_label))
        
        c_dl = box.get_corner(DL)
        c_dr = box.get_corner(DR)
        c_ur = box.get_corner(UR)
        c_ul = box.get_corner(UL)
        
        # ---------------------------------------------------------
        # INITIAL STATE: Layout 2 (Exposing a² and b²)
        # ---------------------------------------------------------
        # Bottom-Left Rectangle (made of 2 triangles)
        t1 = Polygon(c_dl, c_dl + RIGHT*sb, c_dl + RIGHT*sb + UP*sa, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        t2 = Polygon(c_dl, c_dl + UP*sa, c_dl + RIGHT*sb + UP*sa, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        
        # Top-Right Rectangle (made of 2 triangles)
        t3 = Polygon(c_ur, c_ur + LEFT*sa, c_ur + LEFT*sa + DOWN*sb, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        t4 = Polygon(c_ur, c_ur + DOWN*sb, c_ur + LEFT*sa + DOWN*sb, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        
        # FIX ISSUE 1: SWAP POSITIONS FOR a2 and b2 LABELS
        # Empty Area 1 (UL) has side length 'b', its area is b^2.
        # Empty Area 2 (DR) has side length 'a', its area is a^2.
        label_a2 = MathTex("a^2", color=color_a).scale(1.2).move_to(c_dr + UP*(sb/2.5) + LEFT*(sb/2.5))
        label_b2 = MathTex("b^2", color=color_b).scale(1.2).move_to(c_ul + DOWN*(sa/1.5) + RIGHT*(sa/1.5))
        
        # Explicit rectangle side length markings
        # FIX ISSUE 2: COLOR SIDE MARKINGS TO MATCH LABELS
        dim_rect1_b = MathTex("b", color=color_b).scale(0.5).next_to(c_dl + RIGHT*(sb/2), DOWN, buff=0.1)
        dim_rect1_a = MathTex("a", color=color_a).scale(0.5).next_to(c_dl + UP*(sa/2), LEFT, buff=0.1)
        dim_rect2_a = MathTex("a", color=color_a).scale(0.5).next_to(c_ur + LEFT*(sa/2), UP, buff=0.1)
        dim_rect2_b = MathTex("b", color=color_b).scale(0.5).next_to(c_ur + DOWN*(sb/2), RIGHT, buff=0.1)
        
        # UPDATE EQUATION text and color to reflect swapped labels
        equation = MathTex("\\text{Empty Area} = ", "a^2", "+", "b^2").scale(0.9)
        equation[1].set_color(color_a)
        equation[3].set_color(color_b)
        equation.next_to(box, DOWN, buff=0.4)
        
        self.play(
            FadeIn(t1, t2, t3, t4),
            Write(label_a2), Write(label_b2),
            Write(dim_rect1_b), Write(dim_rect1_a), Write(dim_rect2_a), Write(dim_rect2_b),
            Write(equation)
        )
        self.wait(2.5)  # <-- SCREENSHOT 1: Layout 2 Context
        
        # ---------------------------------------------------------
        # MORPH TRANSFORMATION: Layout 2 ---> Layout 1
        # ---------------------------------------------------------
        # Clean up old labels before shifting geometry
        self.play(
            FadeOut(label_a2), FadeOut(label_b2),
            FadeOut(dim_rect1_b), FadeOut(dim_rect1_a), FadeOut(dim_rect2_a), FadeOut(dim_rect2_b),
            FadeOut(equation),
            run_time=0.5
        )
        
        # Target layout positions where right angles sit perfectly in the box corners
        # t1 stays at DL corner, but changes orientation to wrap the edge
        t1_target = Polygon(c_dl, c_dl + RIGHT*sb, c_dl + UP*sa, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        t2_target = Polygon(c_dr, c_dr + UP*sb, c_dr + LEFT*sa, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        t3_target = Polygon(c_ur, c_ur + LEFT*sb, c_ur + DOWN*sa, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        t4_target = Polygon(c_ul, c_ul + DOWN*sb, c_ul + RIGHT*sa, fill_color=color_tri, fill_opacity=0.75, stroke_color=WHITE)
        
        self.play(
            Transform(t1, t1_target),
            Transform(t2, t2_target),
            Transform(t3, t3_target),
            Transform(t4, t4_target),
            run_time=2.5
        )
        
        # ---------------------------------------------------------
        # FINAL STATE: Layout 1 (Exposing c²)
        # ---------------------------------------------------------
        label_c2 = MathTex("c^2", color=color_c).scale(1.2).move_to(box.get_center())
        
        # Add side definitions for individual triangles to denote clarity
        # FIX ISSUE 2: COLOR SIDE MARKINGS TO MATCH LABELS
        lbl_tri_a = MathTex("a", color=color_a).scale(0.7).move_to(c_dl + UP*(sa/2) + RIGHT*0.15)
        lbl_tri_b = MathTex("b", color=color_b).scale(0.7).move_to(c_dl + RIGHT*(sb/2) + UP*0.15)
        lbl_tri_c = MathTex("c", color=color_c).scale(0.7).move_to(c_dl + RIGHT*(sb/2) + UP*(sa/2) + UR*0.15)
        
        # The standard proof morphs from b^2+a^2 = total Area - 4Tri to total Area - 4Tri = c^2, so b^2+a^2=c^2 is shown.
        # The user wants to fix reversed labels in Initial state. Morphed state shows standard c^2 area, I will keep standard colors here.
        final_theorem = MathTex("a^2", "+", "b^2", "=", "c^2").scale(1.2)
        final_theorem[0].set_color(color_a)
        final_theorem[2].set_color(color_b)
        final_theorem[4].set_color(color_c)
        final_theorem.next_to(box, DOWN, buff=0.4)
        
        self.play(
            Write(label_c2),
            Write(lbl_tri_a), Write(lbl_tri_b), Write(lbl_tri_c),
            Write(final_theorem)
        )
        self.wait(3.5)  # <-- SCREENSHOT 2: Morph Completion context