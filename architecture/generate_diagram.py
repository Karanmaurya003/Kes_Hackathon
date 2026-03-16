from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 600
bg = Image.new("RGB", (WIDTH, HEIGHT), "#f7f3ee")
draw = ImageDraw.Draw(bg)

title = "PHISHLENS AI SYSTEM PIPELINE"
draw.text((40, 30), title, fill="#0f1a24")

boxes = [
    "User Input",
    "Threat Input Module",
    "Feature Extraction",
    "Detection Engines",
    "Explainable AI",
    "Risk Scoring",
    "Response Recommendation",
    "Dashboard",
]

start_x = 40
start_y = 120
box_w = 260
box_h = 50
gap_y = 20

for i, label in enumerate(boxes):
    y = start_y + i * (box_h + gap_y)
    draw.rounded_rectangle(
        [start_x, y, start_x + box_w, y + box_h],
        radius=12,
        outline="#0f4c5c",
        width=3,
        fill="#ffffff",
    )
    draw.text((start_x + 12, y + 15), label, fill="#0f1a24")
    if i < len(boxes) - 1:
        mid_x = start_x + box_w / 2
        draw.line(
            [mid_x, y + box_h, mid_x, y + box_h + gap_y],
            fill="#0f4c5c",
            width=3,
        )

bg.save("system_diagram.png")
print("Saved system_diagram.png")

