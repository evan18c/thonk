from JavaScript import *

# Colors
BODY = 'rgb(255, 203, 76)'
HAND = 'rgb(241, 144, 32)'
FEAT = 'rgb(101, 71, 27)'

# random.randint
def randint(min: int, max: int) -> int:
    return Math.round(Math.random() * (max - min) + min)

# Draws a polygon and fills it
def draw_polygon(ctx: object, points: list, color: str) -> None:
    ctx.beginPath()
    first = points[0]
    ctx.moveTo(first[0], first[1])
    for i in range(len(points)):
        point = points[i]
        ctx.lineTo(point[0], point[1])
    ctx.closePath()
    ctx.fillStyle = color
    ctx.fill()

# Smoothens points
def chaikin(points: list, iterations: int) -> list:
    for _ in range(iterations):
        new_points = []
        n = len(points)
        for i in range(n):
            p0 = points[i]
            next = i + 1
            p1 = points[next % n]
            q = (0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1])
            r = (0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1])
            new_points.append(q)
            new_points.append(r)
        points = new_points
    return points

# Checks if a point is in a polygon
def contains_point(polygon: list, point: list) -> bool:
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        pi = polygon[i]
        pj = polygon[j]
        xi = pi[0]
        yi = pi[1]
        xj = pj[0]
        yj = pj[1]
        intersect = ((yi > point[1]) != (yj > point[1])) and (point[0] < ((xj - xi) * (point[1] - yi) / (yj - yi) + xi))
        if intersect:
            inside = not inside
        j = i
    return inside

# Transforms a polygon SRT (Scale, Rotate, Translate)
def transform(points: list, origin: list, scaler: int, rotation: int, translation: list) -> list:
    new_points = []
    for point in points:
        new_x = point[0] + translation[0]
        new_y = point[1] + translation[1]
        new_points.append((new_x, new_y))
    return new_points


# Generates a random shape
def polygon(center: list, size_range: list, total_points: int, chaikin_iterations: int) -> list:
    points = []
    total = total_points
    for i in range(total):
        angle = (i / total) * 6.283185307179586
        magnitude = randint(size_range[0], size_range[1])
        point_x = center[0] + Math.cos(angle) * magnitude
        point_y = center[1] + Math.sin(angle) * magnitude
        point = (point_x, point_y)
        points.append(point)
    points = chaikin(points, chaikin_iterations)
    return points

# Generates a random point in a polygon
def random_point_in_polygon(points: list) -> list:
    inside = False
    while not inside:
        x = randint(0, 500)
        y = randint(0, 500)
        if contains_point(points, (x, y)):
            inside = True
    return (x, y)

# Generates a random point in a polygon AND inside boundaries
def random_point_in_polygon_in_boundary(points: list, range_x: list, range_y: list) -> list:
    inside = False
    while not inside:
        x = randint(0, 500)
        y = randint(0, 500)
        if contains_point(points, (x, y)) and (x >= range_x[0]) and (x <= range_x[1]) and (y >= range_y[0]) and (y <= range_y[1]):
            inside = True
    return (x, y)

# Generates thonk
def thonk():

    # Canvas
    canvas = document.getElementById('thonk_canvas')
    ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    # Body
    body = polygon([250, 250], [50, 250], 10, 3)
    draw_polygon(ctx, body, BODY)

    # Eye 1
    eye1_pos = random_point_in_polygon_in_boundary(body, [0, 250], [0, 250])
    eye1 = polygon(eye1_pos, [15, 20], 10, 3)
    draw_polygon(ctx, eye1, FEAT)

    # Eye 2
    eye2_pos = random_point_in_polygon_in_boundary(body, [250, 500], [0, 250])
    eye2 = polygon(eye2_pos, [15, 20], 10, 3)
    draw_polygon(ctx, eye2, FEAT)

    # Eyebrow 1
    eyebrow1_p1 = (eye1_pos[0] - randint(25, 50), eye1_pos[1] - randint(25, 50))
    eyebrow1_p2 = (eye1_pos[0] + randint(25, 50), eye1_pos[1] - randint(25, 50))
    eyebrow1_pm = (eye1_pos[0], eye1_pos[1] - randint(50, 75))
    eyebrow1_w = randint(10, 20)
    ctx.beginPath()
    ctx.moveTo(eyebrow1_p1[0], eyebrow1_p1[1])
    ctx.quadraticCurveTo(eyebrow1_pm[0], eyebrow1_pm[1], eyebrow1_p2[0], eyebrow1_p2[1])
    ctx.strokeStyle = FEAT
    ctx.lineWidth = eyebrow1_w
    ctx.lineCap = 'square'
    ctx.stroke()

    # Eyebrow 2
    eyebrow2_p1 = (eye2_pos[0] - randint(25, 50), eye2_pos[1] - randint(10, 25))
    eyebrow2_p2 = (eye2_pos[0] + randint(25, 50), eye2_pos[1] - randint(25, 40))
    eyebrow2_pm = (eye2_pos[0], eye2_pos[1] - randint(20, 30))
    eyebrow2_w = randint(10, 20)
    ctx.beginPath()
    ctx.moveTo(eyebrow2_p1[0], eyebrow2_p1[1])
    ctx.quadraticCurveTo(eyebrow2_pm[0], eyebrow2_pm[1], eyebrow2_p2[0], eyebrow2_p2[1])
    ctx.strokeStyle = FEAT
    ctx.lineWidth = eyebrow2_w
    ctx.lineCap = 'square'
    ctx.stroke()

    # Mouth
    mouth_p1 = random_point_in_polygon_in_boundary(body, [0, 250], [250, 500])
    mouth_p2 = random_point_in_polygon_in_boundary(body, [250, 500], [250, 500])
    mouth_pm = random_point_in_polygon_in_boundary(body, [200, 300], [250, 500])
    mouth_w = randint(20, 30)
    ctx.beginPath()
    ctx.moveTo(mouth_p1[0], mouth_p1[1])
    ctx.quadraticCurveTo(mouth_pm[0], mouth_pm[1], mouth_p2[0], mouth_p2[1])
    ctx.strokeStyle = FEAT
    ctx.lineWidth = mouth_w
    ctx.lineCap = 'round'
    ctx.stroke()

    # Hand
    hand_points = chaikin([(0, 0), (0, 50), (50, 50), (50, 25), (75, 25), (75, 15), (15, 15), (15, 0)], 3)
    hand_pos = random_point_in_polygon_in_boundary(body, [0, 500], [250, 500])
    hand_points = transform(hand_points, (0, 0), (1, 1), 0, hand_pos)
    draw_polygon(ctx, hand_points, HAND)

# Load thonk
window.onload = thonk
